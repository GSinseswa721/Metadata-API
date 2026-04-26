# Design Notes

## Architecture Choice

Django REST Framework with a single `assets` app. Chose DRF because it provides
serializers, viewsets, and a browsable. Used `ModelViewSet` to handle all
CRUD operations cleanly with minimal repetition.

## Data Model

Three models:

- **Tag** : reusable labels with auto-generated slugs. Many to many with Asset.
- **Asset** : core entity. Stores title, description, type, file URL, status, and tags.
  Uses `choices` fields for `asset_type` and `status` to enforce valid values at the DB level.
- **ChangeLog** : immutable audit record. Created automatically on every Asset create/update
  via `perform_create` and `perform_update` in the viewset. Stores a JSON snapshot of the
  asset state at that moment so history is fully reconstructable.

## Endpoints Design

Used DRF `DefaultRouter` for standard CRUD, plus two custom `@action` endpoints:
- `GET /api/assets/{id}/history/` , returns all ChangeLog entries for that asset
- `GET /api/assets/{id}/suggest-tags/` , runs the quality tag engine and returns suggestions

## Edge Cases Handled

- Search filter uses `Q` objects with `icontains` so it is case insensitive.
- `tag_ids` is write only in the serializer; `tags` is read-only avoids nested write complexity.
- `slug` is auto generated from `name` on Tag creation so it cannot be submitted incorrectly
- ChangeLog ordering is `-changed_at` so most recent change always comes first.



