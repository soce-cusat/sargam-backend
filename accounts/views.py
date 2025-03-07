from django.shortcuts import render, HttpResponse, redirect
from django.utils.formats import FORMAT_SETTINGS
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import get_user_model, logout, login
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail
from base.models import IndividualItem
from config.settings.base import EMAIL_HOST_USER
from django.contrib.auth.decorators import login_required

from .models import Participant, Zone
from .forms import ParticipantRegistraionForm, ParticipationForm
from .models import Participant, Zone


User = get_user_model()

def create_verification_link(user):
	token = default_token_generator.make_token(user)
	uid = urlsafe_base64_encode(force_bytes(user.pk))
	verification_link = f"http://127.0.0.1:8000{reverse('verify_email', kwargs={'uidb64': uid, 'token': token})}"
	return verification_link

def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('<h1> verified</h1>')
    else:
        return HttpResponse('<h1> failled </h1>')

class RegistrationView(TemplateView):
	template_name = "accounts/reg_login.html"
	
	def get(self, request):
		form = ParticipantRegistraionForm()
		return render(request, self.template_name, {"form": form})

	def post(self, request):
		form = ParticipantRegistraionForm(request.POST, request.FILES)
		if form.is_valid():
			form_data = form.cleaned_data

			if form_data['password'] != form_data['confirm_password']:
				messages.error(request, "Passwords donot match!")
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
				is_active=False
			)
			new_user.save()

			Participant.objects.create(
				user=new_user,
				name=form_data['name'],
				email=form_data['email'],
				zone=Zone.objects.get(id=form_data['zone'].id),
				photo=request.FILES['photo'],
				studentid=form_data['studentid'],
				id_card=request.FILES['id_card']
			)
			send_mail(
    			subject="Sargam Application Verification",
    			message=f"Click this link to verify your Application: {create_verification_link(new_user)}",
    			from_email=EMAIL_HOST_USER,
    			recipient_list=[form_data['email']],
    			fail_silently=False,
			)
			return redirect('user_login')

		return render(request, self.template_name, {"form": form})

	
def user_login(request):
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
	
@login_required(login_url="/login/")
def user_logout(request):
    logout(request)
    return redirect('user_login')

@login_required(login_url="/login/")
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
            participant.individual_items.add(item)
            #messages.success(request, f"You have successfully applied for {item.item_name}.")
            return redirect('user_profile')
    else:
        form = ParticipationForm()

    items = IndividualItem.objects.all()
    applied_items = participant.individual_items.all() if participant else []
    return render(request, 'accounts/profile.html', {'participant': participant, 'items': items, 'applied_items': applied_items, 'form': form})

@login_required(login_url="/login/")
def remove_item_view(request, pk):
    if request.method == 'POST':
         participant = Participant.objects.get(user=request.user)
         items = participant.individual_items.all()
         for item in items:
              if item.id == pk:
                    participant.individual_items.remove(item)
    return redirect('user_profile')