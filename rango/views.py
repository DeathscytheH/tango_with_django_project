from django.shortcuts import render
from django.http import HttpResponse

# Import the category model
from rango.models import Category


# Create your views here.

def index(request):
    # Query the db for a list of ALL categories currently stored. Order the
    # categories by # of likes in descending order. Retrieve the top 5 only -
    # or all if less than 5. Place the list in our context_dict that will be
    # passed to the template engine.

    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    # Render the response and send it back.
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict = {'boldmessage': "Alejandro H. Pineda"}

    return render(request, 'rango/about.html', context=context_dict)
