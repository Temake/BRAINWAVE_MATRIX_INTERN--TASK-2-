from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
import helpers
helpers.cloudinary_init()

class User(AbstractUser):
    email= models.EmailField(unique=True,blank=False, null=False)
    username= models.CharField(max_length=100,unique=True,blank=False, null=False)
    password= models.CharField(max_length=100,blank=False, null=False)

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
    
    
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    Category= models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True,related_name='categorys')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    img= CloudinaryField('images/',blank=True, null=True)
    author= models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(unique=True,default=None,null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            while Post.objects.filter(slug=self.slug).exists():
                original_slug = self.slug
                num = 1
                self.slug = f"{original_slug}-{num}"
                num += 1
        super().save(*args, **kwargs)
    def __str__(self):
        return f' {self.title} by {self.author}'
    @property
    def excerpt(self):
        return self.content[:100]
    @property
    def total_likes(self):
        return self.likes.count()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='likes')

    def __str__(self):
        return f"{self.user} likes {self.post}"
    
    class Meta:
        unique_together = ('user', 'post')

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"