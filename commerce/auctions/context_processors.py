from .models import Category

def get_category(request):
    categories = Category.objects.all()
    return {'categories':categories}
