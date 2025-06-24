from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import Post, Category
from .forms import PostCreateForm, PostUpdateForm



class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 3
    queryset = Post.published.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная страница"
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        return context


class PostFromCategory(ListView):
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    category = None
    paginate_by = 3
    
    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs["slug"])
        queryset = Post.published.filter(category__slug=self.category.slug)
        if not queryset:
            sub_cat = Category.objects.filter(parent=self.category)
            queryset = Post.published.filter(category__in=sub_cat)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Записи из категории: {self.category.title}"
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Представление для создания материалов на сайте"""
    
    model = Post
    template_name = "blog/post_create.html"
    form_class = PostCreateForm
    login_url = "home"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавление статьи на сайт"
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Представление для обновления материала на сайте"""
    
    model = Post
    template_name = "blog/post_update.html"
    context_object_name = "post"
    form_class = PostUpdateForm
    login_url = "home"
    success_message = "Запись была успешно обновлена!"
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Обновление статьи: {self.object.title}"
        return context
    
    def form_valid(self, form):
        form.instance.updater = self.request.user
        return super().form_valid(form)
