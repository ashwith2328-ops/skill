from django.contrib import admin
from .models import (
    SkillCategory,
    Skill,
    PlacementRole,
    RoleSkillRequirement,
    UserProfile,
    UserSkill,
)


class RoleSkillRequirementInline(admin.TabularInline):
    model = RoleSkillRequirement
    extra = 1


class UserSkillInline(admin.TabularInline):
    model = UserSkill
    extra = 1


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']


@admin.register(PlacementRole)
class PlacementRoleAdmin(admin.ModelAdmin):
    list_display = ['title', 'company_or_domain']
    inlines = [RoleSkillRequirementInline]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'updated_at']
    inlines = [UserSkillInline]
