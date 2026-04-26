"""
Rule-based quality tag suggestions for DRE assets.
"""

def suggest_quality_tags(asset) -> list:
    suggestions = []

    if not asset.title or len(asset.title.strip()) < 5:
        suggestions.append('needs-better-title')

    if not asset.description or len(asset.description.strip()) < 20:
        suggestions.append('needs-description')

    if not asset.file_url:
        suggestions.append('no-file-url')

    if asset.tags.count() == 0:
        suggestions.append('untagged')

    if asset.status == 'draft' and len(suggestions) == 0:
        suggestions.append('ready-for-review')

    if asset.status == 'approved' and asset.tags.count() >= 2 and asset.file_url:
        suggestions.append('fully-complete')

    return suggestions