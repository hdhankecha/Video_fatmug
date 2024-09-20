import os
import subprocess
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from .models import Video, Subtitle
from .forms import VideoUploadForm, SearchForm
import re


def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video_instance = form.save()
            video_path = video_instance.video_file.path

            # Extract all subtitles from the video
            subtitle_paths = extract_subtitles_from_video(video_path)

            if subtitle_paths:
                for subtitle_path, language, stream_index in subtitle_paths:
                    # Save subtitle path relative to media root
                    relative_path = os.path.relpath(subtitle_path, start=settings.MEDIA_ROOT)
                    # Create and save subtitle object for each language
                    Subtitle.objects.create(
                        video=video_instance,
                        subtitle_file=relative_path,
                        language=language,
                        stream_index=stream_index
                    )

            return redirect('video_list')
    else:
        form = VideoUploadForm()

    return render(request, 'templates/upload.html', {'form': form})


def extract_subtitles_from_video(video_path):
    subtitle_streams = probe_subtitles(video_path)

    if not subtitle_streams:
        print("No subtitle streams found in the video.")
        return []

    subtitle_paths = []
    for stream_index, language in subtitle_streams:
        subtitle_path = extract_subtitle(video_path, stream_index)
        if subtitle_path and os.path.exists(subtitle_path):
            # Convert SRT to VTT
            vtt_path = convert_srt_to_vtt(subtitle_path)
            if vtt_path and os.path.exists(vtt_path):
                subtitle_paths.append((vtt_path, language, stream_index))
                # remove SRT file after conversion
                os.remove(subtitle_path)
            else:
                print(f"Failed to convert SRT to VTT or VTT file not found for stream {stream_index}")
        else:
            print(f"Failed to extract subtitle or subtitle path does not exist for stream {stream_index}")

    return subtitle_paths


def probe_subtitles(video_path):
    """Use ffprobe to find subtitle streams in the video."""
    ffprobe_path = 'C:/ffmpeg-7.0.2-essentials_build/bin/ffprobe.exe'
    probe_command = [
        ffprobe_path,
        '-v', 'error',
        '-select_streams', 's',  # Select subtitle streams
        '-show_entries', 'stream=index:stream_tags=language',
        '-of', 'csv=p=0',
        video_path
    ]

    try:
        result = subprocess.run(probe_command, capture_output=True, text=True, check=True)
        output_lines = result.stdout.strip().split('\n')
        print(f"ffprobe output:\n{result.stdout}")

        subtitle_streams = []
        for line in output_lines:
            if line.strip():
                parts = line.split(',')
                if len(parts) >= 2:
                    stream_index = parts[0]
                    language = parts[1] if parts[1] else 'unknown'
                    subtitle_streams.append((stream_index, language))

        print(f"Detected subtitle streams: {subtitle_streams}")
        return subtitle_streams

    except subprocess.CalledProcessError as e:
        print(f"Error probing video: {e}")
        return []


def extract_subtitle(video_path, stream_index):
    ffmpeg_path = 'C:/ffmpeg-7.0.2-essentials_build/bin/ffmpeg.exe'
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    subtitle_path = os.path.join('media', 'subtitles', f'{base_name}_s{stream_index}.srt')

    print(f"Extracting subtitle to: {subtitle_path}")
    os.makedirs(os.path.dirname(subtitle_path), exist_ok=True)
    # todo FFmpeg command to extract subtitle
    command = [
        ffmpeg_path,
        '-i', video_path,  # todo input file
        '-map', f'0:s:{stream_index}?',
        '-c:s', 'srt',
        subtitle_path
    ]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Subtitles extracted to {subtitle_path}")
        print(f"FFmpeg output:\n{result.stdout}")
        return subtitle_path

    except subprocess.CalledProcessError as e:
        print(f"Error extracting subtitles from stream {stream_index}: {e}")
        print(f"FFmpeg output:\n{e.stdout}")
        print(f"FFmpeg error output:\n{e.stderr}")
        return None


def convert_srt_to_vtt(srt_file):
    vtt_file = srt_file.replace('.srt', '.vtt')
    try:
        with open(srt_file, 'r', encoding='utf-8') as srt:
            with open(vtt_file, 'w', encoding='utf-8') as vtt:
                vtt.write('WEBVTT\n\n')  # WebVTT header
                for line in srt:
                    line = re.sub(r'(\d{2}):(\d{2}):(\d{2}),(\d{3})', r'\1:\2:\3.\4', line)
                    vtt.write(line)
        print(f"Converted SRT to VTT: {vtt_file}")
        return vtt_file
    except Exception as e:
        print(f"Error converting SRT to VTT: {e}")
        return None


def video_list(request):
    videos = Video.objects.all()
    return render(request, 'templates/list.html', {'videos': videos})


def view_video(request, id):
    video = get_object_or_404(Video, pk=id)
    subtitles = video.subtitles.all()

    # todo Handle the search functionality
    search_results = []
    form = SearchForm(request.GET or None)

    if form.is_valid():
        query = form.cleaned_data['query'].lower()
        # Search through the subtitle files
        for subtitle in subtitles:
            subtitle_path = os.path.join(settings.MEDIA_ROOT, str(subtitle.subtitle_file))
            print(f"Searching in: {subtitle_path}")  # Debugging line

            search_results += search_subtitles(subtitle_path, query, subtitle.language)
        print(f"Search Results: {search_results}")  # Debugging line

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # TODO For AJAX requests, return search results
        html = render_to_string('templates/search_results.html', {'search_results': search_results})
        return JsonResponse({'html': html})

    # For regular page requests, return the full page context
    context = {
        'video': video,
        'subtitles': subtitles,
        'form': form,
        'search_results': search_results
    }

    return render(request, 'templates/video_view.html', context)


def search_subtitles(subtitle_path, query, language):
    results = []
    timestamp_pattern = re.compile(r'(\d{2}:\d{2}:\d{2}[.,]\d{3})')  # Match SRT/VTT timestamps

    try:
        with open(subtitle_path, 'r', encoding='utf-8') as subtitle_file:
            content = subtitle_file.read().split('\n\n')  # Split on blank lines between subtitle blocks

            for block in content:
                if block.strip():
                    lines = block.split('\n')
                    if len(lines) >= 2 and query in block.lower():
                        # Extract timestamp
                        timestamp_match = timestamp_pattern.search(lines[1])
                        timestamp = timestamp_match.group(0) if timestamp_match else ''
                        # Extract subtitle text
                        subtitle_text = ' '.join(lines[2:]).strip()
                        results.append({
                            'text': subtitle_text,
                            'timestamp': timestamp,
                            'language': language
                        })
        return results
    except Exception as e:
        print(f"Error searching subtitle file: {e}")
        return []