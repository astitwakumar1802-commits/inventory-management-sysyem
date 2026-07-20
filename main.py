import subprocess
import sys
import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MasterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DVC System Portal")
        
        # 👑 लॉगिन पेज को भी फुल स्क्रीन (Maximize) करने के लिए यहाँ सेट किया है
        self.state('zoomed')
        
        self.show_login_screen()

    def show_login_screen(self):
        self.clear_window()
        
        # फुल स्क्रीन में एलिमेंट्स बीच में अच्छे लगें इसलिए पैडिंग (pady) बढ़ा दी है
        ctk.CTkLabel(self, text="🔑 SYSTEM SECURE LOGIN", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(150, 25))
        
        self.entry_uid = ctk.CTkEntry(self, placeholder_text="Enter User ID", width=300, height=40)
        self.entry_uid.pack(pady=10)
        
        self.entry_pwd = ctk.CTkEntry(self, placeholder_text="Enter Password", show="*", width=300, height=40)
        self.entry_pwd.pack(pady=10)
        
        ctk.CTkButton(self, text="Login to System", command=self.check_login, width=300, height=45).pack(pady=20)

    def check_login(self):
        uid = self.entry_uid.get().strip()
        pwd = self.entry_pwd.get().strip()
        
        if uid == "admin" and pwd == "AKS@18":
            messagebox.showinfo("Success", "Welcome to the System!")
            self.show_launcher_screen()
        else:
            messagebox.showerror("Access Denied", "Invalid User ID or Password!")

    def show_launcher_screen(self):
        self.clear_window()
        
        ctk.CTkLabel(
            self, 
            text="🎉 WELCOME TO THE SYSTEM", 
            text_color="#4CAF50", 
            font=ctk.CTkFont(size=26, weight="bold")
        ).pack(pady=(120, 20))
        
        ctk.CTkLabel(self, text="Select your preferred mode to continue:", font=ctk.CTkFont(size=16)).pack(pady=5)

        ctk.CTkButton(self, text="🖥️ Launch GUI Version (Modern)", command=self.launch_gui, width=350, height=50).pack(pady=20)

        ctk.CTkButton(self, text="⌨️ Launch CUI Version (Console)", command=self.launch_cui, width=350, height=50, fg_color="#2b7a78", hover_color="#174d4c").pack(pady=10)

    def launch_gui(self):
        subprocess.Popen([sys.executable, "gui_inventory.py"])

    def launch_cui(self):
        if sys.platform.startswith("win"):
            subprocess.Popen(["cmd", "/c", "start", "python", "inventory.py"])
        else:
            subprocess.Popen(["open", "-a", "Terminal", "python", "inventory.py"])

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = MasterApp()
    app.mainloop()

