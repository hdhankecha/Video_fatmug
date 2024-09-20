from django import forms
from .models import Video

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_file']


class SearchForm(forms.Form):
    query = forms.CharField(max_length=255, required=True)