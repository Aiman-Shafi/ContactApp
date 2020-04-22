from django.urls import path
from . import views

urlpatterns = [
	
	path('', views.HomePageView.as_view(), name='home'),
	path('search/',views.search, name= 'search'),

	path('register/',views.registerPage, name= 'register'),
	path('login/',views.loginPage, name= 'login'),
	path('logout/',views.logoutUser, name= 'logout'),

	path('detail/<int:id>',views.detail, name= 'detail'),
	path('create/',views.ContactCreateView.as_view(), name='create'),
	path('delete/<int:pk>', views.ContactDeleteView.as_view(), name='delete'),
	path('update/<int:pk>', views.ContactUpdateView.as_view(), name='update'),

]

