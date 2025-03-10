from django.shortcuts import render, redirect
from django.utils.formats import FORMAT_SETTINGS
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import get_user_model, logout, login, update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail
from base.models import Item
from config.settings.base import EMAIL_HOST_USER
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required

from .models import Participant, Zone, Application
from .forms import ParticipantRegistraionForm, ParticipationForm


User = get_user_model()
def home(request):
    home="https://sargam.cusat.ac.in"
    return redirect(home)

class RegistrationView(TemplateView):
    template_name = "accounts/reg_login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('user_profile')

        form = ParticipantRegistraionForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = ParticipantRegistraionForm(request.POST, request.FILES)
        if form.is_valid():
            form_data = form.cleaned_data

            if form_data['password'] != form_data['confirm_password']:
                messages.error(request, "Passwords do not match!")
                return render(request, self.template_name, {'form': form})

            if User.objects.filter(email=form_data['email']).exists():
                messages.error(request, "Invalid E-Mail ID!")
                return render(request, self.template_name, {'form': form})

            if Participant.objects.filter(studentid=form_data['studentid']).exists():
                messages.error(request, "Invalid Student ID!")
                return render(request, self.template_name, {'form': form})

            new_user = User.objects.create_user(
                full_name=form_data['name'],
                email=form_data['email'], 
                password=form_data['password'],
                is_active=True
            )
            new_user.save()

            Participant.objects.create(
                user=new_user,
                name=form_data['name'],
                email=form_data['email'],
                zone=Zone.objects.get(id=form_data['zone'].id),
                photo=request.FILES['photo'],
                studentid=form_data['studentid'],
                id_card=request.FILES['id_card'],
                ph_number=form_data['ph_number']
            )

            # send_mail(
            #     subject="Sargam Application Verification",
            #     message=f"Click this link to verify your Application: {create_verification_link(new_user)}",
            #     from_email=EMAIL_HOST_USER,
            #     recipient_list=[form_data['email']],
            #     fail_silently=False,
            # )

            return redirect('user_login')

        return render(request, self.template_name, {"form": form})

	
def user_login(request):
    if request.user.is_authenticated:
         return redirect('user_profile')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                # Log the user in
                login(request, user)
                return redirect('user_profile')
            else:
                messages.error(request, "Invalid email or password.")
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.")
    return render(request, 'accounts/user_login.html')
	
@login_required(login_url="/app/login/")
def user_logout(request):
    logout(request)
    return redirect('user_login')

@login_required(login_url="/app/login/")
def user_profile(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    try:
        participant = Participant.objects.get(user=request.user)
    except Participant.DoesNotExist:
        participant = None

    if request.method == 'POST':
        form = ParticipationForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data['item']
            if Application.objects.filter(participant=participant, item=item).exists():
                messages.error(request, "Already applied for this item!")
                return redirect('user_profile')
            Application.objects.create(
                    participant=participant,
                    item=item,
                    status=Application.PENDING,
			)
            return redirect('user_profile')
    else:
        form = ParticipationForm()
    items = Item.objects.all()
    applied_items = Application.objects.filter(participant=participant)
    return render(request, 'accounts/profile.html', {'participant': participant, 'items': items, 'applied_items': applied_items, 'form': form})

@login_required(login_url="/app/login/")
def remove_item_view(request, pk):
    if request.method == 'POST':
         participant = Participant.objects.get(user=request.user)
         items = participant.individual_items.all()
         for item in items:
              if item.id == pk:
                    participant.individual_items.remove(item)
    return redirect('user_profile')

def create_forgot_link(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_link = f"https://sargam.cusat.ac.in{reverse('reset_password', kwargs={'uidb64': uid, 'token': token})}"
    return verification_link

def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password == confirm_password:
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user)  # Update session to prevent logout
                messages.success(request, "Your password has been reset successfully.")
                return redirect("user_login")  # Redirect to login page
            else:
                messages.error(request, "Passwords don't match!")

        # Pass uidb64 and token to the template context
        return render(request, "accounts/user_reset.html", {
            'uidb64': uidb64,
            'token': token,
        })

    messages.error(request, "The password reset link is invalid or has expired.")
    return redirect("user_forgot")

def user_forgot_view(request):
     if request.method == "POST":
        try:
             user = User.objects.get(email=request.POST['email'])
        except:
          user = None
        if user:
            send_mail(
    			subject="Sargam Password Reset",
    			message=f"Click this link to reset your password: {create_forgot_link(user)}",
    			from_email=EMAIL_HOST_USER,
    			recipient_list=[request.POST['email']],
    			fail_silently=False,
			)
            messages.info(request, "A password reset link has been sent to your email.")
        else:
             messages.error(request, "Enter a register E-Mail!")
     return render(request, 'accounts/user_forgot.html')