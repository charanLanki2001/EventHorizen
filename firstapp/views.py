from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages 
from django.template.loader import render_to_string
from .forms import EventForm
from datetime import datetime
from .models import Event
import random
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
import random
from django.db import transaction  # Import the transaction module

from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail
from .forms import PaymentForm
import logging
from .models import Payment

# Create your views here.


@login_required(login_url='login')
def HomePage(request):
    username = request.user.username
    # Retrieve upcoming events from your database or data source
   

    return render(request, 'home.html', {'username': username,})



def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            error_message = "Your password and confirm password do not match."
            return render(request, 'signup.html', {'error_message': error_message})
        else:
            if User.objects.filter(username=uname).exists():
                error_message = "Username already exists. Please choose a different username."
                return render(request, 'signup.html', {'error_message': error_message})
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            success_message = "User registered successfully! You can now log in."
            return render(request, 'login.html', {'success_message': success_message})
            

    return render(request, 'signup.html')


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Username or Password is incorrect!!!"
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')
# ... other imports ...



# ...

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            otp = str(random.randint(100000, 999999))

            # Send OTP to user's email
            subject = 'Password Reset OTP'
            message = f'Your OTP is: {otp}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)

            # Store email and OTP in session
            request.session['reset_email'] = email
            request.session['otp'] = otp

            return render(request, 'password/verify_otp.html')
        except User.DoesNotExist:
            error_message = "No user with this email address exists."
            return render(request, 'password/forgot_password.html', {'error_message': error_message})

    return render(request, 'password/forgot_password.html')

# verify_otp view
def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        email = request.session.get('reset_email')
        otp_from_session = request.session.get('otp')  # Retrieve the OTP from session
        user = User.objects.get(email=email)

        if entered_otp == otp_from_session:  # Compare entered OTP with OTP from session
            return redirect('reset_password', email=email)
        else:
            error_message = "Invalid OTP. Please try again."
            return render(request, 'password/verify_otp.html', {'error_message': error_message})
    return render(request, 'password/verify_otp.html')

# reset_password view
def reset_password(request, email):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            del request.session['reset_email']  # Remove stored email from session
            del request.session['otp']  # Remove stored OTP from session
            return redirect('login')
        else:
            error_message = "Passwords do not match."
            return render(request, 'password/reset_password.html', {'error_message': error_message})

    return render(request, 'password/reset_password.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

def new_events(request):
    return render(request, 'NewEvents.html')



def create_events(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.username = request.user
            event.event_datetime = timezone.now()  # Set the event datetime with timezone information
            event.save()
            messages.success(request, "Event created successfully.")
            return redirect('success_page')
        else:
            messages.error(request, "Form validation failed. Please check the form fields.")
    else:
        form = EventForm()
    
    return render(request, 'create.html', {'form': form})
def success_page(request):
    return render(request, 'success/suucesscreate.html')



def update_event(request, event_id=None):
    if event_id:
        # Handle updating a specific event
        try:
            event = Event.objects.get(pk=event_id)

            if request.method == 'POST':
                form = EventForm(request.POST, instance=event)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Event details have been successfully updated.')
                    return redirect('success_page')  # Redirect to the success page

            events = Event.objects.filter(username=request.user)
            event_form = EventForm(instance=event)

            return render(request, 'update.html', {'events': events, 'event_form': event_form})
        except Event.DoesNotExist:
            # Handle the case where the event with the given ID does not exist
            messages.error(request, 'Event does not exist.')
            return redirect('update_event')
    else:
        # Handle displaying all updated events
        events = Event.objects.filter(username=request.user)
        event_form = EventForm()

        return render(request, 'update.html', {'events': events, 'event_form': event_form})


def event_view(request):
    # Get the event with the specified event_id
    events = Event.objects.all()
    return render(request, 'event_view.html', {'events': events})



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Event
from .forms import EventForm
from django.contrib.messages import get_messages

def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    form = EventForm(request.POST or None, instance=event)

    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()

                # Check if changes were made
                if form.has_changed():
                    messages.success(request, 'Event details have been successfully updated.')

                    # Delay the redirection by a few seconds (adjust the delay as needed)
                    return render(request, 'editupdate.html', {'form': form, 'event': event, 'delay_redirect': True})
                else:
                    messages.info(request, 'No changes were made to the event details.')

                return redirect('update_event')
        except Exception as e:
            # Handle exceptions here
            messages.error(request, f'An error occurred: {str(e)}')

    return render(request, 'editupdate.html', {'form': form, 'event': event})


def delete_event(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')  # Get the event_id from the form
        try:
            event = Event.objects.get(id=event_id)
            if event.username == request.user:  # Check if the event belongs to the logged-in user
                event.delete()
                return redirect('update_event')  # Redirect back to the update_event page
            else:
                # If the event doesn't belong to the user, show an error or redirect to an appropriate page
                pass
        except Event.DoesNotExist:
            pass
    return redirect('update_event')  # Redirect back to the update_event page

def about_us(request):
    return render(request, 'about_us.html')
    
#registration and payment views here
def registration_details(request,event_id):
   event = get_object_or_404(Event, pk=event_id)
   context = {'event': event}
   return render(request, 'registration.html', context)




from django.shortcuts import render, get_object_or_404
from .models import Event
from django.core.mail import send_mail
from django.conf import settings
import logging

def payment(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    email_sent = 0  # Initialize email_sent with a default value

    if request.method == 'POST':
        # Handle the payment processing logic here (you can simulate a successful payment)
        user_email = request.POST.get('user_email')
        entry_fee = event.entry_fee 
        
        # Simulate a successful payment
        
        # Send a confirmation email
        subject = 'Payment Confirmation'
        message = 'Thank you for your payment. Your payment was successful.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user_email]
        
        try:
            # Attempt to send the email
            email_sent = send_mail(subject, message, from_email, recipient_list)
            
            if email_sent == 1:
                # Render the payment success template with the user's email and event details
                payment = Payment.objects.create(
                    email=user_email,
                    payment_date=timezone.now(),  # Use the current date and time as the payment date
                    eventname=event.event_name,
                    amount=entry_fee  # Use the entry fee as the payment amount
                )
                payment.save()

                # Render the payment success template with the user's email and event details
                context = {'user_email': user_email, 'event': event}
                return render(request, 'payment/payment_success.html', context)
            else:
                # Log the error
                logging.error(f'Error sending confirmation email to {user_email}')
                
                # Pass the error message to the template
                error_message = 'There was an issue sending the confirmation email. Please try again.'
    
                return render(request, 'payment/payment.html', {'event': event, 'error_message': error_message})
        except Exception as e:
            logging.error(f'Exception occurred while sending email: {str(e)}')

    # Handle GET requests or invalid submissions
    return render(request, 'payment/payment.html', {'event': event, 'email_sent': email_sent})


def payment_success(request,event_id):
    event = get_object_or_404(Event, pk=event_id)
    context = {'event': event}
    # You can also render a success page or redirect to a specific URL
    return render(request, 'payment/payment_success.html',{'context': context} )
   


@login_required
def user_registered_events(request, event_id=None):
    # Get the user
    user = request.user

    # Fetch the events registered by the currently logged-in user
    registered_events = Event.objects.filter(payment__email=user.email)

    if event_id is not None:
        # If 'event_id' is provided, get the specific event for the given event_id
        event = get_object_or_404(registered_events, pk=event_id)
        context = {'event': event}
    else:
        # If 'event_id' is not provided, you can provide a list of all registered events
        context = {'registered_events': registered_events}

    # Render the template with the appropriate context
    return render(request, 'registered_events.html', context)








