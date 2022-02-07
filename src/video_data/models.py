from django.db import models

# The VideoData model represents a single tuple of the video data in our database
class VideoData(models.Model):
    youtube_pk = models.TextField()
    title = models.TextField()
    description = models.TextField()
    pub_datetime = models.DateTimeField(null=True, auto_now_add=False, editable=True)
    thumbnail_default = models.TextField()
    thumbnail_medium = models.TextField()
    thumbnail_high = models.TextField()
    channel_title = models.TextField()

    # Creating indexes for search optimizations
    class Meta:
        indexes = [
            models.Index(fields=['title', 'description']), # good for both (title & desc) and (title) kind of queries
            models.Index(fields=['description']),  # good for both (desc) kind of queries
        ]

    def __str__(self):
        return self.title