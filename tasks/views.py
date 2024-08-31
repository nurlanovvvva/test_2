
from django.views.generic import ListView, DetailView, CreateView
from .models import Task, Category
from .forms import TaskForm
from django.urls import reverse_lazy
from django.db.models import Q


class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category')
        search_query = self.request.GET.get('q')

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task-list')
