from rest_framework import serializers
from django.utils.text import slugify
from .models import Asset, Tag, ChangeLog


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Tag
        fields = ['id', 'name', 'slug']
        read_only_fields = ['slug']

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['name'])
        return super().create(validated_data)


class ChangeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ChangeLog
        fields = ['id', 'change_summary', 'changed_by', 'snapshot', 'changed_at'] 


class AssetSerializer(serializers.ModelSerializer):
    tags    = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(),
        write_only=True, source='tags', required=False
    )

    class Meta:
        model  = Asset
        fields = [
            'id', 'title', 'description', 'asset_type',
            'file_url', 'status', 'tags', 'tag_ids',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']