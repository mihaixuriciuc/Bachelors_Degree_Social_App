from django.db import models
from config import settings
from apps.posts.helpers import user_directory_path

# Create your models here.

class Post(models.Model):
    # Link to the user, the one who created the post
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    # Content
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)#upload to already has instance and filename


    # Metadata for bot detection
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author.username}-{self.title}"


class Like(models.Model):
    #the one who created the like
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('author', 'post')
        ordering = ['-created_at'] #shows the list of likes in descending order





class Comment(models.Model):
    #the one who commented
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    """
    to understan more clearly, here i can acces both comments from the author and vice versa
    
    example:
    post.comments.all() gets all the comments from one post
    
    comment.post gets tge post of that comment, there is only one anyway
    
    """