from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Post(models.Model):
    description = models.CharField(max_length=255, blank=True)
    pic = models.ImageField(upload_to='posts/%Y/%m/%d/')  # Better organized storage
    date_posted = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Renamed from user_name
    tags = models.CharField(max_length=100, blank=True)
    likes_count = models.PositiveIntegerField(default=0)  # Added for performance

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def update_likes_count(self):
        """Helper method to update likes count"""
        self.likes_count = self.likes.count()
        self.save()

class Comment(models.Model):  # Changed from Comments to Comment
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)  # Changed from CharField to TextField
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Added to track edits

    class Meta:
        ordering = ['-created_at']  # Newest comments first

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post}"

class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Added timestamp

    class Meta:
        unique_together = ('user', 'post')  # Prevent duplicate likes

    def __str__(self):
        return f"{self.user.username} likes {self.post}"

    def save(self, *args, **kwargs):
        """Override save to update likes count"""
        super().save(*args, **kwargs)
        self.post.update_likes_count()

    def delete(self, *args, **kwargs):
        """Override delete to update likes count"""
        post = self.post
        super().delete(*args, **kwargs)
        post.update_likes_count()