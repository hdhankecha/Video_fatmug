from django.urls import path
from .views import upload_video, video_list, view_video, search_subtitles
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', upload_video, name='upload_video'),
    path('video_list/', video_list, name='video_list'),
    path('video/<int:id>/', view_video, name='view_video'),
    path('search-subtitles/', search_subtitles, name='search_subtitles'),  # Add this line

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
