from operator import truediv
from turtle import title, update
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Task

from django.views.generic.edit import CreateView,UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView 

#user login system
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True #if the user is authenticated then don't keep in this page

    #redirects the user to the home page after login
    def get_success_url(self):
        return reverse_lazy('tasks')


#views the set of tasks
class TaskList(ListView):
    model = Task
    context_object_name = 'tasks'


#views the tasks in detail
class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


#create new task
class TaskCreate(CreateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks') #redirects the page to the initial page after adding a task


#update a task
class TaskUpdate(UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks') 


#delete a specific task
class DeleteView(DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks') 
