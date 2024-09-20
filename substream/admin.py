from django.contrib import admin

from substream.models import Video, Subtitle


# Register your models here.


class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_file', 'uploaded_at')


class SubtitleAdmin(admin.ModelAdmin):
    list_display = ('video', 'subtitle_file', 'language','stream_index')


admin.site.register(Video, VideoAdmin)
admin.site.register(Subtitle, SubtitleAdmin)
