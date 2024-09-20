from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/', max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Subtitle(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='subtitles')
    subtitle_file = models.FileField(upload_to='subtitles/', max_length=255)
    language = models.CharField(max_length=50, default='Unknown')
    stream_index = models.CharField(max_length=100)


    def __str__(self):
        return f"{self.language} - {self.video.title}"

