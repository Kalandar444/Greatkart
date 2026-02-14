#from django.http import HttpResponse
from django.shortcuts import render
from store.models import Product

# Create your views here.
def home(request):
    products=Product.objects.all().filter(is_available=True)

    #return httpresponse('Home Page')

    context={
        'products':products,
    }

    return render(request,'home.html',context)
