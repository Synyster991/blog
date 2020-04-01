from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.forms.utils import ErrorList
from django.utils import timezone
from .models import Post, Comment
from .form import comment_form
from random import sample


def home(request):
    last_six_posts = Post.objects.all().order_by('-id')[:6]
    all_posts = Post.objects.all()
    pks_of_posts = []

    for post in all_posts:
        pks_of_posts.append(post.pk)

    random_one, random_two, random_three = sample(pks_of_posts, 3)
    popular_posts = [Post.objects.get(pk=random_one), Post.objects.get(pk=random_two), Post.objects.get(pk=random_three)]

    passing_dict = {
        'last_six_posts': last_six_posts,
        'popular_posts': popular_posts
    }
    return render(request, 'blog/home.html', passing_dict)


@login_required(login_url="/login")
def dashboard(request):
    all_posts = Post.objects.all().order_by('-id')
    current_user = request.user

    passing_dict = {
        'all_posts': all_posts,
        'current_user': current_user
    }
    return render(request, 'blog/dashboard.html', passing_dict)


def about(request):
    return render(request, 'blog/about.html')


# Detail Post
def detail_post(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post)

    passing_dict = {
        'post': post,
        'comments': comments
    }
    return render(request, 'blog/detail_post.html', passing_dict)


# Adding comment to post
@login_required(login_url="/login")
def add_comment(request, pk):
    add_comment = comment_form()

    post = Post.objects.get(pk=pk)

    if request.method == 'POST':
        add_comment = comment_form(request.POST)

        if add_comment.is_valid():
            new_comment = Comment()
            new_comment.body = add_comment.cleaned_data['body']
            new_comment.user = request.user
            new_comment.post = post
            new_comment.save()

            return redirect('detail_post', pk)
        else:
            errors = new_comment._errors.setdefault('body', ErrorList())
            errors.append('Invalid data entry.')

    passing_dict = {
        'add_comment': add_comment
    }
    return render(request, 'blog/add_comment.html', passing_dict)
    


# AUTH
class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/sign_up.html'


# Create Post
class create_post(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['title', 'body']
    template_name = 'blog/create_post.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.time = timezone.datetime.now()
        super(create_post, self).form_valid(form)

        return redirect('dashboard')


class delete_post(LoginRequiredMixin, generic.DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        post = super(delete_post, self).get_object()
        if post.user != self.request.user:
            raise Http404
        else:
            return post



