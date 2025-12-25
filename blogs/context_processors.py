from .models import Category,About,SocialMedia


def get_categories(request):
    categories = Category.objects.all()
    return dict(categories=categories)

def get_social_links(request):
    social_media_links = SocialMedia.objects.filter(status='Active').order_by('order')
    return dict(social_media_links=social_media_links)

def get_about(request):
    about =  About.objects.first()
    return dict(about=about)
