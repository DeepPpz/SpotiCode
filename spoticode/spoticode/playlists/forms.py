from django import forms
# Project
from spoticode.playlists.models import Playlist


class CreatePlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ('playlist_name', 'playlist_link', 'playlist_image', 'notes')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['playlist_name'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['playlist_link'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'https://open.spotify.com/playlist/...',})
        self.fields['playlist_image'].widget.attrs.update({'class': 'form-control bg-dark mb-3'})
        self.fields['notes'].widget.attrs.update({'class': 'form-control mb-4'})
        self.fields['playlist_name'].help_text = ''


class EditPlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ('playlist_name', 'playlist_link', 'playlist_image', 'notes')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['playlist_name'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['playlist_link'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'https://open.spotify.com/playlist/...',})
        self.fields['playlist_image'].widget.attrs.update({'class': 'form-control bg-dark mb-3'})
        self.fields['notes'].widget.attrs.update({'class': 'form-control mb-4'})


class SongsSearchForm(forms.Form):
    artist = forms.CharField(required=False, label='Artist')
    from_year = forms.IntegerField(required=False, label='From Year')
    to_year = forms.IntegerField(required=False, label='To Year')
    genre = forms.CharField(required=False, label='Genre')
    group = forms.CharField(required=False, label='Group')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['artist'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['from_year'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['to_year'].widget.attrs.update({'class': 'form-control bg-dark mb-3'})
        self.fields['genre'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['group'].widget.attrs.update({'class': 'form-control mb-4'})
