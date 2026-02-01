from django.db import models


class SkillCategory(models.Model):
    """Category for grouping skills (e.g., Programming, Soft Skills)."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Skill categories'

    def __str__(self):
        return self.name


class Skill(models.Model):
    """A skill that can be required by roles or possessed by users."""
    name = models.CharField(max_length=150)
    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='skills'
    )
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return self.name


class PlacementRole(models.Model):
    """A placement/job role with required skills."""
    title = models.CharField(max_length=200)
    company_or_domain = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    required_skills = models.ManyToManyField(
        Skill,
        through='RoleSkillRequirement',
        related_name='placement_roles',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class RoleSkillRequirement(models.Model):
    """Links a role to a skill with optional proficiency level."""
    role = models.ForeignKey(PlacementRole, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency = models.CharField(
        max_length=20,
        choices=[
            ('basic', 'Basic'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('expert', 'Expert'),
        ],
        default='intermediate'
    )
    is_mandatory = models.BooleanField(default=True)

    class Meta:
        unique_together = ['role', 'skill']

    def __str__(self):
        return f"{self.role.title} — {self.skill.name} ({self.proficiency})"


class UserProfile(models.Model):
    """Stores a user's self-assessed skills for gap analysis."""
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    skills = models.ManyToManyField(
        Skill,
        through='UserSkill',
        related_name='user_profiles',
        blank=True
    )

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.name


class UserSkill(models.Model):
    """Links a user profile to a skill with self-assessed proficiency."""
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency = models.CharField(
        max_length=20,
        choices=[
            ('basic', 'Basic'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('expert', 'Expert'),
        ],
        default='basic'
    )

    class Meta:
        unique_together = ['profile', 'skill']

    def __str__(self):
        return f"{self.profile.name} — {self.skill.name} ({self.proficiency})"
