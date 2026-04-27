# Design Notes

## Architecture Choice

Django REST Framework with a single `assets` app. Chose DRF because it provides
serializers, viewsets, and a browsable API out of the box — reducing boilerplate
while keeping the code readable and testable. Used `ModelViewSet` to handle all
CRUD operations cleanly with minimal repetition.

## Data Model

Three models:

- **Tag** : reusable labels with auto-generated slugs. Many to many with Asset.
- **Asset** : core entity. Stores title, description, type, file URL, status, and tags.
  Uses `choices` fields for `asset_type` and `status` to enforce valid values at the DB level.
- **ChangeLog**: immutable audit record. Created automatically on every Asset create/update.
  via `perform_create` and `perform_update` in the viewset. Stores a JSON snapshot with:
  - `previous` :full asset state before the change (null on creation).
  - `new` : full asset state after the change.
  - `diff` : only the fields that actually changed, each showing previous → new value.
  - `changed_by` : username of the person who made the change, or "anonymous".
  - `changed_at` : UTC timestamp auto set on creation.

## Endpoints Design

Used DRF `DefaultRouter` for standard CRUD, plus two custom `@action` endpoints:
- `GET /api/assets/{id}/history/` — returns all ChangeLog entries for that asset
- `GET /api/assets/{id}/suggest-tags/` — runs the quality tag engine and returns suggestions

## Audit Log Design (Spec Update)

The `perform_update` method captures the full asset state **before** saving, then the full
state **after** saving. It computes a `diff` dict containing only the fields that changed.
This means the history endpoint shows exactly what changed on each update, not just
that something changed. The `changed_by` field records who made the change — currently
reads from the authenticated user, defaulting to "anonymous" since authentication is
out of scope for this assessment.

## Edge Cases Handled

- Search filter uses `Q` objects with `icontains` so it is case-insensitive.
- `tag_ids` is write-only in the serializer; `tags` is read-only avoids nested write complexity.
- `slug` is auto-generated from `name` on Tag creation so it cannot be submitted incorrectly.
- ChangeLog ordering is `-changed_at` so most recent change always comes first.
- On creation, `snapshot.previous` is explicitly set to `null` to distinguish create from update entries.

## Ownership Note
All design decisions were made and are understood by the author. Any part of this system
can be explained, modified, or extended live in line with DRE quality and ownership
standards (DRE-AI-POLICY-v1.0, Section 9).

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| ChangeLog not created on bulk updates | Documented as known limitation; not in scope |
| No authentication | Acceptable for assessment scope; `changed_by` defaults to "anonymous" |
| SQLite concurrency limits | Fine for dev/assessment; PostgreSQL recommended for production |
