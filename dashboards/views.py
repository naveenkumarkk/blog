from django.shortcuts import get_object_or_404, redirect, render
from blogs.models import Blog, Category
from django.contrib.auth.decorators import login_required
from .forms import BlogPostForm, CategoryForm,AddUserForm,EditUserForm
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
import markdown

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
    else:
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
    else:
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
    else:
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
    else:
        form = BlogPostForm(instance=post)
    context = {"form": form, "post": post}
    return render(request, "dashboard/edit_post.html", context)


@login_required(login_url="login")
def delete_post(request, pk):
    blog_post = get_object_or_404(Blog, pk=pk)
    blog_post.delete()
    return redirect("posts")


@login_required(login_url="login")
def users(request):
    user_list = User.objects.all()
    context = {
        "user_list":user_list
    }
    return render(request, "dashboard/users.html",context)

@login_required(login_url="login")
def add_users(request):
    if request.method == "POST":
        form =  AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
    else:
        form =  AddUserForm()
    context = {
        "form":form
    }
    return render(request, "dashboard/add_users.html",context)


@login_required(login_url="login")
def edit_user(request,pk):
    user_object = get_object_or_404(User,pk=pk)
    if request.method == "POST":
        form = EditUserForm(request.POST,instance = user_object)
        if form.is_valid():
            form.save()
            return redirect('users')
        else:
            print("Invalid Form")
            print(form.errors)
    else:
        form = EditUserForm(instance=user_object)
    context = {"form":form,"user_object":user_object}
    return render(request, "dashboard/edit_user.html",context)


@staff_member_required(login_url="login")
def delete_user(request, pk):
    user_list = get_object_or_404(User, pk=pk)
    if user_list.is_superuser:
        return redirect("users")
    user_list.delete()
    return redirect("users")


@login_required(login_url="login")
def markdown_preview(request):   
    if request.method == "POST":
        markdown_text = request.POST.get('markdown', '')
        html_output = markdown.markdown(
            markdown_text,
            extensions=["fenced_code", "codehilite", "tables", "nl2br", "sane_lists"]
        )
        return JsonResponse({'html': html_output})
    return JsonResponse({'error': 'Invalid request'}, status=400)