from django.shortcuts import render
from django.http import HttpResponse

# Import the category and page model
from rango.models import Category
from rango.models import Page


# Create your views here.

def show_category(request, category_name_slug):
    # Create a context_dict which we can pass to the template rendering engine
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all of the associated pages.
        # Note that filter() will return a list of page objects or an empty list
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages

        # We also add the category object from the database to the context
        # dictionary. We'll use this in the template to verify that the
        # category exist
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything, the template will display "no category" message
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'rango/category.html', context_dict)


def index(request):
    # Query the db for a list of ALL categories currently stored. Order the
    # categories by # of likes in descending order. Retrieve the top 5 only -
    # or all if less than 5. Place the list in our context_dict that will be
    # passed to the template engine.

    # Empty diccionary
    context_dict = {}

    try:
        # Recuperar el top 5 de categorias por likes
        category_list = Category.objects.order_by('-likes')[:5]

        # Recuperar el top 5 de las paginas más vistas
        page_list = Page.objects.order_by('-views')[:5]

        # Agregarlo al diccionario ambas listas
        context_dict['categories'] = category_list
        context_dict['pages'] = page_list
    except (Category.DoesNotExist, Page.DoesNotExist):
        context_dict['categories'] = None
        context_dict['pages'] = None

    # Render the response and send it back.
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict = {'boldmessage': "Alejandro H. Pineda"}

    return render(request, 'rango/about.html', context=context_dict)
