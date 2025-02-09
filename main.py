import customtkinter as ctk
from views.login_view import LoginView

def main():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Water Billing App")
    root.geometry("900x600")

    # Charger la première vue
    LoginView(root)

    root.mainloop()

if __name__ == "__main__":
    main()
