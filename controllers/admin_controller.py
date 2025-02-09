import uuid
from utils import data_manager
from models.client_model import Client
from models.facture_model import Facture
from utils.config import TARIF_UNITAIRE

class AdminController:
    """
    Gère la logique pour les fonctionnalités Admin :
    - Ajout, modification, suppression de clients
    - Génération et consultation de factures
    """

    @staticmethod
    def ajouter_client(nom, adresse, compteur):
        clients_data = data_manager.load_clients()

        # Génération d'un ID unique pour le client
        client_id = str(uuid.uuid4())

        new_client = Client(
            client_id=client_id,
            nom=nom,
            adresse=adresse,
            compteur=compteur
        )
        
        # Convertir en dictionnaire pour l'enregistrer dans le JSON
        clients_data.append(new_client.to_dict())
        data_manager.save_clients(clients_data)

        return client_id

    @staticmethod
    def modifier_client(client_id, new_nom, new_adresse, new_compteur):
        clients_data = data_manager.load_clients()
        for client in clients_data:
            if client["client_id"] == client_id:
                client["nom"] = new_nom
                client["adresse"] = new_adresse
                client["compteur"] = new_compteur
                break
        data_manager.save_clients(clients_data)

    @staticmethod
    def supprimer_client(client_id):
        # Supprimer le client et toutes ses factures
        clients_data = data_manager.load_clients()
        factures_data = data_manager.load_factures()

        # Filtrer la liste pour retirer le client
        clients_data = [c for c in clients_data if c["client_id"] != client_id]
        
        # Filtrer les factures associées au client
        factures_data = [f for f in factures_data if f["client_id"] != client_id]

        data_manager.save_clients(clients_data)
        data_manager.save_factures(factures_data)

    @staticmethod
    def generer_facture(client_id, index_initial, index_final):
        factures_data = data_manager.load_factures()
        facture_id = str(uuid.uuid4())
        
        consommation = max(0, index_final - index_initial)
        montant = consommation * TARIF_UNITAIRE

        new_facture = Facture(
            facture_id=facture_id,
            client_id=client_id,
            index_initial=index_initial,
            index_final=index_final,
            montant=montant,
            statut="impayée"
        )
        factures_data.append(new_facture.to_dict())
        data_manager.save_factures(factures_data)

        return facture_id

    @staticmethod
    def get_all_clients():
        return data_manager.load_clients()

    @staticmethod
    def get_all_factures():
        return data_manager.load_factures()
