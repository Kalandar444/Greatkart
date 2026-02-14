# store/context_processors.py
def category_links(request):
    """
    Provides `links` = queryset of categories for your header dropdown.
    Safe to import even during migrations.
    """
    try:
        from .models import Category
        return {"links": Category.objects.all()}
    except Exception:
        # Model might not be ready (e.g., during migrate) — fail gracefully.
        return {"links": []}
