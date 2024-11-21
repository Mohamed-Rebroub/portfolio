from django.contrib import admin  # type: ignore
from .models import CVFile
from .models import Education, Work, Skill, SkillCategory, Project, Service


admin.site.register(CVFile)

admin.site.register(Education)
admin.site.register(Work)

admin.site.register(Skill)
admin.site.register(SkillCategory)
admin.site.register(Project)
admin.site.register(Service)
