from django import forms
from blogs.models import Blog,Category
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title','category','feature_image','short_description','blog_body','status','is_featured')

class AddUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','is_staff','is_active',"groups",'user_permissions','date_joined')

class EditUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email','is_staff','is_superuser','is_active',"groups",'user_permissions','date_joined')
