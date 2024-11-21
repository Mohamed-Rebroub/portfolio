from django.shortcuts import render

# Create your views here.
# mon_application/views.py
from django.http import HttpResponse  # type: ignore
from django.shortcuts import render  # type: ignore
from django.shortcuts import get_object_or_404  # type: ignore
from django.http import FileResponse  # type: ignore
from .models import CVFile
from .models import Education, Work, SkillCategory, Skill

# mon_application/views.py


def simple_page(request):
    return render(request, "simple_page.html")


from django.shortcuts import render  # type: ignore

from .models import Project, Education, Work, Service


def home(request):
    if request.method == "POST":
        # Gestion de la requête chatbot
        user_query = request.POST.get("query", "").strip()
        response = generate_response(user_query)
        return JsonResponse({"response": response})

    # Chargement des données pour la page
    educations = Education.objects.all()
    work_experiences = Work.objects.all()
    projects = Project.objects.all()
    services = Service.objects.all()

    # Diviser les fonctionnalités pour chaque service
    for service in services:
        service.features_list = service.features.split(
            ","
        )  # Divise les fonctionnalités en liste

    return render(
        request,
        "home.html",
        {
            "educations": educations,
            "work_experiences": work_experiences,
            "projects": projects,
            "services": services,
        },
    )


# mon_application/views.py
from django.http import FileResponse  # type: ignore
from django.shortcuts import get_object_or_404  # type: ignore
from .models import CVFile


def download_cv(request):
    cv = get_object_or_404(
        CVFile, is_active=True
    )  # Cela devrait maintenant fonctionner si la migration est appliquée
    response = FileResponse(cv.fichier, as_attachment=True)
    return response


def simple_page(request):
    projects = Project.objects.all()  # Assurez-vous que ce modèle est défini
    return render(request, "simple_page.html", {"projects": projects})


import pandas as pd
import requests
from django.shortcuts import render
from django.http import JsonResponse

from groq import Groq

# Initialisation avec clé API
GROQ_AI_API_KEY = "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"

# Chemin vers le fichier CSV
csv_file_path = "universities.csv"
# Données statiques des services avec descriptions et prix
SERVICES = {
    "ui/ux design": {
        "description": "Je conçois des maquettes et prototypes haute fidélité pour des produits accessibles et performants.",
        "prix": "À partir de 3000 MAD",
    },
    "web development": {
        "description": "Création de sites web attrayants et responsives avec les dernières technologies.",
        "prix": "À partir de 5000 MAD",
    },
    "chatbots personnalisés": {
        "description": "Conception de chatbots sur mesure intégrant l'intelligence artificielle.",
        "prix": "À partir de 4000 MAD",
    },
    "modèles d'IA": {
        "description": "Développement de modèles d'intelligence artificielle performants et personnalisés.",
        "prix": "À partir de 8000 MAD",
    },
    "wordpress": {
        "description": "Développement et gestion de sites via WordPress, adapté à vos besoins.",
        "prix": "À partir de 2000 MAD",
    },
}

COMPETENCES = [
    "HTML, CSS, JavaScript",
    "Frameworks : .NET, Django, Spring Boot",
    "Bases de données : SQL Server, PostgreSQL",
    "Méthodologies : MERISE, UML, Agile",
]


# Chargement des données depuis un CSV
def load_csv_data(file_path):
    try:
        df = pd.read_csv(file_path, encoding="ISO-8859-1", sep=";")
        data = []
        for _, row in df.iterrows():
            data.append(
                {
                    "Université": row["Université"].strip().lower(),
                    "Adresse": row["Adresse"].strip(),
                    "Ville": row["Ville"].strip(),
                    "Site Web": row["Site"].strip(),
                    "Filières": row["Filières"].strip(),
                }
            )
        return data
    except Exception as e:
        print(f"Erreur lors du chargement du fichier CSV : {e}")
        return []


data = load_csv_data(csv_file_path)


# Vue principale
def index(request):
    if request.method == "POST":
        user_query = request.POST.get("query", "").strip()
        response = generate_response(user_query)
        return JsonResponse({"response": response})
    return render(request, "home.html")


## Fonction pour interagir avec Groq AI
def query_groq_ai(query):
    url = "https://api.groq.ai/v1/ask"
    headers = {
        "Authorization": f"Bearer {GROQ_AI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"query": query}
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get(
                "answer", "Je n'ai pas de réponse pour cette question."
            )
        else:
            print(f"Erreur API Groq AI: {response.status_code} - {response.text}")
            return "Je n'ai pas pu obtenir de réponse. Veuillez réessayer."
    except Exception as e:
        print(f"Erreur lors de l'appel à Groq AI: {e}")
        return "Une erreur s'est produite lors de la connexion au service AI."


# Génération des réponses
def generate_response(query):
    query_lower = query.lower().strip()

    # Vérification des services spécifiques
    for service, details in SERVICES.items():
        if service in query_lower:
            return (
                f"Service : {service}.\n"
                f"Description : {details['description']}\n"
                f"Prix : {details['prix']}"
            )

    # Demande générale sur les services
    if (
        "service" in query_lower
        or "services" in query_lower
        or "autres services" in query_lower
    ):
        all_services = "\n".join(
            [
                f"- {service}: {details['description']} (Prix : {details['prix']})"
                for service, details in SERVICES.items()
            ]
        )
        return (
            "Voici la liste de tous les services que je propose :\n" f"{all_services}"
        )

    # Vérification des compétences
    if "compétence" in query_lower or "compétences" in query_lower:
        return f"Mes compétences incluent : {', '.join(COMPETENCES)}."

    # Recherche dans les données CSV
    for row in data:
        if row["Université"] in query_lower:
            return (
                f"L'université {row['Université']} est située à {row['Adresse']}, "
                f"{row['Ville']}. Plus d'informations sur leur site : {row['Site Web']}."
            )

    # Réponses génériques
    if "contact" in query_lower:
        return "Vous pouvez me contacter au +212 674156928 ou par email à mohamedrebroub815@gmail.com."

    if "localisation" in query_lower:
        return "Je suis basé à Casablanca, Maroc."

    if any(greeting in query_lower for greeting in ["hi", "hello", "bonjour", "salut"]):
        return "Bonjour ! Comment puis-je vous aider aujourd'hui ?"

    # Utiliser Groq AI pour des questions complexes
    return query_groq_ai(query)


from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render

from django.shortcuts import render


def email_page(request):
    return render(request, "email2.html")


def send_email(request):
    if request.method == "POST":
        # Récupérer les données du formulaire
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        subject = request.POST.get("subject", "")
        message = request.POST.get("message", "")

        # Contenu complet du message
        full_message = f"Nom : {name}\nEmail : {email}\n\nMessage : {message}"

        try:
            # Envoi de l'e-mail
            send_mail(
                subject=subject,
                message=full_message,
                from_email="srebroub550@gmail.com",  # Votre adresse Gmail
                recipient_list=["destinataire@example.com"],  # Adresse du destinataire
                fail_silently=False,
            )
            return JsonResponse(
                {"status": "success", "message": "Email envoyé avec succès!"}
            )
        except Exception as e:
            return JsonResponse({"status": "error", "message": f"Erreur : {e}"})

    return JsonResponse({"status": "error", "message": "Requête invalide"})
