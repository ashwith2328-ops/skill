from django import forms
from .models import UserProfile, Skill, PlacementRole, UserSkill

PROFICIENCY_LEVELS = [
    ('', 'Select level'),
    ('basic', 'Basic'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
    ('expert', 'Expert'),
]


class ProfileForm(forms.ModelForm):
    """Form for creating/editing a user profile."""
    class Meta:
        model = UserProfile
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'your@email.com',
            }),
        }


class SkillGapAnalyzerForm(forms.Form):
    """Form for selecting a role and optionally a profile to analyze."""
    role = forms.ModelChoiceField(
        queryset=PlacementRole.objects.all(),
        empty_label='Select a placement role',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    profile = forms.ModelChoiceField(
        queryset=UserProfile.objects.all(),
        required=False,
        empty_label='Select your profile (or add skills below)',
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class InlineSkillForm(forms.Form):
    """Form for adding skills inline (skill + proficiency)."""
    skill = forms.ModelChoiceField(
        queryset=Skill.objects.all().order_by('category', 'name'),
        empty_label='Select a skill',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    proficiency = forms.ChoiceField(
        choices=PROFICIENCY_LEVELS,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
