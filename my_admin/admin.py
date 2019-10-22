from django.contrib import admin


# Register your models here.
from my_admin.models import *

admin.site.register(Program)
admin.site.register(Plo)
admin.site.register(Slo)
admin.site.register(Course)
admin.site.register(Clo)
admin.site.register(Role)
admin.site.register(Student)
admin.site.register(Semester)
admin.site.register(Section)
admin.site.register(AssessmentTool)
admin.site.register(Assessment)
