from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView
from .models import PlacementRole, UserProfile, Skill, RoleSkillRequirement, UserSkill
from .forms import ProfileForm, SkillGapAnalyzerForm


def home(request):
    """Landing page with quick analyze CTA."""
    roles_count = PlacementRole.objects.count()
    skills_count = Skill.objects.count()
    return render(request, 'skill_gap/home.html', {
        'roles_count': roles_count,
        'skills_count': skills_count,
    })


def analyze(request):
    """Skill gap analysis: compare profile or manual skills vs role requirements."""
    form = SkillGapAnalyzerForm(request.GET or None)
    role = None
    profile = None
    gap_data = None
    role_requirements = []

    if form.is_valid():
        role = form.cleaned_data.get('role')
        profile = form.cleaned_data.get('profile')
        if role:
            requirements = RoleSkillRequirement.objects.filter(role=role).select_related('skill')
            role_requirements = list(requirements)
            user_skill_map = {}
            if profile:
                for us in UserSkill.objects.filter(profile=profile).select_related('skill'):
                    user_skill_map[us.skill_id] = us.proficiency
            gap_data = []
            proficiency_order = {'basic': 1, 'intermediate': 2, 'advanced': 3, 'expert': 4}
            for req in role_requirements:
                user_level = user_skill_map.get(req.skill_id)
                required_level = proficiency_order.get(req.proficiency, 0)
                user_level_num = proficiency_order.get(user_level, 0) if user_level else 0
                status = 'met' if user_level_num >= required_level else 'gap'
                gap_data.append({
                    'skill': req.skill,
                    'required_proficiency': req.proficiency,
                    'your_proficiency': user_level or '—',
                    'status': status,
                    'is_mandatory': req.is_mandatory,
                })

    return render(request, 'skill_gap/analyze.html', {
        'form': form,
        'role': role,
        'profile': profile,
        'gap_data': gap_data or [],
        'role_requirements': role_requirements,
    })


def roles_list(request):
    """List all placement roles."""
    roles = PlacementRole.objects.prefetch_related('required_skills').all()
    return render(request, 'skill_gap/roles_list.html', {'roles': roles})


def role_detail(request, pk):
    """Detail view for a placement role and its required skills."""
    role = get_object_or_404(PlacementRole, pk=pk)
    requirements = RoleSkillRequirement.objects.filter(role=role).select_related('skill')
    return render(request, 'skill_gap/role_detail.html', {
        'role': role,
        'requirements': requirements,
    })


def profiles_list(request):
    """List user profiles (for demo; in production would be per-user)."""
    profiles = UserProfile.objects.all()
    return render(request, 'skill_gap/profiles_list.html', {'profiles': profiles})


def profile_create(request):
    """Create a new user profile."""
    form = ProfileForm(request.POST or None)
    if form.is_valid():
        profile = form.save()
        return redirect('skill_gap:profile_detail', pk=profile.pk)
    return render(request, 'skill_gap/profile_form.html', {'form': form, 'title': 'Create Profile'})


def profile_detail(request, pk):
    """View and manage a user profile and their skills."""
    profile = get_object_or_404(UserProfile, pk=pk)
    user_skills = UserSkill.objects.filter(profile=profile).select_related('skill')
    return render(request, 'skill_gap/profile_detail.html', {
        'profile': profile,
        'user_skills': user_skills,
    })


def skills_list(request):
    """List all skills by category."""
    from django.db.models import Prefetch
    categories = SkillCategory.objects.prefetch_related(
        Prefetch('skills', queryset=Skill.objects.all())
    ).order_by('order', 'name')
    uncategorized = Skill.objects.filter(category__isnull=True)
    return render(request, 'skill_gap/skills_list.html', {
        'categories': categories,
        'uncategorized': uncategorized,
    })
