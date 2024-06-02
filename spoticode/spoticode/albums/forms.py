from django import forms
# Project
from spoticode.albums.models import Album, AlbumLink, AlbumTrack


# Albums 
class CreateAlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = ('album_id', )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['release_date'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'YYYY-MM-DD'})
        self.fields['album_artist'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['album_name'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['album_type'].widget.attrs.update({'class': 'form-select mb-4'})


class EditAlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = ('album_id', )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['release_date'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'YYYY-MM-DD'})
        self.fields['album_artist'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['album_name'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['album_type'].widget.attrs.update({'class': 'form-select mb-4'})


class EditAlbumLinkForm(forms.ModelForm):
    wiki_curid = forms.CharField(label='Wikipedia ID', required=False)

    class Meta:
        model = AlbumLink
        fields = ('spotify_link', 'wiki_curid', 'rateyourmusic_link')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['spotify_link'].widget.attrs.update({'class': 'form-control mb-3','placeholder': 'https://open.spotify.com/album/...'})
        self.fields['wiki_curid'].widget.attrs.update({'class': 'form-control mb-3','placeholder': '123...'})
        self.fields['rateyourmusic_link'].widget.attrs.update({'class': 'form-control mb-4','placeholder': 'https://rateyourmusic.com/release/album/...'})
        
        if self.instance and self.instance.wikipedia_link:
            self.initial['wiki_curid'] = self.instance.wikipedia_link.split('=')[1]
        
    def clean(self):
        cleaned_data = super().clean()
        spotify_link = cleaned_data.get('spotify_link')
        wiki_curid = cleaned_data.get("wiki_curid")
        rateyourmusic_link = cleaned_data.get('rateyourmusic_link')

        if not spotify_link:
            self.cleaned_data['spotify_link'] = None
        if not wiki_curid:
            self.cleaned_data['wiki_curid'] = None
            self.cleaned_data['wikipedia_link'] = None
        if not rateyourmusic_link:
            self.cleaned_data['rateyourmusic_link'] = None

        return cleaned_data



# Album Tracks
class CreateAlbumTrackForm(forms.ModelForm):
    class Meta:
        model = AlbumTrack
        exclude = ('track_id', 'album_id')
    
    def __init__(self, *args, **kwargs):
        album_id = kwargs.pop('album_id', None) 
        super().__init__(*args, **kwargs)
        self.album_id = album_id
        self.fields['track_num'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': '1, 2, ...'})
        self.fields['track_name'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['feat_artist'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['song_id'].widget.attrs.update({'class': 'form-select mb-4'})
    
    def clean(self):
        cleaned_data = super().clean()
        album_id = cleaned_data.get('album_id')
        track_num = cleaned_data.get('track_num')
        track_name = cleaned_data.get('track_name')

        if AlbumTrack.objects.filter(album_id=album_id, track_num=track_num).exists():
            raise forms.ValidationError('Track with such number already exists.')
        elif AlbumTrack.objects.filter(album_id=album_id, track_name=track_name).exists():
            raise forms.ValidationError('Track with such name already exists.')

        return cleaned_data


class EditAlbumTrackForm(forms.ModelForm):
    class Meta:
        model = AlbumTrack
        exclude = ('album_id', )
    
    def __init__(self, *args, **kwargs):
        album_id = kwargs.pop('album_id', None) 
        super().__init__(*args, **kwargs)
        self.album_id = album_id
        self.fields['track_num'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': '1'})
        self.fields['track_name'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['feat_artist'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['song_id'].widget.attrs.update({'class': 'form-select mb-4'})
    
    def clean(self):
        cleaned_data = super().clean()
        album_id = cleaned_data.get('album_id')
        track_num = cleaned_data.get('track_num')
        track_name = cleaned_data.get('track_name')

        if AlbumTrack.objects.filter(album_id=album_id, track_num=track_num).exists():
            raise forms.ValidationError('Track with such number already exists.')
        elif AlbumTrack.objects.filter(album_id=album_id, track_name=track_name).exists():
            raise forms.ValidationError('Track with such name already exists.')

        return cleaned_data
