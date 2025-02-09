from utils import data_manager

class ClientController:
    """
    Gère la logique côté client :
    - Récupère la liste des factures par numéro de compteur
    - Permet éventuellement de payer une facture
    """

    @staticmethod
    def get_client_by_compteur(numero_compteur):
        clients_data = data_manager.load_clients()
        for client in clients_data:
            if client["compteur"] == numero_compteur:
                return client
        return None

    @staticmethod
    def get_factures_by_compteur(numero_compteur):
        """
        Retrouve un client par son compteur
        et renvoie la liste de toutes ses factures.
        """
        client = ClientController.get_client_by_compteur(numero_compteur)
        if not client:
            return []
        
        factures_data = data_manager.load_factures()
        # Filtrer par client_id
        client_factures = [f for f in factures_data if f["client_id"] == client["client_id"]]
        return client_factures

    @staticmethod
    def payer_facture(facture_id):
        """
        Change le statut d'une facture en 'payée'.
        Optionnel, selon si vous voulez implémenter la notion de paiement.
        """
        factures_data = data_manager.load_factures()
        for facture in factures_data:
            if facture["facture_id"] == facture_id:
                facture["statut"] = "payée"
                break
        data_manager.save_factures(factures_data)
