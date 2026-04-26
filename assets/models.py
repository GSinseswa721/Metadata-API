from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Asset(models.Model):

    TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('document', 'Document'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('review', 'In Review'),
        ('approved', 'Approved'),
        ('archived', 'Archived'),
    ]

    title       = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    asset_type  = models.CharField(max_length=20, choices=TYPE_CHOICES, default='other')
    file_url    = models.URLField(blank=True, default='')
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    tags        = models.ManyToManyField(Tag, blank=True, related_name='assets')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ChangeLog(models.Model):
    asset          = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='history')
    change_summary = models.CharField(max_length=255)
    snapshot       = models.JSONField()
    changed_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-changed_at']

    def __str__(self):
        return f"{self.asset.title} — {self.changed_at:%Y-%m-%d %H:%M}"