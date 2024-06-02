import random, string
from datetime import datetime
# Django
from django.db import models
from django.contrib.auth.models import User
# Project
from spoticode.tasks.models_choices import get_app_choices, get_default_user


class Task(models.Model):
    TASK_TYPES = {
        'Bug': 'Bug',
        'Cleanup': 'Cleanup',
        'Feature': 'Feature',
        'Data Error': 'Data Error',
        'Other': 'Other',
    }
    
    STATUSES = {
        'Not Started': 'Not Started',
        'In Progress': 'In Progress',
        'Needs Assistance': 'Needs Assistance',
        'Issues Found': 'Issues Found',
        'On Hold': 'On Hold',
        'For Testing': 'For Testing',
        'Cancelled': 'Cancelled',
        'Completed': 'Completed',
    }
    
    PRIORITIES = {
        'Urgent': 'Urgent',
        'High': 'High',
        'Normal': 'Normal',
        'Low': 'Low',
    }
    
    task_id = models.CharField(primary_key=True, blank=True, 
                               db_column='task_id', verbose_name='Task ID')
    date_created = models.DateTimeField(auto_now_add=True, blank=True, 
                                        db_column='date_created', verbose_name='Date Created')
    last_modified = models.DateTimeField(auto_now=True, blank=True, 
                                         db_column='last_modified', verbose_name='Last Modified')
    date_closed = models.DateTimeField(null=True, blank=True, 
                                       db_column='date_closed', verbose_name='Date Closed')
    task_name = models.CharField(max_length=50, 
                                 db_column='task_name', verbose_name='Task Name')
    related_app = models.CharField(choices=get_app_choices(), default='Administration', 
                                   db_column='related_app', verbose_name='Related App')
    responsible = models.ForeignKey(User, to_field='username', on_delete=models.SET_NULL, 
                                    null=True, blank=True, 
                                    db_column='responsible', verbose_name='Responsible')
    status = models.CharField(choices=STATUSES, default='Not Started', 
                              db_column='status', verbose_name='Status')
    priority = models.CharField(choices=PRIORITIES, default='Normal', 
                                db_column='priority', verbose_name='Priority')
    task_type = models.CharField(choices=TASK_TYPES, default='Bug', 
                                 db_column='task_type', verbose_name='Task Type')
    description = models.TextField(db_column='description', verbose_name='Description')
    
    def __str__(self):
        return self.task_name
    
    def save(self, *args, **kwargs):
        if not self.task_id:
            random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
            while Task.objects.filter(task_id=random_part).exists():
                random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
            self.task_id = random_part
            
            if not self.date_created:
                self.date_created = datetime.now()
        
        else:
            try:
                old = Task.objects.get(task_id=self.task_id)
                if old.status not in ['Cancelled', 'Completed'] and self.status in ['Cancelled', 'Completed']:
                    self.date_closed = datetime.now()
                
                if self.status not in ['Cancelled', 'Completed']:
                    self.date_closed = None
            except Task.DoesNotExist:
                pass
        
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'tasks'
        unique_together = ('task_name', 'related_app', 'task_type')
        ordering = ('priority', 'date_created')
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'


class TaskComment(models.Model):
    comment_id = models.CharField(primary_key=True, blank=True, 
                                  db_column='comment_id', verbose_name='Comment ID')
    comment_text = models.TextField(db_column='comment_text', verbose_name='Comment')
    user = models.ForeignKey(User, to_field='username', on_delete=models.SET(get_default_user), 
                             blank=True, 
                             db_column='user', verbose_name='User')
    date_added = models.DateTimeField(auto_now_add=True, blank=True, 
                                      db_column='date_added', verbose_name='Date Added')
    task_id = models.ForeignKey(Task, to_field='task_id', on_delete=models.CASCADE, 
                                blank=True, 
                                db_column='task_id', verbose_name='Task')

    def save(self, *args, **kwargs):
        if not self.comment_id:
            random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            while TaskComment.objects.filter(comment_id=random_part).exists():
                random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            self.comment_id = random_part
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'task_comments'
        unique_together = ('comment_text', 'task_id')
        ordering = ('task_id', 'date_added')
        verbose_name = 'Task Comment'
        verbose_name_plural = 'Task Comments'
