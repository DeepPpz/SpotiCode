from django import forms
# Project
from spoticode.tasks.models import Task, TaskComment


# Tasks 
class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('task_id', 'date_created', 'last_modified', 'date_closed')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['task_name'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['related_app'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['responsible'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['status'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['priority'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['task_type'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['description'].widget.attrs.update({'class': 'form-control mb-4'})


class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('task_id', 'date_created', 'last_modified', 'date_closed')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['task_name'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['related_app'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['responsible'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['status'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['priority'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['task_type'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['description'].widget.attrs.update({'class': 'form-control mb-4'})



# Task Comments
class CreateTaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ('comment_text',)
    
    def __init__(self, *args, **kwargs):
        task_id = kwargs.pop('task_id', None) 
        super().__init__(*args, **kwargs)
        self.task_id = task_id
        self.fields['comment_text'].widget.attrs.update({'class': 'form-control mb-4'})


class EditTaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ('comment_text', 'user')
    
    def __init__(self, *args, **kwargs):
        task_id = kwargs.pop('task_id', None) 
        super().__init__(*args, **kwargs)
        self.task_id = task_id
        self.fields['comment_text'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['user'].widget.attrs.update({'class': 'form-select mb-4'})
