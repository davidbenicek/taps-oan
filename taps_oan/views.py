from django.contrib.auth.views import password_reset_confirm, password_reset
from django.http import HttpResponse
from django.shortcuts import render
from taps_oan.models import Pub
from taps_oan.models import Beer
from taps_oan.forms import PubForm
from taps_oan.forms import BeerForm
from taps_oan.forms import CarrierForm
from taps_oan.forms import UserForm, UserProfileForm
from django.template.defaultfilters import slugify
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
import requests
import json


def reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, template_name='resetConfirm.html',
                                  uidb64=uidb64, token=token, post_reset_redirect=reverse('login'))


def reset(request):
    return password_reset(request, template_name='taps_oan/pwdReset.html',
                          email_template_name='taps_oan/reset_subject.html',
                          subject_template_name='taps_oan/email_title.html',
                          post_reset_redirect=reverse('login'))

def yelpLookUp(request, pub_name):
    # Sanatize pub_name from slug to readable string
    pub_name = pub_name.replace('-', " ")
    # Read in secrets
    f = open('secret.json')
    post_data = json.load(f)
    f.close()
    print post_data
    # Post secret to yelp to acquire token
    r = requests.post('https://api.yelp.com/oauth2/token', data=post_data)
    # Check response code is okay
    if r.status_code >= 400:
        return JsonResponse({'err': 'Trouble validating YELP token'}, status=404)
    # Extract token
    token = r.json().get('access_token')
    # Look up pub, in Glasgow, sort by most relevant and retrieve only 1 result
    r = requests.get(
        'https://api.yelp.com/v3/businesses/search?term=' + pub_name + '&location=Glasgow,UK&sort_by=best_match&limit=1',
        headers={'Authorization': 'Bearer ' + token})
    # Check status OK
    if r.status_code >= 400:
        return JsonResponse({'err': 'Trouble fetching pub ' + pub_name}, status=404)
    # Send back to front end
    return JsonResponse(r.json())


# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


# Updated the function definition
def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                               str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')

    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        # set the last visit cookie
        request.session['last_visit'] = last_visit_cookie

    # Update/set the visits cookie
    request.session['visits'] = visits


def index(request):
    request.session.set_test_cookie()
    pub_list = Pub.objects.order_by('-likes')[:5]
    beer_list = Beer.objects.order_by('-views')[:5]
    context_dict = {'pubs': pub_list, 'beers': beer_list}

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    response = render(request, 'taps_oan/index.html', context=context_dict)
    return response


def about(request):
    if request.session.test_cookie_worked():
        print "TEST COOKIE WORKED!"
        request.session.delete_test_cookie()
    visitor_cookie_handler(request)
    context_dict = {'visits': request.session['visits']}
    return render(request, 'taps_oan/about.html', context=context_dict)


def show_pub(request, pub_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}
    try:
        # Can we find a pub name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        pub = Pub.objects.get(slug=pub_name_slug)

        # Retrieve all of the associated beers.
        # Note that filter() will return a list of beer objects or an empty list
        beers = Beer.objects.filter(pub=pub)
        # beers = Pub.objects.get(beers)

        # Adds our results list to the template context under name beers.
        context_dict['beers'] = beers
        # We also add the pub object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the pub exists.
        context_dict['pub'] = pub
    except Pub.DoesNotExist:
        # We get here if we didn't find the specified pub.
        # Don't do anything -
        # the template will display the "no pub" message for us.
        context_dict['pub'] = None
        context_dict['beers'] = None
        # Go render the response and return it to the client.
    return render(request, 'taps_oan/pub.html', context_dict)


def show_beer(request, beer_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}
    exception = False
    try:
        # Can we find a pub name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        beer = Beer.objects.get(slug=beer_name_slug)
    except Beer.DoesNotExist:
        # We get here if we didn't find the specified pub.
        # Don't do anything -
        # the template will display the "no pub" message for us.
        context_dict['beer'] = None
        context_dict['pubs'] = None
        exception = True
    if not exception:
        # Retrieve all of the associated beers.
        # Note that filter() will return a list of beer objects or an empty list
        # pubs = Pub.beers.filter(beers_in=beer)
        pubs = Pub.objects.filter(beers__in=[beer])
        # Adds our results list to the template context under name beers.
        context_dict['pubs'] = list(pubs)
        # We also add the pub object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the pub exists.
        context_dict['beer'] = beer
        # Go render the response and return it to the client.
        print context_dict['pubs']
    return render(request, 'taps_oan/beer.html', context_dict)


@login_required
def add_pub(request):
    form = PubForm()

    # A HTTP POST?
    if request.method == 'POST':
        form = PubForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new pub to the database.
            form.save(commit=True)
            # Now that the pub is saved
            # We could give a confirmation message
            # But since the most recent pub added is on the index beer
            # Then we can direct the user back to the index beer.
            return index(request)
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print form.errors

    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'taps_oan/add_pub.html', {'form': form})


@login_required
def add_beer(request, pub_name_slug):
    try:
        pub = Pub.objects.get(slug=pub_name_slug)
    except Pub.DoesNotExist:
        pub = None

    form = BeerForm()
    if request.method == 'POST':
        form = BeerForm(request.POST)
        if form.is_valid():
            if pub:
                beer, created = Beer.objects.get_or_create(name=form.cleaned_data["name"].title())
                pub.beers.add(beer)
                return show_pub(request, pub_name_slug)
        else:
            print form.errors

    context_dict = {'form': form, 'pub': pub}
    return render(request, 'taps_oan/add_beer.html', context_dict)


@login_required
def add_carrier(request, beer_name_slug):
    form = CarrierForm()

    try:
        beer = Beer.objects.get(slug=beer_name_slug)
    except Beer.DoesNotExist:
        beer = None

    if request.method == 'POST':
        form = CarrierForm(request.POST)
        if form.is_valid():
            if beer:
                pub, created = Pub.objects.get_or_create(name=form.cleaned_data['name'].title())
                pub.beers.add(beer)
                return show_beer(request, beer_name_slug)
        else:
            print form.errors

    context_dict = {'form': form, 'beer': beer}
    return render(request, 'taps_oan/add_carrier.html', context_dict)


@login_required
def account(request):
    return render(request, 'taps_oan/account.html')


def register(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
            # put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
                  'taps_oan/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homebeer.
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'taps_oan/login.html', {})


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homebeer.
    return HttpResponseRedirect(reverse('index'))
