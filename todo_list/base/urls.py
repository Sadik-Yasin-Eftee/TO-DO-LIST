from unicodedata import name
from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView
from .views import CustomLoginView, RegisterPage

from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', CustomLoginView.as_view() , name = 'login'),
    path('logout/', LogoutView.as_view(next_page = 'login') , name = 'logout'), #redirects to the login page by the as_view part
    path('register/', RegisterPage.as_view() , name = 'register'),
    path('', TaskList.as_view() , name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name ='task'),
    path('create-task/', TaskCreate.as_view(), name = 'create-task'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name ='task-update'),
    path('task-delete/<int:pk>/', DeleteView.as_view(), name ='task-delete')
]