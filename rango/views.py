from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from rango.forms import UserForm, UserProfileForm


def add_page(request, category_name_slug):

    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
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


def add_category(request):
    form = CategoryForm()

    # a http post?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # have we been provided with a valid form?
        if form.is_valid():
            # save the new category to the database
            cat = form.save(commit=True)
            # return to index page since new category is added
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
    # Prints out whether message is a GET or a POST
    print(request.method)
    # Prints out the user name, if no one is logged in it prints anonymoususer
    print(request.user)
    return render(request, 'rango/about.html', {})


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST or None)
        profile_form = UserProfileForm(data=request.POST or None)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['pictures']
            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm
        profile_form = UserProfileForm

    return render(request, 'rango/register.html', {'user_form': user_form, 'profile_form': profile_form,
                                                   'registered': registered})
