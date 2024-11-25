import random, string
from datetime import datetime
# Django
from django.contrib import admin
# Project
from spoticode.tasks.models import Task, TaskComment
from spoticode.tasks.models_choices import get_default_user
# Other
from django_admin_listfilter_dropdown.filters import DropdownFilter


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'task_name', 'formatted_date_created', 'task_type','priority', 'related_app', 'responsible', 'status')
    search_fields = ('task_name', 'description')
    list_filter = (
        ('related_app', DropdownFilter),
        ('responsible__username', DropdownFilter),
        ('status', DropdownFilter),
        ('priority', DropdownFilter),
        ('task_type', DropdownFilter),
    )
    
    def formatted_date_created(self, obj):
        return obj.date_created.date()
    formatted_date_created.short_description = 'Date Created'
    
    def responsible(self, obj):
        return obj.responsible.username if obj.responsible else '--none--'
    
    def get_exclude(self, request, obj=None):
        if obj is None:
            return ['task_id', 'last_modified']
        return []

    def save_model(self, request, obj, form, change):
        if not obj.task_id:
            random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
            while Task.objects.filter(task_id=random_part).exists():
                random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
            obj.task_id = random_part
            print(obj.task_id)
            
            if not obj.date_created:
                obj.date_created = datetime.now()
                
        super().save_model(request, obj, form, change)
        

@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ('comment_id', 'formatted_date_added', 'user', 'task', 'comment_text')
    search_fields = ('comment_text',)
    list_filter = (
        ('user__username', DropdownFilter),
        ('task_id__task_name', DropdownFilter),
    )
    
    def user(self, obj):
        return obj.user.username if obj.user else None
    
    def task(self, obj):
        return obj.task_id.task_name if obj.task_id else None
    
    def formatted_date_added(self, obj):
        return obj.date_added.date()
    formatted_date_added.short_description = 'Date Created'
    
    def get_exclude(self, request, obj=None):
        if obj is None:
            return ['comment_id', 'user', 'date_added']
        return []

    def save_model(self, request, obj, form, change):
        if not obj.comment_id:
            random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            while TaskComment.objects.filter(comment_id=random_part).exists():
                random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            obj.comment_id = random_part
        
        try:
            obj.user = request.user
        except AttributeError:
            obj.user = get_default_user()
            
        super().save_model(request, obj, form, change)
