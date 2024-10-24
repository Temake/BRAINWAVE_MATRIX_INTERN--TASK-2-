from django.urls import path
from .views import *

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('create/',PostCreateView.as_view(),name='create'),
    path('register/',RegisterView,name='signup'),
    path('login/',LoginView,name='login'),
    path('logout/',LogoutView,name='logout'),
    path('explore/',ExploreView.as_view(),name='explore'),
    path('<str:slug>/comment/',post_comment,name='comment'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(),name='update'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name='delete'),
    path('detail/<str:slug>/',PostDetailView.as_view(),name='detail'),
    path('like/<int:post_id>/', like_post, name='like_post'),
    path('dashboard/',dashboard,name='dashboard'),
]