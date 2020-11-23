from django.contrib import admin
from accounts.models import User,Category,Country,City,State,Service,Subcategory,Item,Review

admin.site.register(User, admin.ModelAdmin)
admin.site.register(Category, admin.ModelAdmin)
admin.site.register(Subcategory, admin.ModelAdmin)
admin.site.register(Item, admin.ModelAdmin)
admin.site.register(Country, admin.ModelAdmin)
admin.site.register(State, admin.ModelAdmin)
admin.site.register(City, admin.ModelAdmin)
admin.site.register(Service, admin.ModelAdmin)
admin.site.register(Review, admin.ModelAdmin)
