from django.contrib import admin
from .models import TechTool,SkillCategory,Project,Experience,Testimonial
# Register your models here.
admin.site.register(TechTool)
admin.site.register(SkillCategory)
admin.site.register(Project)
admin.site.register(Experience)
admin.site.register(Testimonial)