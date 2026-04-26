# Dev Journal

- **Setup issue:** Django was installed globally before the virtual environment was activated.

- **Models decision:** Initially considered putting ChangeLog logic in a Django signal,
  but overriding `perform_create` and `perform_update` in the viewset kept the audit
  logic visible and easier to trace during a code review.

- **Serializer write vs read:** First attempt returned nested tag objects on both read
  and write, which caused DRF to reject tag data.

- **400 error on browsable API:** The raw JSON form submitted `null` for choice fields,
  causing a parse error. Switched to the HTML form view in DRF which sends clean values.

- **All 7 tests green** on first full run after fixing the serializer split.

