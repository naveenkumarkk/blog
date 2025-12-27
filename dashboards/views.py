from django.shortcuts import get_object_or_404, redirect, render
from blogs.models import Blog, Category,NewsLetter,NewsLetterUser
from django.contrib.auth.decorators import login_required
from .forms import BlogPostForm, CategoryForm,AddUserForm,EditUserForm, NewsLetterForm
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse
import markdown
from django.views.decorators.http import require_GET,require_POST
from django.core.mail import send_mail
from django_q.tasks import async_task
from django.db.models import Q 

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


@require_POST
def newsletter_send(request):
    return 

@require_GET
def send_test_email(request):
    send_mail(
        subject="Hello from Django",
        message="This is a test email sent from Django.",
        from_email="naveenkumar.dev.io@gmail.com",
        recipient_list=["jayakulandhaivel@gmail.com"],
        fail_silently=False,
    )
    return HttpResponse("Email sent!")

@require_POST
def send_email(request,newsletter_id):
    newsletter = get_object_or_404(NewsLetter,id=newsletter_id)
    
    async_task('dashboards.task.send_newsletter_email',newsletter.id)
    return JsonResponse({
        "success": True,
        "message": "Newsletter queued successfully 🚀"
    })


@login_required(login_url="login")
def newsletter(request):
    if request.method == "POST":
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("newsletter")
    else:
        form = NewsLetterForm()
    
    newsletters = (
        NewsLetter.objects
        .filter(status__in=["Draft", "Published"])
        .order_by("-created_at")
    )
    context = {
        "form": form,
        "newsletters": newsletters,
    }
    return render(request, "dashboard/new_letter.html", context)


@login_required(login_url="login")
def edit_newsletter(request, pk):
    newsletter_obj = get_object_or_404(NewsLetter, pk=pk)
    if request.method == "POST":
        form = NewsLetterForm(request.POST, instance=newsletter_obj)
        if form.is_valid():
            form.save()
            return redirect("newsletter")
    else:
        form = NewsLetterForm(instance=newsletter_obj)
    context = {
        "form": form,
        "newsletter": newsletter_obj,
        "is_edit": True,
    }
    return render(request, "dashboard/edit_newsletter.html", context)


@login_required(login_url="login")
def delete_newsletter(request, pk):
    newsletter_obj = get_object_or_404(NewsLetter, pk=pk)
    if request.method == "POST":
        newsletter_obj.delete()
        return redirect("newsletter")
    context = {
        "newsletter": newsletter_obj,
    }
    return render(request, "dashboard/delete_newsletter.html", context)
