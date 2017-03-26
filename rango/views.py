from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Import the category and page model
from rango.models import Category, Page

# Import the forms
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

# Import std libraries
from datetime import datetime

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
    
    # Test cookie
    request.session.set_test_cookie()

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

    # Call the helper function to handle the cookies
    visitor_cookie_handler(request)
    
    # Pass the number of visits
    context_dict['visits'] = request.session['visits']
    
    # Response object
    response = render(request, 'rango/index.html', context=context_dict)
    
    # Render the response and send it back.
    # Return response back to the user, updating any cookies that need changed.
    return response


def about(request):
    # Call the helper function to handle the cookies
    visitor_cookie_handler(request)
    
    context_dict = {'boldmessage': "Alejandro H. Pineda"}
    
    # Pass the number of visits
    context_dict['visits'] = request.session['visits']    
    
    # Response object
    response = render(request, 'rango/about.html', context=context_dict)    

    return response


@login_required
def add_category(request):
    form = CategoryForm()
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            cat = form.save(commit=True)
            print(cat, cat.slug)
            # Now that the category is saved we could give a confirmation
            # message but since the most recent category added is on the index
            # page.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the cmd.
            print(form.errors)
    # Will handle the bad form, new form, or no form suppied cases. Render the
    # form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    # Preguntamos si existe la categoria o la dejamos vacia
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    
    # Creamos una forma vacia
    form = PageForm()
    # Si es un post
    if request.method == 'POST':
        form = PageForm(request.POST)
        # Si es una forma valida continuamos
        if form.is_valid():
            # Si existe la categoria
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)


# Helper function, doesn't return a response object.
# Updated the function definition
def visitor_cookie_handler(request):
    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, then the default value of 1 is used.
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    
    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
    
    # Update/set the visits cookie
    request.session['visits'] = visits


# Another helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val
