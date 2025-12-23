from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from .models import Blog, Category
from django.db.models import Q  # to use the complex operations as such OR operations


# Create your views here.
def posts_by_category(request, category_id):
    # Fetch the posts that belongs to the category with the id category_id
    posts = Blog.objects.filter(status="Published", category=category_id)
    try:
        category = Category.objects.get(id=category_id)
    except:
        # Redirect the user to homepage
        return redirect("404.html")
    # To display the 404 error - default error page
    # category = get_object_or_404(Category,id=category_id)

    context = {"posts": posts, "category": category}
    return render(request, "posts_by_category.html", context)


def blogs(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status="Published")
    context = {
        "single_blog": single_blog,
    }
    return render(request, "blogs.html", context)


def search(request):
    keyword = request.GET.get("keyword")
    blog = Blog.objects.filter(
        Q(title__icontains=keyword)
        | Q(short_description__icontains=keyword)
        | Q(blog_body__icontains=keyword),
        status="Published",
    )
    context = {
        "blogs": blog,
        "keyword":keyword
        }
    return render(request, "search.html", context)
