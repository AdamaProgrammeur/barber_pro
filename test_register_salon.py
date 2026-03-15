import requests

url = "https://barber-pro-upue.onrender.com/accounts/api/register-salon/"

payload = {
    "username": "client_test1",
    "email": "client_test1@example.com",
    "password": "Password123",
    "first_name": "Client",
    "last_name": "Test",

    "salon_nom": "Salon Test",
    "salon_adresse": "",
    "salon_telephone": "",
    "salon_email": "",
    "salon_localisation": "",
    "max_postes": 1
}

headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, json=payload, headers=headers, timeout=30)

    print("Status code:", response.status_code)

    try:
        print("Réponse JSON:", response.json())
    except Exception as e:
        print("Erreur JSON:", e)
        print("Texte brut du serveur:", response.text)

except requests.exceptions.RequestException as e:
    print("Erreur de connexion ou timeout :", e)