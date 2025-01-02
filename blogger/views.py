from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404,HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from .models import *
from django.views.generic import TemplateView,CreateView,UpdateView,DeleteView,DetailView,ListView
from .forms import CommentForm


# Create your views here.
class HomeView(TemplateView):
    template_name = 'blogger/home.html'
    
class ExploreView(ListView):
    model = Post
    template_name = 'blogger/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 9 
    
    
class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content','img','Category']
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super(self,PostCreateView).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  
        return context


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    success_url = reverse_lazy('dashboard')
    fields = ['title','content','img','Category']
    
 
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  
        return context

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

        
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('dashboard')
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post
    template_name = 'blogger/post_detail.html'
    def post_detail(request, slug):
        post = get_object_or_404(Post,slug=slug)
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect('detail', slug=post.slug)
        else:
            form = CommentForm()

def RegisterView(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username,email,password)
        user.save()
        return render(request,'login.html')
    else:
        return render(request,'signup.html')

def LoginView(request):
    if request.method == 'POST':
        user_input = request.POST['username'] 
        password = request.POST['password']

     
        if '@' in user_input:
            try:
                
                user = User.objects.get(email=user_input)
                username = user.username  # Get the associated username
            except User.DoesNotExist:
                user = None
        else:
            username = user_input  # Assume input is a username
        
    
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  
        else:
            return render(request, 'login.html', {'error': 'Invalid username/email or password'})

    return render(request, 'login.html')
def LogoutView(request):
    
    return render(request,'login.html')

@login_required
def dashboard(request):
    user_posts = Post.objects.filter(author=request.user) 
    return render(request,'blogger/dashboard.html',{'user_posts':user_posts})
@login_required
def post_comment(request, slug):
        post = get_object_or_404(Post,slug=slug)
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect('detail', slug=post.slug)
        else:
            form = CommentForm()
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    post_id=Post.objects.get(id=post_id)
    

    if not created:
        # If the like already exists, remove it (unlike).
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({'liked': liked, 'total_likes': post.total_likes})

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

