from django.shortcuts import render
from rango.models import Category, Page
from django.http import HttpResponse
from rango.forms import CategoryForm


def add_category(request):
    form = CategoryForm()

    # a http post?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # have we been provided with a valid form?
        if form.is_valid():
    # save the new category to the database
            cat = form.save(commit=True)
            #return to index page since new category is added
            return index(request)
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})



def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)

        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages

        context_dict['category'] = category

    except Category.DoesnotExist:
        context_dict['pages'] = None
        context_dict['category'] = None

    return render(request, 'rango/category.html', context_dict)


def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary
    # that will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': pages_list}
    # Render the response and send it back!
    return render(request, 'rango/index.html', context_dict)


def about(request):
    HttpResponse('This is the about page')
    return render(request, 'rango/about.html/')
