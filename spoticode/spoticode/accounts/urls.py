from django.urls import path, include
# Project
from spoticode.accounts import views


urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='user_login'),
    path('logout/', views.CustomLogoutView.as_view(), name='user_logout'),
    path('register/', views.RegisterUserView.as_view(), name='user_register'),
   
    path('<int:id>/', include([
        path('first_login/', views.FirstLoginUserView.as_view(), name='user_first_login'),
        path('details/', views.ShowDetailsUserView.as_view(), name='user_details'),
        path('edit/', views.EditUserView.as_view(), name='user_edit'),
        path('password_change/', views.CustomPasswordChangeView.as_view(), name='user_password_change'),
    ])),
]
