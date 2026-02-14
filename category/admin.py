from django.contrib import admin
from .models import Category
# Register your models here.


#admin.site.register(Category)


class CategoryAdmin(admin.ModelAdmin):
     prepopulated_fields = {'slug': ('category_name',)}  # ✅ comma makes it a tuple
     list_display=('category_name','slug')

admin.site.register(Category,CategoryAdmin)