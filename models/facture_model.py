class Facture:
    def __init__(self, facture_id, client_id, index_initial, index_final, montant, statut="impayée"):
        self.facture_id = facture_id
        self.client_id = client_id
        self.index_initial = index_initial
        self.index_final = index_final
        self.montant = montant
        self.statut = statut

    def to_dict(self):
        return {
            "facture_id": self.facture_id,
            "client_id": self.client_id,
            "index_initial": self.index_initial,
            "index_final": self.index_final,
            "montant": self.montant,
            "statut": self.statut
        }

    @staticmethod
    def from_dict(data):
        return Facture(
            data["facture_id"],
            data["client_id"],
            data["index_initial"],
            data["index_final"],
            data["montant"],
            data.get("statut", "impayée")
        )
