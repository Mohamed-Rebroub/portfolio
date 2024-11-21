# mon_application/models.py
from django.db import models  # type: ignore
from django.utils import timezone  # type: ignore


class CVFile(models.Model):
    fichier = models.FileField(upload_to="media/media/cvs/")
    date_upload = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)  # Ensure this field is here

    class Meta:
        verbose_name = "CV"
        verbose_name_plural = "CVs"

    def __str__(self):
        return self.fichier.name


class Education(models.Model):
    school_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    option = models.CharField(max_length=255)
    start_year = models.IntegerField()
    end_year = models.IntegerField()

    def __str__(self):
        return f"{self.school_name} ({self.option})"


class Work(models.Model):
    position = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    duration = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return f"{self.position} at {self.company_name}"


# Model for skill categories (e.g., Microsoft Office, Framework, etc.)
class SkillCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Skill Category"
        verbose_name_plural = "Skill Categories"

    def __str__(self):
        return self.name


# Model for individual skills associated with categories
class Skill(models.Model):
    category = models.ForeignKey(
        SkillCategory, on_delete=models.CASCADE, related_name="skills"
    )
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def __str__(self):
        return self.name


from django.db import models
from django.utils import timezone


class Project(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to="projects/images/"
    )  # Chemin de stockage des images
    github_url = models.URLField(blank=True, null=True)  # Lien GitHub
    live_url = models.URLField(blank=True, null=True)  # Lien pour le site en ligne
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"

    def __str__(self):
        return self.name


from django.db import models


class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.TextField(
        help_text="Liste des fonctionnalités séparées par des virgules."
    )
    stripe_price_id = models.CharField(
        max_length=200, blank=True, null=True, help_text="L'identifiant du prix Stripe."
    )

    def __str__(self):
        return self.title
