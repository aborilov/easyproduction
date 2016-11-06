from django.contrib import admin

from .models import User, UserForm, Role, CostCenter, PartType, Part, Place
from .models import WorkType


class UserAdmin(admin.ModelAdmin):
    search_fields = ['username']
    form = UserForm

admin.site.register(User, UserAdmin)
admin.site.register(Role)
admin.site.register(CostCenter)
admin.site.register(PartType)
admin.site.register(Part)
admin.site.register(Place)
admin.site.register(WorkType)
