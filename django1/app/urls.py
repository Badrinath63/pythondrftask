"""django1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import LoginView, LogoutView, CreateUserView, ListUsersView, UpdateUserView, DeleteUserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('list/', ListUsersView.as_view(), name='list_users'),
    path('update/<int:user_id>/', UpdateUserView.as_view(), name='update_user'),
    path('delete/<int:user_id>/', DeleteUserView.as_view(), name='delete_user'),
]
