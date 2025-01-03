from .models import Category

def menu_links(request):
    try:
        links = Category.objects.all().order_by('category_name')
        return {'links': links}
    except:
        return {'links': None}
