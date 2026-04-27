from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from .models import Asset, Tag, ChangeLog
from .serializers import AssetSerializer, TagSerializer, ChangeLogSerializer
from .quality_tags import suggest_quality_tags


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.prefetch_related('tags').all()
    serializer_class = AssetSerializer

    def get_queryset(self):
        qs         = super().get_queryset()
        search     = self.request.query_params.get('search')
        status_    = self.request.query_params.get('status')
        asset_type = self.request.query_params.get('asset_type')

        if search:
            qs = qs.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        if status_:
            qs = qs.filter(status=status_)
        if asset_type:
            qs = qs.filter(asset_type=asset_type)
        return qs

    def _get_snapshot(self, asset):
        return {
            'title':       asset.title,
            'description': asset.description,
            'asset_type':  asset.asset_type,
            'file_url':    asset.file_url,
            'status':      asset.status,
            'tags':        list(asset.tags.values_list('name', flat=True)),
        }

    def _get_changed_by(self):
        user = self.request.user
        if user and user.is_authenticated:
            return user.username
        return 'anonymous'

    def perform_create(self, serializer):
        asset = serializer.save()
        ChangeLog.objects.create(
            asset=asset,
            change_summary='Asset created',
            changed_by=self._get_changed_by(),
            snapshot={
                'previous': None,
                'new':      self._get_snapshot(asset),
            }
        )

    def perform_update(self, serializer):
        previous = self._get_snapshot(serializer.instance)
        asset    = serializer.save()
        new      = self._get_snapshot(asset)
        diff = {
            field: {'previous': previous[field], 'new': new[field]}
            for field in new
            if previous[field] != new[field]
        }

        ChangeLog.objects.create(
            asset=asset,
            change_summary=f"Updated fields: {', '.join(diff.keys()) or 'none'}",
            changed_by=self._get_changed_by(),
            snapshot={
                'previous': previous,
                'new':      new,
                'diff':     diff,
            }
        )

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        asset      = self.get_object()
        logs       = asset.history.all()
        serializer = ChangeLogSerializer(logs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='suggest-tags')
    def suggest_tags(self, request, pk=None):
        asset       = self.get_object()
        suggestions = suggest_quality_tags(asset)
        return Response({'suggestions': suggestions})