from django.shortcuts import get_object_or_404, redirect, render
from blogs.models import Blog, Category
from django.contrib.auth.decorators import login_required
from .forms import BlogPostForm, CategoryForm
from django.template.defaultfilters import slugify


@login_required(login_url="login")
# Create your views here.
def dashboard(request):
    category_count = Category.objects.all().count()
    blogs_count = Blog.objects.all().count()

    context = {"category_count": category_count, "blogs_count": blogs_count}
    return render(request, "dashboard/dashboard.html", context)


@login_required(login_url="login")
def categories(request):
    return render(request, "dashboard/categories.html")


@login_required(login_url="login")
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("categories")
    form = CategoryForm()
    context = {
        "form": form,
    }
    return render(request, "dashboard/add_category.html", context)


@login_required(login_url="login")
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("categories")
    form = CategoryForm(instance=category)
    context = {"form": form, "category": category}
    return render(request, "dashboard/edit_category.html", context)


@login_required(login_url="login")
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect("categories")


@login_required(login_url="login")
def post(request):
    posts = Blog.objects.all()
    context = {"posts": posts}
    return render(request, "dashboard/posts.html", context)


@login_required(login_url="login")
def add_post(request):
    if request.method == "POST":
        # request.FILES-> for all file types
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # Temporarily saving the form
            post.author = request.user
            post.save()
            title = form.cleaned_data["title"]
            post.slug = (
                slugify(title) + "-" + str(post.id)
            )  # we need to make the slug unique

            post.save()
            return redirect("posts")
        else:
            print("Form is Invalid")
            print(form.errors)
    form = BlogPostForm()
    context = {"form": form}
    return render(request, "dashboard/add_post.html", context)


@login_required(login_url="login")
def edit_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            title = form.cleaned_data["title"]
            post.slug = slugify(title) + "-" + str(post.id)
            post = form.save()
            return redirect("posts")
    form = BlogPostForm(instance=post)
    context = {"form": form, "post": post}
    return render(request, "dashboard/edit_post.html", context)


@login_required(login_url="login")
def delete_post(request, pk):
    blog_post = get_object_or_404(Blog, pk=pk)
    blog_post.delete()
    return redirect("posts")
