from django.urls import path, include
# Project
from spoticode.tasks import views


urlpatterns = [
    path('all/', views.show_all_tasks, name='tasks_all'),
    path('create/', views.create_task, name='task_create'),
    
    path('<str:id>/', include([
        path('details/', views.show_details_task, name='task_details'),
        path('delete/', views.delete_task, name='task_delete'),
        path('edit/', views.edit_task, name='task_edit'),
        
        path('comment/', include([
            path('create/', views.create_task_comment, name='task_comment_create'),
            path('<str:c_id>/', include([
                path('details/', views.show_details_task_comment, name='task_comment_details'),
                path('delete/', views.delete_task_comment, name='task_comment_delete'),
                path('edit/', views.edit_task_comment, name='task_comment_edit'),
            ])),
        ])),
    ])),
]
