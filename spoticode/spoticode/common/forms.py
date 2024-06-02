from django import forms
# Project
from spoticode.common.models import MusicGroup, Genre


# Music Groups
class CreateMusicGroupForm(forms.ModelForm):
    class Meta:
        model = MusicGroup
        fields = ('group_name', )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group_name'].widget.attrs.update({'class': 'form-control mb-4'})


class EditMusicGroupForm(forms.ModelForm):
    class Meta:
        model = MusicGroup
        fields = ('group_name', )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group_name'].widget.attrs.update({'class': 'form-control mb-4'})



# Genres
class CreateGenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ('genre_name', 'description')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genre_name'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['description'].widget.attrs.update({'class': 'form-control mb-4'})


class EditGenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ('genre_name', 'description')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genre_name'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['description'].widget.attrs.update({'class': 'form-control mb-4'})
