from django import forms
# Project
from spoticode.songs.models import Song, PendingSong
from spoticode.playlists.models import Playlist


# Songs
class CreateSongForm(forms.ModelForm):
    class Meta:
        model = Song
        exclude = ('song_id', )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['song_title'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['main_artist'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['feat_artist'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['genre'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['song_year'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'YYYY'})
        self.fields['group'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['album_id'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['spotify_link'].widget.attrs.update({'class': 'form-control mb-4', 'placeholder': 'https://open.spotify.com/track/...',})


class EditSongForm(forms.ModelForm):
    class Meta:
        model = Song
        exclude = ('song_id', )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['song_title'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['main_artist'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['feat_artist'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['genre'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['song_year'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'YYYY'})
        self.fields['group'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['album_id'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['spotify_link'].widget.attrs.update({'class': 'form-control mb-4'})


class AddSongToPlaylistForm(forms.Form):
    playlist = forms.ModelChoiceField(queryset=Playlist.objects.all(), label='Select Playlist')
    
    def __init__(self, *args, **kwargs):
        song_id = kwargs.pop('song_id', None)
        super().__init__(*args, **kwargs)
        self.fields['playlist'].widget.attrs.update({'class': 'form-select mb-4'})
        
        if song_id:
            self.fields['playlist'].queryset = Playlist.objects.exclude(songplaylistrelation__song_id=song_id)



# Pending Songs
class CreatePendingSongForm(forms.ModelForm):
    class Meta:
        model = PendingSong
        fields = ('song_title', 'main_artist', 'feat_artist', 'to_group')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['song_title'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['main_artist'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['feat_artist'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['to_group'].widget.attrs.update({'class': 'form-select mb-4'})


class EditPendingSongForm(forms.ModelForm):
    class Meta:
        model = PendingSong
        fields = ('song_title', 'main_artist', 'feat_artist', 'to_group')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['song_title'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['main_artist'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['feat_artist'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['to_group'].widget.attrs.update({'class': 'form-select mb-4'})
