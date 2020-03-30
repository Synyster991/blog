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


def home(request):
    all_posts = Post.objects.all

    passing_dict = {
        'all_posts': all_posts
    }
    return render(request, 'blog/home.html', passing_dict)


# Detail Post
def detail_post(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post)
    print("POST")
    print(pk)
    print(post)
    print()
    print("COMMENT")
    print(comments)

    passing_dict = {
        'post': post,
        'comments': comments
    }
    return render(request, 'blog/detail_post.html', passing_dict)


# AUTH
class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/sign_up.html'


# Create Post
class create_post(generic.CreateView):
    model = Post
    fields = ['title', 'body']
    template_name = 'blog/create_post.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.time = timezone.datetime.now()
        super(create_post, self).form_valid(form)

        return redirect('home')


