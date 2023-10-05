from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse
from .forms import RegistrationForm, UserProfileForm  
from .models import UserProfile, Book
from .search_functions.ciela_search_query import search_ciela
from .search_functions.orange_search_query import search_orange
from .search_functions.ozone_search_query import search_ozone

def search_local(title, author):
    print(title, author)
    # Search in the local database for existing books
    existing_books = []
    
    all_books = Book.objects.all()
    for book in all_books:
        if (author.lower() == book.author.lower()) & (title.lower() in book.title.lower()):
            existing_books.append(book)

    # Create a list of dictionaries with the desired format
    local_results = []
    for book in existing_books:
        book_dict = {
            'title': book.title,
            'author': book.author,
            'price': book.price,
            'link': book.link
        }
        local_results.append(book_dict)
    print(local_results)
    return local_results

@login_required
def search(request):
    title = request.GET.get('title')
    author = request.GET.get('author')
    selected_sites = request.GET.getlist('sites')

    local_results = search_local(title, author)
    search_results = local_results if local_results else []
    print(search_results)

    if 'all' in selected_sites and not local_results:
        search_results.append(search_ciela(title, author))  # Search Ciela
        search_results.append(search_orange(title, author))  # Search Orange Center
        search_results.append(search_ozone(title, author))  # Search Ozone
    elif not local_results:
        if 'ciela' in selected_sites:
            search_results.append(search_ciela(title, author))  # Search Ciela
        if 'orangecenter' in selected_sites:
            search_results.append(search_orange(title, author))  # Search Orange Center
        if 'ozone' in selected_sites:
            search_results.append(search_ozone(title, author))  # Search Ozone
    
    #Remove any empty entries
    search_results = [result for result in search_results if result]

    #Sort the results by price
    sorted_results = sorted(search_results, key=lambda x: float(x['price']))

    #Get current favorites to dispaly
    user_favorites = request.user.userprofile.favorite_books.all()
    
    context = {'search_results': sorted_results,
               'user_favorites': user_favorites
    }
    return render(request, 'home.html', context)

@login_required
def add_to_favorites(request):
    if request.method == 'POST':
        link = request.POST.get('link')  # Get the link from the POST data
        user = request.user

        # Check if the book with the given link exists in the database
        try:
            book = Book.objects.get(link=link)
        except Book.DoesNotExist:
            return redirect('home')  # Redirect to home if book not found
        
        # Add the book to the user's list of favorite books
        user.userprofile.favorite_books.add(book)
        user.userprofile.save()

        return redirect('home')  # Redirect back to the home page

    return redirect('home')  # Redirect back to the home page if not a POST request

@login_required
def remove_from_favorites(request):
    if request.method == 'POST':
        link = request.POST.get('link')
        book_to_remove = get_object_or_404(Book, link=link)
        request.user.userprofile.favorite_books.remove(book_to_remove)
    return redirect('home')

@login_required
def home(request):

    user_favorites = request.user.userprofile.favorite_books.all()
    # Pass context data to the template
    context = {
        'user': request.user,
        'username': request.user.username,
        'user_favorites': user_favorites
    }
    
    return render(request, 'home.html', context)

@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        password_change_form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile changes saved successfully.')

        if password_change_form.is_valid():
            password_change_form.save()
            update_session_auth_hash(request, password_change_form.user)
            messages.success(request, 'Password changed successfully.')

        if form.is_valid() or password_change_form.is_valid():
            return redirect('home')

    else:
        form = UserProfileForm(instance=user_profile)
        password_change_form = PasswordChangeForm(request.user)

    context = {'form': form, 'password_change_form': password_change_form}
    return render(request, 'profile/edit_profile.html', context)

@login_required
def send_favorites_email(request):
    user_profile = UserProfile.objects.get(user=request.user)
    favorites_list = request.user.userprofile.favorite_books.all()
    subject = 'Your Favorite Books Information'
    
    if favorites_list:
        # Prepare the context for the email template
        email_context = {
            'favorites_list': favorites_list,
            'username': request.user.username  # Include the username in the context
        }

        # Create a text version of the email content
        email_text = render_to_string('email/favorites_email.txt', email_context)
        email_text = strip_tags(email_text)  # Remove HTML tags

        # Send the email
        send_mail(
            subject,
            email_text,
            settings.EMAIL_HOST_USER,  # Replace with a actual email address
            [user_profile.email],  # Send the email to the user's email address
            fail_silently=False,
        )
        # Return a JSON response indicating success
        return JsonResponse({'success': True, 'message': 'Email sent successfully.'})
    else:
        return JsonResponse({'success': False, 'message': 'No favorite books to send.'})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_profile = UserProfile(user=user, email=form.cleaned_data['email'])
            user_profile.save()
            # Log the user in
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')
