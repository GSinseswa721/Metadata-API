# Test Plan

All tests are in `assets/tests.py` and run with `python3 manage.py test assets`.

## Tests

### 1. `test_create_tag`
**What it checks:** POST to `/api/tags/` creates a tag and auto generates the correct slug.
**Why:** Slug generation is custom logic in the serializer needs explicit verification.

### 2. `test_create_asset_returns_201`
**What it checks:** POST to `/api/assets/` with valid data returns HTTP 201 and saves to DB.
**Why:** Core happy path test. If this fails, nothing else matters.

### 3. `test_create_asset_auto_creates_changelog`
**What it checks:** After creating an asset, exactly one ChangeLog entry exists with `change_summary = "Asset created"`.
**Why:** ChangeLog auto creation is a key business requirement must be verified independently from asset creation.

### 4. `test_update_asset_adds_changelog_entry`
**What it checks:** PATCH on an existing asset adds a second ChangeLog entry (total = 2).
**Why:** Verifies that history grows correctly on every update, not just on creation.

### 5. `test_search_assets_by_title`
**What it checks:** GET `/api/assets/?search=Promo` returns only assets whose title matches.
**Why:** Search is a required endpoint feature must return correct filtered results.

### 6. `test_history_endpoint`
**What it checks:** GET `/api/assets/{id}/history/` returns HTTP 200 with one entry after creation.
**Why:** Verifies the custom `@action` endpoint is routed and responds correctly.

### 7. `test_suggest_tags_for_incomplete_asset`
**What it checks:** An asset with a short title and no description/tags gets back `needs-better-title`, `needs-description`, and `untagged` suggestions.
**Why:** Verifies the rule-based quality tag engine logic end to end through the API.

### 8. `test_audit_log_captures_previous_and_new_values`
**What it checks:** After a PATCH, the ChangeLog `diff` correctly records the previous and new values of the changed field (e.g. status: draft → approved).
**Why:** Directly verifies the spec update requirement the audit log must capture what changed, not just that something changed.

### 9. `test_create_changelog_has_no_previous`
**What it checks:** On asset creation, the ChangeLog snapshot has `previous: null` since there is no prior state.
**Why:** Verifies that the create and update audit paths are handled separately and correctly.

### 10. `test_audit_log_records_changed_by`
**What it checks:** The `changed_by` field on the ChangeLog is set to `"anonymous"` when no authenticated user makes the request.
**Why:** Verifies the "who" requirement from the spec update the audit log must record the author of every change.
