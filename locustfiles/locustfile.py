"""
Locustfile for load testing store_manager.py
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import random
from locust import HttpUser, task, between

class FlaskAPIUser(HttpUser):
    # Wait time between requests (1-3 seconds)
    wait_time = between(1, 3)
        
    # Proportion 1:1, meaning 1/2 + 1/2
    # This means 50% calls to /highest-spenders, 50% calls to /best-sellers
    @task(1) 
    def highest_spenders(self):
        """Test GET /orders/reports/highest-spenders endpoint (read)"""
        with self.client.get("/orders/reports/highest-spenders", catch_response=True) as response:
            try:
                data = response.json()
                if response.status_code == 200: 
                    if str(type(data)) == "<class 'list'>":
                        response.success()
                    else:
                        response.failure("Le resultat n'est pas une liste : " + str(data))
                else:
                    response.failure(f"Erreur : {response.status_code} - {data.get('error', 'Unknown error')}")
            except ValueError:
                response.failure(f"Invalid JSON response: {response.text}, code {response.status_code}")

    @task(1) 
    def best_sellers(self):
        """Test GET /orders/reports/best-sellers endpoint (read)"""
        with self.client.get("/orders/reports/best-sellers", catch_response=True) as response:
            try:
                data = response.json()
                if response.status_code == 200: 
                    if str(type(data)) == "<class 'list'>":
                        response.success()
                    else:
                        response.failure("Le resultat n'est pas une liste : " + str(data))
                else:
                    response.failure(f"Erreur : {response.status_code} - {data.get('error', 'Unknown error')}")
            except ValueError:
                response.failure(f"Invalid JSON response: {response.text}, {response.status_code}")
        # Proportion d'exécution 1:1:1, ce qui donne 66% lectures (2 méthodes) et 33% écritures (1 méthode)
    @task(1) 
    def orders(self):
        """Test POST /orders endpoint (write)"""
        # TODO: ajoutez des IDs aléatoires de 1-3
        user_id = random.randint(1, 3)
        product_id = random.randint(1, 4)
        quantity = random.randint(1, 5)
        
        mock_order = {
            "user_id": user_id,
            "items": [{"product_id": product_id, "quantity": quantity}] 
        }   

        # Ajouter aléatoirement plusiers articles (30 % des fois)
        if random.randint(1, 10) <= 3:
            # TODO: ajoutez des IDs aléatoires de 1-4
            mock_order["items"].append({"product_id": random.randint(1, 4), "quantity": random.randint(1, 3)})
            mock_order["items"].append({"product_id": random.randint(1, 4), "quantity": random.randint(1, 3)})

        with self.client.post("/orders", 
                            json=mock_order, 
                            headers={"Content-Type": "application/json"},
                            catch_response=True) as response:
            try:
                data = response.json()
                if response.status_code == 201:
                    if "order_id" in data:
                        response.success()
                    else:
                        response.failure("Aucun ID renvoyé pour la commande créée")
                else:
                    response.failure(f"Erreur : {response.status_code} - {data.get('error', 'Unknown error')}")
            except ValueError:
                response.failure(f"Invalid JSON response: {response.text}")