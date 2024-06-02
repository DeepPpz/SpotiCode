from datetime import datetime
# Django
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
# Project
from spoticode.tasks.models import Task, TaskComment
from spoticode.tasks.forms import CreateTaskForm, EditTaskForm, CreateTaskCommentForm, EditTaskCommentForm
from spoticode.web.access_validators import custom_login_required, can_create_or_update, can_delete, can_read
from spoticode.web.access_checkers import can_create_checker, can_edit_checker, can_delete_checker


# Tasks
@custom_login_required
@can_read
def show_all_tasks(request):
    tasks = Task.objects.all()
    query = request.GET.get('query')
    
    if query:
        tasks = Task.objects.filter(task_name__icontains=query) | \
            Task.objects.filter(description__icontains=query) | \
                Task.objects.filter(status__icontains=query) | \
                    Task.objects.filter(responsible__username__icontains=query)
    
    tasks = tasks.order_by('date_created', 'last_modified')
    
    paginator = Paginator(tasks, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'curr_year': datetime.now().year,
        'tasks': tasks,
        'total_active_tasks': tasks.filter(date_closed__isnull=True).count(),
        'page_obj': page_obj,
        'can_create_check': can_create_checker(request.user),
    }
    
    return render(request, 'tasks/tasks-all.html', context)


@custom_login_required
@can_read
def show_details_task(request, id):
    task = get_object_or_404(Task, task_id=id)
    task_comments = TaskComment.objects.filter(task_id=id).order_by('date_added')
    
    context = {
        'curr_year': datetime.now().year,
        'task': task,
        'task_comments': task_comments,
        'can_create_check': can_create_checker(request.user),
        'can_edit_check': can_edit_checker(request.user),
        'can_delete_check': can_delete_checker(request.user),
    }
    
    return render(request, 'tasks/task-details.html', context)


@custom_login_required
@can_create_or_update
def create_task(request):
    form = CreateTaskForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        task = form.save()
        return redirect('task_details', id=task.task_id)

    context = {
        'curr_year': datetime.now().year,
        'form': form,
    }

    return render(request, 'tasks/task-create.html', context)


@custom_login_required
@can_create_or_update
def edit_task(request, id):
    task = get_object_or_404(Task, task_id=id)
    form = EditTaskForm(request.POST or None, instance=task)
    
    if request.method == 'POST' and form.is_valid():
        task = form.save()
        return redirect('task_details', id=task.task_id)
    
    context = {
        'curr_year': datetime.now().year,
        'task': task,
        'form': form,
    }
    
    return render(request, 'tasks/task-edit.html', context)


@custom_login_required
@can_delete
def delete_task(request, id):
    task = get_object_or_404(Task, task_id=id)
    
    if request.method == 'POST':
        task.delete()
        return redirect('tasks_all')

    context = {
        'curr_year': datetime.now().year,
        'task': task,
    }
    
    return render(request, 'tasks/task-delete.html', context)



# Task Comments
@custom_login_required
@can_read
def show_details_task_comment(request, id, c_id):
    task = get_object_or_404(Task, task_id=id)
    task_comment = get_object_or_404(TaskComment, comment_id=c_id)
    
    context = {
        'curr_year': datetime.now().year,
        'task': task,
        'task_comment': task_comment,
        'can_edit_check': can_edit_checker(request.user),
        'can_delete_check': can_delete_checker(request.user),
    }
    
    return render(request, 'tasks/comments/task-comment-details.html', context)


@custom_login_required
@can_create_or_update
def create_task_comment(request, id):
    task = get_object_or_404(Task, task_id=id)
    form = CreateTaskCommentForm(request.POST or None, task_id=task.task_id)
    
    if request.method == 'POST' and form.is_valid():
        task_comment = form.save(commit=False)
        task_comment.task_id = task
        task_comment.user = request.user
        task_comment.save()
        return redirect('task_details', id=task.task_id)

    context = {
        'curr_year': datetime.now().year,
        'form': form,
        'task': task,
    }

    return render(request, 'tasks/comments/task-comment-create.html', context)


@custom_login_required
@can_create_or_update
def edit_task_comment(request, id, c_id):
    task = get_object_or_404(Task, task_id=id)
    task_comment = get_object_or_404(TaskComment, comment_id=c_id)
    form = EditTaskCommentForm(request.POST or None, instance=task_comment)
    
    if request.method == 'POST' and form.is_valid():
        task_comment = form.save()
        return redirect('task_details', id=task.task_id)
    
    context = {
        'curr_year': datetime.now().year,
        'task': task,
        'task_comment': task_comment,
        'form': form,
    }
    
    return render(request, 'tasks/comments/task-comment-edit.html', context)


@custom_login_required
@can_delete
def delete_task_comment(request, id, c_id):
    task = get_object_or_404(Task, task_id=id)
    task_comment = get_object_or_404(TaskComment, comment_id=c_id)
    
    if request.method == 'POST':
        task_comment.delete()
        return redirect('task_details', id=task.task_id)

    context = {
        'curr_year': datetime.now().year,
        'task': task,
        'task_comment': task_comment,
    }
    
    return render(request, 'tasks/comments/task-comment-delete.html', context)
