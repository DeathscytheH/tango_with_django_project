from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def index(request):
    # Construct a dictionary to pass to the template engine as it context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, full, sugar!"}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    return HttpResponse("Rango says here is the about page. Retun to <a href='/rango'> home </a> page.")
