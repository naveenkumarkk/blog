from django.shortcuts import redirect, render,get_object_or_404
from django.http import HttpResponse
from .models import Blog,Category


# Create your views here.
def posts_by_category(request, category_id):
    # Fetch the posts that belongs to the category with the id category_id
    posts = Blog.objects.filter(status='Published',category=category_id)
    try:
        category = Category.objects.get(id=category_id)
    except:
        # Redirect the user to homepage
        return redirect('404.html')
    # To display the 404 error - default error page
    # category = get_object_or_404(Category,id=category_id)
    
    context = {
        "posts":posts,
        'category' : category
    }
    return render(request,'posts_by_category.html',context)

def blogs(request,slug):
    single_blog = get_object_or_404(Blog,slug=slug,status='Published')
    context = {
        'single_blog':single_blog,
    }
    return render(request,'blogs.html',context)
