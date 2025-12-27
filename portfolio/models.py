from django.db import models

class TechTool(models.Model):
    STATUS_CHOICES = (
        ("Active", "Active"),
        ("Inactive", "Inactive"),
    )

    name = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=50)     
    color = models.CharField(max_length=20)   
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="Active"
    )

    def __str__(self):
        return self.name

class SkillCategory(models.Model):
    title = models.CharField(max_length=50, unique=True)
    skills = models.ManyToManyField(TechTool, related_name="categories")

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50)
    description = models.TextField()
    live_link = models.URLField()
    role = models.CharField(max_length=100)

    tech_stack = models.ManyToManyField(
        TechTool,
        related_name="projects"
    )

    tools = models.ManyToManyField(
        TechTool,
        related_name="tool_projects",
        blank=True
    )

    image = models.URLField(blank=True)

    def __str__(self):
        return self.title


class Experience(models.Model):
    company = models.CharField(max_length=100)
    logo = models.CharField(max_length=50,blank=True)  # frontend icon key
    title = models.CharField(max_length=100)
    period = models.CharField(max_length=100)
    description = models.TextField()

    skills = models.ManyToManyField(
        TechTool,
        related_name="experiences"
    )

    def __str__(self):
        return f"{self.company} - {self.title}"


class Testimonial(models.Model):
    name = models.CharField(max_length=100,blank=False)
    position = models.CharField(max_length=100,blank=False)
    content = models.TextField(blank=False)
    image = models.URLField(blank=True)

    def __str__(self):
        return self.name
