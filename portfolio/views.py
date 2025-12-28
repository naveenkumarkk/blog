from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET,require_POST
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import json


from .forms import (
    ExperienceForm,
    ProjectForm,
    SkillCategoryForm,
    TechToolForm,
    TestimonialForm,
)
from .models import Experience, Project, SkillCategory, TechTool, Testimonial,GetInTouch


@login_required(login_url="login")
def portfolio(request):
    form_type = request.POST.get("form_type")

    tool_form = TechToolForm(prefix="tool")
    skill_form = SkillCategoryForm(prefix="skill")
    project_form = ProjectForm(prefix="project")
    experience_form = ExperienceForm(prefix="exp")
    testimonial_form = TestimonialForm(prefix="testi")

    if request.method == "POST":
        if form_type == "techtool":
            tool_form = TechToolForm(request.POST, prefix="tool")
            if tool_form.is_valid():
                tool_form.save()
                return redirect("portfolio")
        elif form_type == "skillcategory":
            skill_form = SkillCategoryForm(request.POST, prefix="skill")
            if skill_form.is_valid():
                skill_form.save()
                return redirect("portfolio")
        elif form_type == "project":
            project_form = ProjectForm(request.POST, prefix="project")
            if project_form.is_valid():
                project_form.save()
                return redirect("portfolio")
        elif form_type == "experience":
            experience_form = ExperienceForm(request.POST, prefix="exp")
            if experience_form.is_valid():
                experience_form.save()
                return redirect("portfolio")
        elif form_type == "testimonial":
            testimonial_form = TestimonialForm(request.POST, prefix="testi")
            if testimonial_form.is_valid():
                testimonial_form.save()
                return redirect("portfolio")

    context = {
        "tool_form": tool_form,
        "skill_form": skill_form,
        "project_form": project_form,
        "experience_form": experience_form,
        "testimonial_form": testimonial_form,
        "tools": TechTool.objects.all().order_by("name"),
        "skill_categories": SkillCategory.objects.prefetch_related("skills").order_by(
            "title"
        ),
        "projects": Project.objects.prefetch_related("tech_stack", "tools").order_by(
            "title"
        ),
        "experiences": Experience.objects.prefetch_related("skills").order_by(
            "company"
        ),
        "testimonials": Testimonial.objects.all().order_by("name"),
    }
    return render(request, "portfolio/portfolio.html", context)


@login_required(login_url="login")
def edit_tool(request, pk):
    tool = TechTool.objects.filter(pk=pk).first()
    if not tool:
        return redirect("portfolio")
    form = TechToolForm(request.POST or None, instance=tool, prefix="tool")
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("portfolio")
    return render(
        request,
        "portfolio/edit_item.html",
        {
            "form": form,
            "title": "Edit Tech Tool",
            "submit_label": "Update Tool",
            "back_url": reverse("portfolio"),
        },
    )


@login_required(login_url="login")
def delete_tool(request, pk):
    tool = TechTool.objects.filter(pk=pk).first()
    if not tool:
        return redirect("portfolio")
    if request.method == "POST":
        tool.delete()
        return redirect("portfolio")
    return render(
        request,
        "portfolio/confirm_delete.html",
        {
            "title": "Delete Tech Tool",
            "object_name": tool.name,
            "confirm_url": request.path,
            "back_url": reverse("portfolio"),
        },
    )


@login_required(login_url="login")
def edit_skill_category(request, pk):
    category = SkillCategory.objects.filter(pk=pk).first()
    if not category:
        return redirect("portfolio")
    form = SkillCategoryForm(request.POST or None, instance=category, prefix="skill")
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("portfolio")
    return render(
        request,
        "portfolio/edit_item.html",
        {
            "form": form,
            "title": "Edit Skill Category",
            "submit_label": "Update Category",
            "back_url": reverse("portfolio"),
        },
    )


@login_required(login_url="login")
def delete_skill_category(request, pk):
    category = SkillCategory.objects.filter(pk=pk).first()
    if not category:
        return redirect("portfolio")
    if request.method == "POST":
        category.delete()
        return redirect("portfolio")
    return render(
        request,
        "portfolio/confirm_delete.html",
        {
            "title": "Delete Skill Category",
            "object_name": category.title,
            "confirm_url": request.path,
            "back_url": reverse("portfolio"),
        },
    )


@login_required(login_url="login")
def edit_project(request, pk):
    project = Project.objects.filter(pk=pk).first()
    if not project:
        return redirect("portfolio")
    form = ProjectForm(request.POST or None, instance=project, prefix="project")
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("portfolio")
    return render(
        request,
        "portfolio/edit_item.html",
        {
            "form": form,
            "title": "Edit Project",
            "submit_label": "Update Project",
            "back_url": reverse("portfolio"),
        },
    )


@login_required(login_url="login")
def delete_project(request, pk):
    project = Project.objects.filter(pk=pk).first()
    if not project:
        return redirect("portfolio")
    if request.method == "POST":
        project.delete()
        return redirect("portfolio")
    return render(
        request,
        "portfolio/confirm_delete.html",
        {
            "title": "Delete Project",
            "object_name": project.title,
            "confirm_url": request.path,
            "back_url": reverse("portfolio"),
        },
    )


@login_required(login_url="login")
def edit_experience(request, pk):
    exp = Experience.objects.filter(pk=pk).first()
    if not exp:
        return redirect("portfolio")
    form = ExperienceForm(request.POST or None, instance=exp, prefix="exp")
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("portfolio")
    return render(
        request,
        "portfolio/edit_item.html",
        {
            "form": form,
            "title": "Edit Experience",
            "submit_label": "Update Experience",
            "back_url": reverse("portfolio"),
        },
    )


@login_required(login_url="login")
def delete_experience(request, pk):
    exp = Experience.objects.filter(pk=pk).first()
    if not exp:
        return redirect("portfolio")
    if request.method == "POST":
        exp.delete()
        return redirect("portfolio")
    return render(
        request,
        "portfolio/confirm_delete.html",
        {
            "title": "Delete Experience",
            "object_name": f"{exp.company} - {exp.title}",
            "confirm_url": request.path,
            "back_url": reverse("portfolio"),
        },
    )


@login_required(login_url="login")
def edit_testimonial(request, pk):
    testi = Testimonial.objects.filter(pk=pk).first()
    if not testi:
        return redirect("portfolio")
    form = TestimonialForm(request.POST or None, instance=testi, prefix="testi")
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("portfolio")
    return render(
        request,
        "portfolio/edit_item.html",
        {
            "form": form,
            "title": "Edit Testimonial",
            "submit_label": "Update Testimonial",
            "back_url": reverse("portfolio"),
        },
    )


@login_required(login_url="login")
def delete_testimonial(request, pk):
    testi = Testimonial.objects.filter(pk=pk).first()
    if not testi:
        return redirect("portfolio")
    if request.method == "POST":
        testi.delete()
        return redirect("portfolio")
    return render(
        request,
        "portfolio/confirm_delete.html",
        {
            "title": "Delete Testimonial",
            "object_name": testi.name,
            "confirm_url": request.path,
            "back_url": reverse("portfolio"),
        },
    )

def serialize_project(project):
    return {
        "id": project.id,
        "title": project.title,
        "category": project.category,
        "description": project.description,
        "live_link": project.live_link,
        "role": project.role,
        "image": project.image,
        "tech_stack": [
            serialize_techtool(tool)
            for tool in project.tech_stack.filter(status="Active")
        ],
        "tools": [
            serialize_techtool(tool)
            for tool in project.tools.filter(status="Active")
        ],
    }

def serialize_techtool(tool):
    return {
        "id": tool.id,
        "name": tool.name,
        "icon": tool.icon,
        "color": tool.color,
    }

def serialize_experience(exp):
    return {
        "id": exp.id,
        "company": exp.company,
        "logo": exp.logo,
        "title": exp.title,
        "period": exp.period,
        "description": exp.description,
        "skills": [
            serialize_techtool(tool)
            for tool in exp.skills.filter(status="Active")
        ],
    }

def serialize_skill_category(category):
    return {
        "id": category.id,
        "title": category.title,
        "skills": [
            serialize_techtool(tool)
            for tool in category.skills.filter(status="Active")
        ],
    }

def get_portfolio_detail(request):
    data = {
        "testimonials": list(
            Testimonial.objects.values(
                "id", "name", "position", "content", "image"
            )
        ),
        "experience": [
            serialize_experience(exp)
            for exp in Experience.objects.all()
        ],
        "project": [
            serialize_project(proj)
            for proj in Project.objects.all()
        ],
        "skills": [
            serialize_skill_category(cat)
            for cat in SkillCategory.objects.all()
        ],
        "techtool": [
            serialize_techtool(tool)
            for tool in TechTool.objects.filter(status="Active")
        ],
    }

    return JsonResponse({"success": True, "data": data})
@csrf_exempt
@require_POST
def send_contact_form(request):
    try:
        # Parse JSON body
        data = json.loads(request.body.decode("utf-8"))

        client_name = data.get("name")
        client_email = data.get("email")
        subject = data.get("subject")
        message = data.get("message")

        # Basic validation
        if not all([client_name, client_email, subject, message]):
            return JsonResponse(
                {"success": False, "error": "All fields are required"},
                status=400
            )

        # Save to DB
        GetInTouch.objects.create(
            client_name=client_name,
            client_email=client_email,
            subject=subject,
            message=message
        )

        # Email body
        body = f"""
        From: {client_name}
        Email: {client_email}

        Message:
        {message}
        """

        # Send email
        send_mail(
            subject=f"[Portfolio Contact] {subject}",
            message=body,
            from_email="naveenkumar.dev.io@gmail.com",
            recipient_list=["jayakulandhaivel@gmail.com"],
            fail_silently=False,
        )

        return JsonResponse({"success": True})

    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "error": "Invalid JSON"},
            status=400
        )

    except Exception as e:
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=500
        )

