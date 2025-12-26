from django.contrib import admin
from .models import Category, Blog,SocialMedia,About,Comment,NewsLetter,NewsLetterUser,NewsLetterMail


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

class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ('name','link','user','status','order')
    search_fields = ('id','name','link','status')
    list_display_links = ('link',)
    list_editable = ('status','name','order')

class AboutAdmin(admin.ModelAdmin):
    list_display = ('user','description','created_at','updated_at')
    list_editable = ('description',)


# Register your models here.
admin.site.register(Category)
admin.site.register(Blog,BlogAdmin)
admin.site.register(SocialMedia,SocialMediaAdmin)
admin.site.register(About,AboutAdmin)
admin.site.register(Comment)
admin.site.register(NewsLetter)
admin.site.register(NewsLetterUser)
admin.site.register(NewsLetterMail)
