from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import (
    ExperienceForm,
    ProjectForm,
    SkillCategoryForm,
    TechToolForm,
    TestimonialForm,
)
from .models import Experience, Project, SkillCategory, TechTool, Testimonial


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


def get_portfolio_detail(request):
    data = {
        "testimonials": list(Testimonial.objects.all().values()),
        "experience": list(Experience.objects.all().values()),
        "project": list(Project.objects.all().values()),
        "skills": list(SkillCategory.objects.all().values()),
        "techtool": list(TechTool.objects.filter(status='Active').values()),
    }
    return JsonResponse({"success": True, "data": data})