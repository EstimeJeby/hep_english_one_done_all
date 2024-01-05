
from typing import Any
from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404,redirect
from .models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy,reverse
from django.views.generic import RedirectView
from django.contrib import messages
from .forms import CommentForm ,CreatePost
import json

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View
)

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request,'blog/home.html',context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
   
    
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    

# class  LikePost(View):
#     def post(self,request):
#         post_id = request.POST.get('post_id')

#         print(post_id)

#         return JsonResponse('Like it is down there',safe=False)

def  PostLikeToggle(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data['id']
        action = data['action']
        print(action)
        post = Post.objects.get(id=id)
        if request.user.is_authenticated:
            if post.liked.filter(id=request.user.id).exists():
                post.liked.remove(request.user)
            
            else:
                post.liked.add(request.user)
           
    
    return JsonResponse('items add', safe=False)
   
          

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


def  PostCreateView(request):
    form = CreatePost()
    if request.method == 'POST':
        form=CreatePost(request.POST,request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            messages.success(request, f'A new Post has been created!')
            return redirect('blog-home')
        else:
            messages.info(request, f'error the Post is not created!')
            return redirect('post-create')

    context ={
        'form':form
    }

    return render(request,'blog/post_form.html',context)
    # model = Post
    # form_class= CreatePost
    # template_name = 'blog/post_form.html'
    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)


class AddComment(LoginRequiredMixin,CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/addComment.html'
    
    def form_valid(self,form):
        
        form.instance.post_id = self.kwargs['pk']
        form.instance.name = self.request.user
        return super().form_valid(form)
    
    success_url = reverse_lazy('blog-home')
    

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


