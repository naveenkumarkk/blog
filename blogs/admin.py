from django.contrib import admin
from .models import Category, Blog


class BlogAdmin(admin.ModelAdmin):
    # This will create a prepopluate feild copied from title field to the slug field
    # Useful to create slug name 
    prepopulated_fields = {'slug':('title',)}
    # To list what feilds needed to be displayed in the dashboard 
    list_display = ('title','category','author','is_featured','status')
    # To search Record
    # In order to search the foreign key, use __ like below
    search_fields = ('id','title','category__category_name','status')
    # We can make the fileds editable in the search list section
    list_editable = ('is_featured',)

# Register your models here.
admin.site.register(Category)
admin.site.register(Blog,BlogAdmin)