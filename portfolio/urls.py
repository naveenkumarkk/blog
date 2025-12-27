from django.urls import path
from . import views

urlpatterns = [
    path('', views.portfolio, name='portfolio'),
    path('tool/<int:pk>/edit/', views.edit_tool, name='portfolio_edit_tool'),
    path('tool/<int:pk>/delete/', views.delete_tool, name='portfolio_delete_tool'),
    path('skill-category/<int:pk>/edit/', views.edit_skill_category, name='portfolio_edit_skill_category'),
    path('skill-category/<int:pk>/delete/', views.delete_skill_category, name='portfolio_delete_skill_category'),
    path('project/<int:pk>/edit/', views.edit_project, name='portfolio_edit_project'),
    path('project/<int:pk>/delete/', views.delete_project, name='portfolio_delete_project'),
    path('experience/<int:pk>/edit/', views.edit_experience, name='portfolio_edit_experience'),
    path('experience/<int:pk>/delete/', views.delete_experience, name='portfolio_delete_experience'),
    path('testimonial/<int:pk>/edit/', views.edit_testimonial, name='portfolio_edit_testimonial'),
    path('testimonial/<int:pk>/delete/', views.delete_testimonial, name='portfolio_delete_testimonial'),
    path('get', views.delete_testimonial, name='portfolio_delete_testimonial'),
]