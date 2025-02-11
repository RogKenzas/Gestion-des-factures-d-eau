import customtkinter as ctk
from tkinter import messagebox
from views.admin_view import AdminView
from views.client_view import ClientView

class PasswordWindow(ctk.CTkToplevel):
    def __init__(self, master, callback, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Saisir le mot de passe")
        self.geometry("300x190")
        self.resizable(False, False)
        
        self.callback = callback
        
        self.label = ctk.CTkLabel(self, text="Veuillez entrer le mot de passe administrateur:", font=("Arial", 12))
        self.label.pack(pady=20)
        
        self.password_entry = ctk.CTkEntry(self, show="*", width=200)
        self.password_entry.pack(pady=10)
        
        # Bouton de validation
        self.submit_button = ctk.CTkButton(self, text="Valider", command=self.check_password)
        self.submit_button.pack(pady=10)

    def check_password(self):
        password = self.password_entry.get()
        if password == "root": #Modifie si tu veux hein !!!
            self.callback()
            self.destroy()
        else:
            messagebox.showerror("Erreur", "Mot de passe incorrect. Veuillez réessayer.")
            self.password_entry.delete(0, ctk.END)

class LoginView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.pack(fill="both", expand=True)

        title_label = ctk.CTkLabel(self, text="Bienvenue sur l'application de facturation d'eau",
                                   font=("Arial", 16))
        title_label.pack(pady=20)

        admin_button = ctk.CTkButton(self, text="Espace Administrateur", command=self.ask_password_and_go_admin)
        admin_button.pack(pady=10)

        client_button = ctk.CTkButton(self, text="Espace Client", command=self.go_client)
        client_button.pack(pady=10)

    def ask_password_and_go_admin(self):
        # Crée une fenêtre modale pour la saisie du mot de passe
        PasswordWindow(self.master, self.go_to_admin)

    def go_to_admin(self):
        # Si le mot de passe est correct, redirige vers l'admin
        self.destroy()
        AdminView(self.master)

    def go_client(self):
        # Redirige vers l'espace client sans mot de passe
        self.destroy()
        ClientView(self.master)
