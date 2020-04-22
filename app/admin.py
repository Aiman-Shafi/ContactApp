from django.contrib import admin
from django.contrib.auth.models import Group
from import_export.admin import ImportExportModelAdmin


# Register your models here.

from .models import Contact

# CLASS EDITNG THE CONTACT TABLE

class ContactTable(ImportExportModelAdmin):

	list_display = ('id', 'name', 'email' , 'gender', 'phone', 'info', 'date_added', )
	list_editable = ( 'info' ,)
	list_per_page = 5
	search_fields = ('name', 'email' , 'gender', 'info', 'phone',)
	list_filter = ( 'gender', 'date_added' ,)

# ADMIN RESIGTERS	

admin.site.register(Contact,ContactTable)
admin.site.unregister(Group)

