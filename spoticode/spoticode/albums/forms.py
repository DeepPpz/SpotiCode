from django import forms
# Project
from spoticode.albums.models import Album, AlbumLink


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
        fields = ('spotify_link', 'wiki_curid')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['spotify_link'].widget.attrs.update({'class': 'form-control mb-3','placeholder': 'https://open.spotify.com/album/...'})
        self.fields['wiki_curid'].widget.attrs.update({'class': 'form-control mb-4','placeholder': '123...'})
        
        if self.instance and self.instance.wikipedia_link:
            self.initial['wiki_curid'] = self.instance.wikipedia_link.split('=')[1]
        
    def clean(self):
        cleaned_data = super().clean()
        spotify_link = cleaned_data.get('spotify_link')
        wiki_curid = cleaned_data.get("wiki_curid")

        if not spotify_link:
            self.cleaned_data['spotify_link'] = None
        if not wiki_curid:
            self.cleaned_data["wiki_curid"] = None
            self.cleaned_data["wikipedia_link"] = None

        return cleaned_data
