import customtkinter as ctk
from views.admin_view import AdminView
from views.client_view import ClientView

class LoginView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.pack(fill="both", expand=True)

        title_label = ctk.CTkLabel(self, text="Bienvenue sur l'application de facturation d'eau",
                                   font=("Arial", 16))
        title_label.pack(pady=20)

        admin_button = ctk.CTkButton(self, text="Espace Administrateur", command=self.go_admin)
        admin_button.pack(pady=10)

        client_button = ctk.CTkButton(self, text="Espace Client", command=self.go_client)
        client_button.pack(pady=10)

    def go_admin(self):
        self.destroy()
        AdminView(self.master)

    def go_client(self):
        self.destroy()
        ClientView(self.master)
