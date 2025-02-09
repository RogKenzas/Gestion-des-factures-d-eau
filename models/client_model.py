class Client:
    def __init__(self, client_id, nom, adresse, compteur):
        self.client_id = client_id
        self.nom = nom
        self.adresse = adresse
        self.compteur = compteur
    
    def to_dict(self):
        return {
            "client_id": self.client_id,
            "nom": self.nom,
            "adresse": self.adresse,
            "compteur": self.compteur
        }
    
    @staticmethod
    def from_dict(data):
        return Client(
            data["client_id"],
            data["nom"],
            data["adresse"],
            data["compteur"]
        )
