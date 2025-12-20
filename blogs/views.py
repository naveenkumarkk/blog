from django.shortcuts import render
from django.http import HttpResponse
from .models import Blog


# Create your views here.
def posts_by_category(request, category_id):
    # Fetch the posts that belongs to the category with the id category_id
    posts = Blog.objects.filter(status='Published',category_id=category_id)
    return HttpResponse("Posts By Category")
