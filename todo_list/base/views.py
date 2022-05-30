from multiprocessing import context
from operator import truediv
from turtle import title, update
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Task

from django.views.generic.edit import CreateView,UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView 
from django.contrib.auth.mixins import LoginRequiredMixin #used for restricting user to see the tasks before login

#user login system
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True #if the user is authenticated then don't keep in this page

    #redirects the user to the home page after login
    def get_success_url(self):
        return reverse_lazy('tasks')


#views the set of tasks
class TaskList(LoginRequiredMixin , ListView): #LoginRequiredMixin is used to restrict the user
    model = Task
    context_object_name = 'tasks'

    #this part is done so that the user can only see his own data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) #kwargs = key word argument
        context['tasks'] = context['tasks'].filter(user = self.request.user) #making sure that the datas/context of the user are restricted to that user only
        context['count'] = context['tasks'].filter(complete = False).count() #counting the number of task not done. no need to filter here as the filtering has been done in the upper section
                                                                            #provides query set
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
