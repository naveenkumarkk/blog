from django import forms
from .models import Experience, Project, SkillCategory, TechTool, Testimonial


class TechToolForm(forms.ModelForm):
    class Meta:
        model = TechTool
        fields = ("name", "icon", "color", "status")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Tool name"}),
            "icon": forms.TextInput(attrs={"class": "form-control", "placeholder": "Icon key"}),
            "color": forms.TextInput(attrs={"class": "form-control", "placeholder": "Color (e.g. #123abc)"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }


class SkillCategoryForm(forms.ModelForm):
    class Meta:
        model = SkillCategory
        fields = ("title", "skills")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Category title"}),
            "skills": forms.SelectMultiple(attrs={"class": "form-control"}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("title", "category", "description", "live_link", "role", "tech_stack", "tools", "image")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Project title"}),
            "category": forms.TextInput(attrs={"class": "form-control", "placeholder": "Category"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Project description"}),
            "live_link": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://..."}),
            "role": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your role"}),
            "tech_stack": forms.SelectMultiple(attrs={"class": "form-control"}),
            "tools": forms.SelectMultiple(attrs={"class": "form-control"}),
            "image": forms.URLInput(attrs={"class": "form-control", "placeholder": "Image URL (optional)"}),
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ("company", "logo", "title", "period", "description", "skills")
        widgets = {
            "company": forms.TextInput(attrs={"class": "form-control", "placeholder": "Company"}),
            "logo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Icon key (optional)"}),
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Job title"}),
            "period": forms.TextInput(attrs={"class": "form-control", "placeholder": "Period e.g. 2022-2024"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "What you did"}),
            "skills": forms.SelectMultiple(attrs={"class": "form-control"}),
        }


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ("name", "position", "content", "image")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Name"}),
            "position": forms.TextInput(attrs={"class": "form-control", "placeholder": "Position"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Testimonial"}),
            "image": forms.URLInput(attrs={"class": "form-control", "placeholder": "Image URL (optional)"}),
        }
