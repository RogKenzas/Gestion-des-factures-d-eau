import customtkinter as ctk
from controllers.client_controller import ClientController

class ClientView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.pack(fill="both", expand=True)

        title_label = ctk.CTkLabel(self, text="Espace Client", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        self.label_compteur = ctk.CTkLabel(self, text="Entrer votre n° de compteur :")
        self.label_compteur.pack(pady=5)

        self.entry_compteur = ctk.CTkEntry(self)
        self.entry_compteur.pack(pady=5)

        self.button_rechercher = ctk.CTkButton(self, text="Rechercher Factures",
                                               command=self.afficher_factures)
        self.button_rechercher.pack(pady=5)

        self.factures_textbox = ctk.CTkTextbox(self, width=400, height=200)
        self.factures_textbox.pack(pady=10)

    def afficher_factures(self):
        """Récupère et affiche les factures du client correspondant au n° de compteur."""
        compteur = self.entry_compteur.get()
        if not compteur:
            return

        factures = ClientController.get_factures_by_compteur(compteur)
        self.factures_textbox.delete("0.0", "end")

        if len(factures) == 0:
            self.factures_textbox.insert("end", "Aucune facture trouvée pour ce compteur.\n")
            return

        for f in factures:
            conso = f["index_final"] - f["index_initial"]
            texte = (f"FactureID : {f['facture_id']}\n"
                     f"Consommation : {conso} m³\n"
                     f"Montant : {f['montant']}\n"
                     f"Statut : {f['statut']}\n"
                     "----------------------------------\n")
            self.factures_textbox.insert("end", texte)
