from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from .models import Blog, Category, Comment
from django.db.models import Q  # to use the complex operations as such OR operations
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET,require_POST
from django.utils.timesince import timesince
from django.utils import timezone
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

@require_GET
def load_comments(request,blog_id):
    page = int(request.GET.get("page",1))
    blog = Blog.objects.get(id=blog_id)
    comment_qs = Comment.objects.filter(blog=blog).order_by("-created_at")
    paginator = Paginator(comment_qs,3)
    comments = paginator.get_page(page)
    context = {
        "comments":[
            {
                "text":c.comment,
                "created_at": timesince(c.created_at,timezone.now())
            }
            for c in comments
        ],
        "has_next":comments.has_next()
    }
    return JsonResponse(context)

@require_POST
def add_comment(request,blog_id):
    blog = Blog.objects.get(id=blog_id)
    text = request.POST.get("comment")
    print(text)
    if not text.strip():
        return JsonResponse({"error":"Empty Comment"},status=400)

    comment = Comment.objects.create(
        blog = blog,
        # user=request.user,
        comment=text
    )
    return JsonResponse({
        "text":comment.comment,
        "created_at": timesince(comment.created_at,timezone.now())
    })

def blogs(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status="Published")
    # Comments
    context = {"single_blog": single_blog }
    return render(request, "blogs.html", context)


def search(request):
    keyword = request.GET.get("keyword")
    blog = Blog.objects.filter(
        Q(title__icontains=keyword)
        | Q(short_description__icontains=keyword)
        | Q(blog_body__icontains=keyword),
        status="Published",
    )
    context = {"blogs": blog, "keyword": keyword}
    return render(request, "search.html", context)
