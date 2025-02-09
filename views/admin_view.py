import customtkinter as ctk
from controllers.admin_controller import AdminController
from views.invoice_view import InvoicePreview

class AdminView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.pack(fill="both", expand=True)

        title_label = ctk.CTkLabel(self, text="Espace Administrateur",
                                   font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        # ----------- GESTION DES CLIENTS -----------
        self.frame_clients = ctk.CTkFrame(self)
        self.frame_clients.pack(pady=5, padx=5, fill="x")

        # Nom
        self.label_nom = ctk.CTkLabel(self.frame_clients, text="Nom :")
        self.label_nom.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nom = ctk.CTkEntry(self.frame_clients)
        self.entry_nom.grid(row=0, column=1, padx=5, pady=5)

        # Adresse
        self.label_adresse = ctk.CTkLabel(self.frame_clients, text="Adresse :")
        self.label_adresse.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_adresse = ctk.CTkEntry(self.frame_clients)
        self.entry_adresse.grid(row=1, column=1, padx=5, pady=5)

        # Compteur
        self.label_compteur = ctk.CTkLabel(self.frame_clients, text="N° Compteur :")
        self.label_compteur.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_compteur = ctk.CTkEntry(self.frame_clients)
        self.entry_compteur.grid(row=2, column=1, padx=5, pady=5)

        # Boutons
        self.button_ajouter = ctk.CTkButton(self.frame_clients,
                                            text="Ajouter Client",
                                            command=self.ajouter_client)
        self.button_ajouter.grid(row=3, column=0, padx=5, pady=5)

        self.button_refresh_clients = ctk.CTkButton(self.frame_clients,
                                                    text="Rafraîchir Liste Clients",
                                                    command=self.refresh_clients_list)
        self.button_refresh_clients.grid(row=3, column=1, padx=5, pady=5)

        # Zone de texte pour afficher la liste des clients
        self.clients_textbox = ctk.CTkTextbox(self, width=400, height=150)
        self.clients_textbox.pack(pady=5)

        # ----------- GESTION DES FACTURES -----------
        self.frame_factures = ctk.CTkFrame(self)
        self.frame_factures.pack(pady=5, fill="x")

        self.label_client_id = ctk.CTkLabel(self.frame_factures, text="Client ID :")
        self.label_client_id.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_client_id = ctk.CTkEntry(self.frame_factures)
        self.entry_client_id.grid(row=0, column=1, padx=5, pady=5)

        self.label_index_initial = ctk.CTkLabel(self.frame_factures, text="Index Initial :")
        self.label_index_initial.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_index_initial = ctk.CTkEntry(self.frame_factures)
        self.entry_index_initial.grid(row=1, column=1, padx=5, pady=5)

        self.label_index_final = ctk.CTkLabel(self.frame_factures, text="Index Final :")
        self.label_index_final.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_index_final = ctk.CTkEntry(self.frame_factures)
        self.entry_index_final.grid(row=2, column=1, padx=5, pady=5)

        self.button_generer_facture = ctk.CTkButton(self.frame_factures,
                                                    text="Générer Facture",
                                                    command=self.generer_facture)
        self.button_generer_facture.grid(row=3, column=0, padx=5, pady=5)

        self.button_refresh_factures = ctk.CTkButton(self.frame_factures,
                                                     text="Rafraîchir Liste Factures",
                                                     command=self.refresh_factures_list)
        self.button_refresh_factures.grid(row=3, column=1, padx=5, pady=5)

        # Zone de texte pour lister les factures
        self.factures_textbox = ctk.CTkTextbox(self, width=400, height=150)
        self.factures_textbox.pack(pady=5)

    def ajouter_client(self):
        """Ajout d'un client via le contrôleur AdminController."""
        nom = self.entry_nom.get()
        adresse = self.entry_adresse.get()
        compteur = self.entry_compteur.get()

        if not nom or not adresse or not compteur:
            return

        AdminController.ajouter_client(nom, adresse, compteur)
        self.refresh_clients_list()

        # Nettoyage des champs
        self.entry_nom.delete(0, "end")
        self.entry_adresse.delete(0, "end")
        self.entry_compteur.delete(0, "end")

    def refresh_clients_list(self):
        """Récupère et affiche la liste des clients."""
        self.clients_textbox.delete("0.0", "end")
        clients = AdminController.get_all_clients()
        for c in clients:
            ligne = f"{c['client_id']} | {c['nom']} | {c['adresse']} | {c['compteur']}\n"
            self.clients_textbox.insert("end", ligne)

    from views.invoice_view import InvoicePreview

    def generer_facture(self):
        """Génère une facture pour un client et ouvre l'aperçu de facture."""
        client_id = self.entry_client_id.get()
        index_init = self.entry_index_initial.get()
        index_fin = self.entry_index_final.get()

        if not client_id or not index_init or not index_fin:
            return

        try:
            index_init = int(index_init)
            index_fin = int(index_fin)
        except ValueError:
            return 

        # Génére la facture et récupère son ID
        facture_id = AdminController.generer_facture(client_id, index_init, index_fin)

        # Rafraîchit la liste, si on veut
        self.refresh_factures_list()

        # Nettoyage des champs
        self.entry_client_id.delete(0, "end")
        self.entry_index_initial.delete(0, "end")
        self.entry_index_final.delete(0, "end")

        # Ouvre la fenêtre d'aperçu en lui passant l'ID de la facture
        InvoicePreview(self.master, facture_id)

    def refresh_factures_list(self):
        """Récupère et affiche la liste des factures."""
        self.factures_textbox.delete("0.0", "end")
        factures = AdminController.get_all_factures()
        for f in factures:
            conso = f["index_final"] - f["index_initial"]
            ligne = (f"{f['facture_id']} | Client: {f['client_id']} | "
                     f"Conso: {conso} m³ | Montant: {f['montant']} | Statut: {f['statut']}\n")
            self.factures_textbox.insert("end", ligne)
