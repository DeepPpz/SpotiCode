from datetime import datetime
# Django
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User, Group
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
# Project
from spoticode.accounts.forms import RegisterUserForm, EditUserForm, PasswordChangeForm
from spoticode.accounts.mixins import LoginRequiredMixin, AdminRequiredMixin, UserCheckMixin


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.last_login is None:
                login(request, user)
                return redirect('user_first_login', id=user.id)
            else:
                login(request, user)
                return redirect('homepage')
        else:
            error_message = 'Your username or password is incorrect.'
            return redirect(f"{reverse('user_login')}?error={error_message}")
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curr_year'] = datetime.now().year
        context['error_message'] = self.request.GET.get('error', None)
        return context


class CustomLogoutView(LoginRequiredMixin, LogoutView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('homepage'))


class RegisterUserView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    template_name = 'accounts/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('homepage') 
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curr_year'] = datetime.now().year
        return context
    
    def form_valid(self, form):
        user = form.save()
        user.save()
        return super().form_valid(form)


class FirstLoginUserView(LoginRequiredMixin, UserCheckMixin, PasswordChangeView):
    template_name = 'accounts/first-login-user.html'
    form_class = PasswordChangeForm
    
    def get_object(self, queryset=None):
        return get_object_or_404(User, id=self.kwargs['id'])
    
    def get_success_url(self):
        return reverse_lazy('homepage')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.get_object()
        viewer_group, created = Group.objects.get_or_create(name='Viewer')
        user.groups.add(viewer_group)

        return response
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curr_year'] = datetime.now().year
        return context


class ShowDetailsUserView(LoginRequiredMixin, UserCheckMixin, DetailView):
    model = User
    template_name = 'accounts/details-user.html'
    
    def get_object(self, queryset=None):
        return get_object_or_404(User, id=self.kwargs['id'])
    
    def get_user_group(self):
        user = self.get_object()
        return user.groups.first() if user.groups.exists() else None
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curr_year'] = datetime.now().year
        context['user_group'] = self.get_user_group()
        return context


class EditUserView(LoginRequiredMixin, UserCheckMixin, UpdateView):
    template_name = 'accounts/edit-user.html'
    form_class = EditUserForm
    
    def get_object(self, queryset=None):
        return get_object_or_404(User, id=self.kwargs['id'])
    
    def get_success_url(self):
        return reverse('user_details', kwargs={'id': self.kwargs['id']})
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curr_year'] = datetime.now().year
        return context


class CustomPasswordChangeView(LoginRequiredMixin, UserCheckMixin, PasswordChangeView):
    template_name = 'accounts/password-change-user.html'
    form_class = PasswordChangeForm
    
    def get_object(self, queryset=None):
        return get_object_or_404(User, id=self.kwargs['id'])
    
    def get_success_url(self):
        return reverse_lazy('user_details', kwargs={'id': self.kwargs['id']})
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curr_year'] = datetime.now().year
        return context
