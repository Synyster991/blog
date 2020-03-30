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


def home(request):
    all_posts = Post.objects.all().order_by('-id')

    passing_dict = {
        'all_posts': all_posts
    }
    return render(request, 'blog/home.html', passing_dict)


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


