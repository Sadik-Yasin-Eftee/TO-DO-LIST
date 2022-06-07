from asyncio import tasks
from atexit import register
from multiprocessing import context
from operator import truediv
from turtle import title, update
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


import base

from .models import Task

from django.views.generic.edit import CreateView,UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView 
from django.contrib.auth.mixins import LoginRequiredMixin #used for restricting user to see the tasks before login
from django.contrib.auth.forms import UserCreationForm #django provides form
from django.contrib.auth import login #user don't have to login again. they will be logged in 

#user login system
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True #if the user is authenticated then don't keep in this page

    #redirects the user to the home page after login
    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm #django pre-built form is generated and this form is to be submitted
    redirect_authenticated_user = True #if the user is authenticated then don't keep in this page
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save() #create the user using form  
        if user is not None: #if the user has been validated/registered redirect to the login page
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)


    #the below funtion is used so that the user cannot enter register and login page while he is logged in
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated: #if user is authenticated then redirect to home-page
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs) #else redirect to register page



#views the set of tasks
class TaskList(LoginRequiredMixin , ListView): #LoginRequiredMixin is used to restrict the user
    model = Task
    context_object_name = 'tasks'

    #this part is done so that the user can only see his own data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) #kwargs = key word argument
        context['tasks'] = context['tasks'].filter(user = self.request.user) #making sure that the datas/context of the user are restricted to that user only
        context['count'] = context['tasks'].filter(complete = False).count() #counting the number of task not done. no need to filter here as the filtering has been done in the upper section #provides query set 
                                                        
        search_input = self.request.GET.get('search-area') or '' #blank space if required results aren't met in search
        
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith = search_input) #search funtion added.This part includes the search logic
        
        context['search_input'] = search_input
        return context


#views the tasks in detail
class TaskDetail(LoginRequiredMixin , DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


#create new task
class TaskCreate(LoginRequiredMixin , CreateView):
    model = Task
    fields = ['title' , 'description' , 'complete']
    success_url = reverse_lazy('tasks') #redirects the page to the initial page after adding a task

    def form_valid(self, form):
        form.instance.user = self.request.user #makes sure that the forms filled up is added to that users database
        return super(TaskCreate, self).form_valid(form)


#update a task
class TaskUpdate(LoginRequiredMixin , UpdateView):
    model = Task
    fields = ['title' , 'description' , 'complete']
    success_url = reverse_lazy('tasks') 


#delete a specific task
class DeleteView(LoginRequiredMixin , DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks') 
