from django.shortcuts import render, get_object_or_404, redirect
from .models import Contact
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Create your views here.
from .forms import CreateUserForm


def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')
			

		context = {'form':form}
		return render(request, 'app/register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'app/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')



# @login_required(login_url='login')
# def home(request):

#	context = {

#		'contacts': Contact.objects.all()

#	}

#	def get_queryset(self):

#		return render(request, 'app/index.html', context)

class HomePageView(LoginRequiredMixin, ListView):

	model = Contact
	template_name = 'app/index.html'
	context_object_name = 'contacts'

	def get_queryset(self):

		contacts = super().get_queryset()
		return contacts.filter(manager=self.request.user) 


		


@login_required(login_url='login')
def search(request):
	if request.GET:
		search_term = request.GET['search_term']
		search_result = Contact.objects.filter( 

			Q(name__icontains = search_term)|
			Q(email__icontains = search_term)|
			Q(info__icontains = search_term)|
			Q(phone__iexact = search_term)
			
			)
		
		context = {

			'search_output': search_term,
			'contacts' : search_result.filter(manager=request.user)

		}
		return render(request, 'app/search.html', context)
	
	else:

		return redirect('home')	


@login_required(login_url='login')
def detail(request, id):
	context = {

		'contact': get_object_or_404(Contact,pk=id)

	}
	return render(request, 'app/detail.html' , context)



class ContactCreateView(LoginRequiredMixin,CreateView):

	model = Contact
	template_name = 'app/create.html'
	fields = ['name', 'phone', 'email' , 'info', 'gender', 'image',]
	
	def form_valid(self, form):

		instance = form.save(commit= False)
		instance.manager = self.request.user
		instance.save()
		return redirect ('home')




class ContactUpdateView(LoginRequiredMixin,UpdateView):

	model = Contact
	template_name = 'app/update.html'
	fields = ['name', 'phone', 'email' , 'info', 'gender', 'image',]
	
	def form_valid(self, form):

		instance = form.save()
		return redirect ('detail', instance.pk)



class ContactDeleteView(LoginRequiredMixin,DeleteView):

	model = Contact
	template_name = 'app/delete.html'
	success_url = '/'
