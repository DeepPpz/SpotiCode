from django import forms
# Project
from spoticode.artists.models import Artist, ArtistLink


class CreateArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ('artist_id', 'artist_name', 'other_names')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['artist_id'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'must be all caps, 2-5 symbols abbreviation'})
        self.fields['artist_name'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['other_names'].widget.attrs.update({'class': 'form-control mb-4'})


class EditArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ('artist_id', 'artist_name', 'other_names')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['artist_id'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['artist_name'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['other_names'].widget.attrs.update({'class': 'form-control mb-4'})


class EditArtistLinkForm(forms.ModelForm):
    wiki_curid = forms.CharField(label='Wikipedia ID', required=False)

    class Meta:
        model = ArtistLink
        fields = ('official_website', 'spotify_link', 'wiki_curid')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['official_website'].widget.attrs.update({'class': 'form-control mb-3','placeholder': 'https://...'})
        self.fields['spotify_link'].widget.attrs.update({'class': 'form-control mb-3','placeholder': 'https://open.spotify.com/artist/...'})
        self.fields['wiki_curid'].widget.attrs.update({'class': 'form-control mb-4','placeholder': '123...'})
        
        if self.instance and self.instance.wikipedia_link:
            self.initial['wiki_curid'] = self.instance.wikipedia_link.split('=')[1]

    def clean(self):
        cleaned_data = super().clean()
        official_website = cleaned_data.get('official_website')
        spotify_link = cleaned_data.get('spotify_link')
        wiki_curid = cleaned_data.get("wiki_curid")

        if not official_website:
            self.cleaned_data['official_website'] = None
        if not spotify_link:
            self.cleaned_data['spotify_link'] = None
        if not wiki_curid:
            self.cleaned_data["wiki_curid"] = None

        return cleaned_data
