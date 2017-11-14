from django.contrib import admin

from .models import User, UserForm, Role, CostCenter, PartType, Part, Place
from .models import WorkPattern, WorkPatternGroup
from .models import Work, WorkGroup
from .models import EventStatus, Event
from .models import WorkType
from .models import Manufacturer
from .models import Period
from .models import File
from .models import EventReport


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
admin.site.register(WorkPattern)
admin.site.register(WorkPatternGroup)
admin.site.register(Work)
admin.site.register(WorkGroup)
admin.site.register(EventStatus)
admin.site.register(Event)
admin.site.register(Manufacturer)
admin.site.register(Period)
admin.site.register(File)
admin.site.register(EventReport)
