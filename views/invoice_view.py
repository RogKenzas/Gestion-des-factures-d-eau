import customtkinter as ctk
from datetime import datetime
from controllers.admin_controller import AdminController
from utils import data_manager
from fpdf import FPDF

class InvoicePreview(ctk.CTkToplevel):
    """
    Fenêtre d'aperçu d'une facture d'eau,
    basée sur la facture_id renvoyée par AdminController.
    """
    def __init__(self, master, facture_id):
        super().__init__(master)
        self.title("Aperçu de la Facture")
        self.geometry("600x500")
        self.facture_id = facture_id

        # Charger la facture depuis le data_manager
        self.facture_data = self.get_facture_data(facture_id)
        if not self.facture_data:
            # Si jamais on ne retrouve pas la facture, on affiche un message d'erreur
            ctk.CTkLabel(self, text="Facture introuvable!").pack(pady=20)
            return

        # Charger également les infos du client
        self.client_data = self.get_client_data(self.facture_data["client_id"])

        # Construire l'interface
        self.build_ui()

    def build_ui(self):
        """Construit l'interface d'aperçu de la facture."""
        ctk.CTkLabel(self, text="FACTURE D'EAU", font=("Arial", 18, "bold")).pack(pady=10)

        # --- Informations principales ---
        date_auj = datetime.now().strftime("%d/%m/%Y")

        # Frame pour regrouper infos
        info_frame = ctk.CTkFrame(self)
        info_frame.pack(pady=5, fill="x", padx=10)

        # Date du jour
        ctk.CTkLabel(info_frame, text=f"Date : {date_auj}", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=5)
        
        # Numéro de facture = facture_id
        ctk.CTkLabel(info_frame, text=f"N° Facture : {self.facture_data['facture_id']}", font=("Arial", 12)).grid(row=0, column=1, sticky="e", padx=5)

        # --- Infos Client ---
        client_frame = ctk.CTkFrame(self)
        client_frame.pack(pady=5, fill="x", padx=10)

        nom_client = self.client_data["nom"] if self.client_data else "Inconnu"
        adr_client = self.client_data["adresse"] if self.client_data else "N/A"

        ctk.CTkLabel(client_frame, text=f"Client : {nom_client}", font=("Arial", 12)).pack(anchor="w", pady=2)
        ctk.CTkLabel(client_frame, text=f"Adresse : {adr_client}", font=("Arial", 12)).pack(anchor="w", pady=2)

        # --- Détails de consommation ---
        details_frame = ctk.CTkFrame(self)
        details_frame.pack(pady=5, fill="x", padx=10)

        index_init = self.facture_data["index_initial"]
        index_fin = self.facture_data["index_final"]
        conso = index_fin - index_init
        montant = self.facture_data["montant"]
        statut = self.facture_data["statut"]

        ctk.CTkLabel(details_frame, text=f"Index initial : {index_init}", font=("Arial", 12)).pack(anchor="w", pady=2)
        ctk.CTkLabel(details_frame, text=f"Index final : {index_fin}", font=("Arial", 12)).pack(anchor="w", pady=2)
        ctk.CTkLabel(details_frame, text=f"Consommation : {conso} m³", font=("Arial", 12)).pack(anchor="w", pady=2)
        ctk.CTkLabel(details_frame, text=f"Montant : {montant} XAF", font=("Arial", 12, "bold")).pack(anchor="w", pady=2)
        ctk.CTkLabel(details_frame, text=f"Statut : {statut}", font=("Arial", 12)).pack(anchor="w", pady=2)

        # --- Bouton Export PDF ---
        export_btn = ctk.CTkButton(self, text="Exporter en PDF", command=self.exporter_pdf)
        export_btn.pack(pady=15)

    def get_facture_data(self, facture_id):
        """Retourne le dictionnaire correspondant à la facture_id."""
        all_factures = data_manager.load_factures()
        for f in all_factures:
            if f["facture_id"] == facture_id:
                return f
        return None

    def get_client_data(self, client_id):
        """Retourne le dictionnaire correspondant au client_id."""
        all_clients = data_manager.load_clients()
        for c in all_clients:
            if c["client_id"] == client_id:
                return c
        return None

    def exporter_pdf(self):
        """
        Génére un fichier PDF minimaliste de la facture
        en encodage cp1252 (windows-1252) pour supporter le symbole €.
        """
        date_auj = datetime.now().strftime("%d/%m/%Y")
        facture_id = self.facture_data["facture_id"]
        nom_client = self.client_data["nom"] if self.client_data else "Inconnu"
        adr_client = self.client_data["adresse"] if self.client_data else "N/A"
        index_init = self.facture_data["index_initial"]
        index_fin = self.facture_data["index_final"]
        conso = index_fin - index_init
        montant = self.facture_data["montant"]
        statut = self.facture_data["statut"]

        # Nom du fichier
        pdf_filename = f"Facture_{facture_id}.pdf"

        # Création d'un PDF FPDF
        pdf = FPDF()

        # pdf.set_doc_option("core_fonts_encoding", "windows-1252")

        pdf.add_page()
        pdf.set_font("Arial", style="", size=12)

        # Titre
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "FACTURE D'EAU", ln=1, align="C")

        # Date et Num Facture
        pdf.set_font("Arial", "", 12)
        pdf.cell(100, 10, f"Date : {date_auj}", ln=0)
        pdf.cell(0, 10, f"N° Facture : {facture_id}", ln=1, align="R")

        # Infos client
        pdf.ln(5)
        pdf.cell(0, 10, f"Client : {nom_client}", ln=1)
        pdf.cell(0, 10, f"Adresse : {adr_client}", ln=1)

        # Consommation
        pdf.ln(5)
        pdf.cell(0, 10, f"Index initial : {index_init}", ln=1)
        pdf.cell(0, 10, f"Index final : {index_fin}", ln=1)
        pdf.cell(0, 10, f"Consommation : {conso} m³", ln=1)

        # Montant
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"Montant : {montant} XAF", ln=1)
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Statut : {statut}", ln=1)
        
        pdf.ln(10)
        pdf.cell(0, 10, "Merci pour votre confiance.", ln=1)

        pdf.output(pdf_filename)

        confirm_label = ctk.CTkLabel(self, text=f"PDF enregistré : {pdf_filename}")
        confirm_label.pack(pady=5)
