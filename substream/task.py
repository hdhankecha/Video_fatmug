# from celery import shared_task
# import subprocess
# import os
#
# @shared_task
# def process_video(video_id):
#     from .models import Video
#     video = Video.objects.get(id=video_id)
#     video_path = video.video_file.path
#     subtitle_path = video_path.replace('.mp4', '.srt')
#
#     try:
#         subprocess.run(['ccextractor', video_path, '-o', subtitle_path], check=True)
#         with open(subtitle_path, 'r') as f:
#             video.subtitle_file = f.read()
#         video.save()
#     except subprocess.CalledProcessError:
#         # Handle errors
#         pass
