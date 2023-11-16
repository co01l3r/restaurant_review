from django.contrib import admin
from .models import Restaurant, Review, Customer, Visit

admin.site.register(Restaurant)
admin.site.register(Review)
admin.site.register(Customer)
admin.site.register(Visit)
