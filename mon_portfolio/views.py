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


import stripe
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from .models import Service

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": service.stripe_price_id,  # ID Stripe Price
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=request.build_absolute_uri("/?success=true"),
            cancel_url=request.build_absolute_uri("/?canceled=true"),
        )
        return redirect(checkout_session.url)
    except stripe.error.StripeError as e:
        print(f"StripeError: {str(e)}")  # Log de l'erreur Stripe
        return redirect("/?error=true")
    except Exception as e:
        print(f"Erreur générale : {str(e)}")  # Log des erreurs générales
        return redirect("/?error=true")


import pandas as pd
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail

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


# Fonction de calcul de la distance de Levenshtein
def levenshtein_distance(str1, str2):
    m = len(str1)
    n = len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(
                    dp[i - 1][j - 1] + 1,  # Substitution
                    dp[i - 1][j] + 1,  # Suppression
                    dp[i][j - 1] + 1,  # Insertion
                )
    return dp[m][n]


# Fonction pour trouver la meilleure correspondance
def find_best_match(input_text, responses):
    threshold = 3  # Tolérance maximale
    best_match = None
    min_distance = float("inf")

    normalized_input = input_text.lower().strip()
    input_words = normalized_input.split()

    for key in responses.keys():
        key_words = key.lower().strip().split()
        total_distance = 0

        for input_word in input_words:
            min_word_distance = float("inf")
            for key_word in key_words:
                distance = levenshtein_distance(input_word, key_word)
                min_word_distance = min(min_word_distance, distance)
            total_distance += min_word_distance

        if total_distance < min_distance:
            min_distance = total_distance
            best_match = key

    return best_match if min_distance <= threshold * len(input_words) else None


# Vue principale
def index(request):
    if request.method == "POST":
        user_query = request.POST.get("query", "").strip()
        response = generate_response(user_query)
        return JsonResponse({"response": response})
    return render(request, "home.html")


# Fonction pour interagir avec Groq AI
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


def generate_response(query):
    query_lower = query.lower().strip()

    # Vérification de la longueur minimale
    if len(query_lower) < 3:
        return "Votre requête est trop courte. Veuillez préciser votre demande."

    # Vérification des services spécifiques
    best_service_match = find_best_match(query_lower, SERVICES)
    if best_service_match:
        service_details = SERVICES[best_service_match]
        return (
            f"Service : {best_service_match}.\n"
            f"Description : {service_details['description']}\n"
            f"Prix : {service_details['prix']}"
        )

    # Demande générale sur les services
    if "service" in query_lower or "services" in query_lower:
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
        if find_best_match(query_lower, {row["Université"]: None}):
            return (
                f"L'université {row['Université']} est située à {row['Adresse']}, "
                f"{row['Ville']}. Plus d'informations sur leur site : {row['Site Web']}."
            )

    # Réponses génériques
    generic_responses = {
        "contact": "Vous pouvez me contacter au +212 674156928 ou par email à mohamedrebroub815@gmail.com.",
        "localisation": "Je suis basé à Casablanca, Maroc.",
        "hi": "Bonjour ! Comment puis-je vous aider aujourd'hui ?",
        "hello": "Bonjour ! Comment puis-je vous aider aujourd'hui ?",
        "bonjour": "Bonjour ! Comment puis-je vous aider aujourd'hui ?",
        "salut": "Bonjour ! Comment puis-je vous aider aujourd'hui ?",
    }
    best_generic_match = find_best_match(query_lower, generic_responses)
    if best_generic_match:
        return generic_responses[best_generic_match]

    # Utiliser Groq AI pour des questions complexes
    groq_response = query_groq_ai(query)
    if groq_response != "Une erreur s'est produite lors de la connexion au service AI.":
        return groq_response

    # Réponse par défaut en cas d'erreur ou d'absence de correspondance
    return "Je ne suis pas sûr de comprendre votre demande. Pouvez-vous reformuler ?"


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
