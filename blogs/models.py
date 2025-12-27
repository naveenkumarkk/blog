from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Django always displays the model name in plural ,
    # so we can change the spelling if needed by using the following Class
    class Meta:
        verbose_name_plural = "categories"

    # Set the string represenation of the category model
    # This is used to display the catgory name instead of displaying as the object in the dashboard
    def __str__(self):
        return self.category_name


BLOG_STATUS_CHOICES = (("Draft", "Draft"), ("Published", "Published"))


class Blog(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    feature_image = models.ImageField(upload_to="uploads/%Y/%m/%d")
    short_description = models.TextField(max_length=500)
    blog_body = models.TextField(max_length=4000)
    # Staus needs to be dropdown
    status = models.CharField(
        max_length=20, choices=BLOG_STATUS_CHOICES, default="Draft"
    )
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


LINK_STATUS = (
    ("Active", "Active"),
    ("InActive", "InActive"),
)


class SocialMedia(models.Model):
    name = models.CharField(max_length=20, unique=True, blank=False)
    link = models.URLField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=LINK_STATUS, default="Active")

    def __str__(self):
        return self.name


class About(models.Model):
    description = models.TextField(max_length=700)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment


class NewsLetterUser(models.Model):
    NEWSLETTER_USER_STATUS = (
        ("Subscribed", "Subscribed"),
        ("UnSubscribed", "UnSubscribed"),
    )
    email = models.EmailField(unique=True)
    status = models.CharField(
        max_length=15, choices=NEWSLETTER_USER_STATUS, default="Subscribed"
    )
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class NewsLetter(models.Model):

    STATUS_CHOICES = (("Draft", "Draft"), ("Published", "Published"), ("Sent", "Sent"))

    body = models.TextField()
    subject = models.CharField(max_length=255)
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default="Draft"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class NewsLetterMail(models.Model):
    EMAIL_STATUS_CHOICES = (("Pending", "Pending"),("Success", "Success"), ("Failed", "Failed"))
    newsletter = models.ForeignKey(NewsLetter, on_delete=models.CASCADE,related_name="mail_log")
    subscriber = models.ForeignKey(NewsLetterUser, on_delete=models.CASCADE,related_name="mail_logs")
    status = models.CharField(max_length=15, choices=EMAIL_STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("newsletter", "subscriber")
    
    def __str__(self):
        return f"{self.newletter.subject} -> {self.subscriber.email}"
    