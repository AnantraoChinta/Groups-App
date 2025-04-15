from django.contrib import admin

from .models import Profile, Relationship

# Register your models here.


# class PeopleListAdmin(admin.ModelAdmin):
#     # The fields of People List model being displayed in the admin view
#     list_filter = ['user']
#     list_display = ['user']
#     search_fields = ['user']
#     readonly_fields = ['user']
#     class Meta:
#         model = PeopleList

# admin.site.register(PeopleList, PeopleListAdmin)

# class RequestAdmin(admin.ModelAdmin):
#     list_filter = ['sender', 'receiver']
#     list_display = ['sender', 'receiver']
#     search_fields = ['sender__email', 'receiver__email']

#     class Meta:
#         model = Request
    
admin.site.register(Profile)
admin.site.register(Relationship)
