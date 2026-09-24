import tkinter as tk
from tkinter import ttk
import time
from emailManager import EmailManager

email_manager = EmailManager()

class TkinterManager():
    
    def __init__(self):
        self._verified = False
        self._settingsconfirmed = False
        self._speed = 5
        self._foodnum = 100
        self._preynum = 10
        self._predatornum = 0
        self.welcome_page = tk.Tk()
        self.welcome_page.title("Welcome!")
        self.welcome_page.geometry("400x400")
        self.centre_page(self.welcome_page)
        self.welcome_page.iconbitmap("Icon.ico")
        welcome_message = tk.Label(self.welcome_page, text = "Welcome to the simulation!")
        welcome_message.pack()
        login_choice = tk.Button(self.welcome_page, text = "Login", width = 30, command = self.open_login_page)
        login_choice.pack()
        new_account_choice = tk.Button(self.welcome_page, text = "Make New Account", width = 30, command = self.open_account_creation_page)
        new_account_choice.pack()
        self.welcome_page.mainloop()
    
    def centre_page(self,page):
        page.update_idletasks()
        page_width = page.winfo_width()
        page_height = page.winfo_height()
        user_screen_width = page.winfo_screenwidth()
        user_screen_height = page.winfo_screenheight()
        x = (user_screen_width - page_width) // 2
        y = (user_screen_height - page_height) // 2
        page.geometry(f"{page_width}x{page_height}+{x}+{y}")
        
    def open_settings_page(self):
        
        self.settings_page = tk.Tk()
        self.settings_page.title("Settings")
        self.settings_page.geometry("400x400")
        self.centre_page(self.settings_page)
        self.settings_page.iconbitmap("Icon.ico")
        settings_message = tk.Label(self.settings_page,text = "Change Settings here.")
        settings_message.pack()
        simulation_speed_label = tk.Label(self.settings_page,text = "Simulation Speed")
        simulation_speed_label.pack()
        simulation_speed_choice = ttk.Spinbox(self.settings_page, from_=1, to=10)
        simulation_speed_choice.pack()
        foodnum_label = tk.Label(self.settings_page,text = "Number of Food")
        foodnum_label.pack()
        foodnum_choice = ttk.Spinbox(self.settings_page, from_=1, to=100)
        foodnum_choice.pack()
        preynum_label = tk.Label(self.settings_page,text = "Number of Prey")
        preynum_label.pack()
        preynum_choice = ttk.Spinbox(self.settings_page, from_=1, to=100)
        preynum_choice.pack()
        predatornum_label = tk.Label(self.settings_page,text = "Number of Predators")
        predatornum_label.pack()
        predatornum_choice = ttk.Spinbox(self.settings_page, from_=1, to=100)
        predatornum_choice.pack()
        
        
        def confirm_settings():
            boolean_list_checker = [False,False,False,False]
            if int(simulation_speed_choice.get()) <= 10 and int(simulation_speed_choice.get()) >= 1:
                self._speed = float(simulation_speed_choice.get())
                boolean_list_checker[0] = True
            else:
                settings_status.configure(text = "Settings are invalid.", fg = "red")
                boolean_list_checker = [False,False,False,False]
            if int(foodnum_choice.get()) <= 100 and int(foodnum_choice.get()) >= 1:
                self._foodnum = int(foodnum_choice.get())
                boolean_list_checker[1] = True
            else:
                settings_status.configure(text = "Settings are invalid.", fg = "red")
                boolean_list_checker = [False,False,False,False]
            if int(preynum_choice.get()) <= 100 and int(preynum_choice.get()) >= 1:
                self._preynum = int(preynum_choice.get())
                boolean_list_checker[2] = True
            else:
                settings_status.configure(text = "Settings are invalid.", fg = "red")
                boolean_list_checker = [False,False,False,False]
            if int(predatornum_choice.get()) <= 100 and int(predatornum_choice.get()) >= 1:
                self._predatornum = int(predatornum_choice.get())
                boolean_list_checker[3] = True
            else:
                settings_status.configure(text = "Settings are invalid.", fg = "red")
                boolean_list_checker = [False,False,False,False]
                
            if boolean_list_checker == [True, True, True, True]:
                self._settingsconfirmed = True
                self.settings_page.destroy()
                
        settings_status = tk.Label(self.settings_page, text = "")
        settings_status.pack()
        confirm_settings_button = tk.Button(self.settings_page, text = "Confirm Settings", command = confirm_settings)
        confirm_settings_button.pack()
        
    def open_login_page(self):
        
        self.welcome_page.destroy()
        
        self.login_page = tk.Tk()
        self.login_page.title("Login Page")
        self.login_page.geometry("400x400")
        self.centre_page(self.login_page)
        self.login_page.iconbitmap("Icon.ico")
        
        login_message = tk.Label(self.login_page,text = "Please Log in")
        login_message.pack()
        username_label = tk.Label(self.login_page,text = "Username:")
        username_label.pack()
        username_entry = tk.Entry(self.login_page)
        username_entry.pack()
        password_label = tk.Label(self.login_page,text = "Password:")
        password_label.pack()
        password_entry = tk.Entry(self.login_page, show = "*")
        password_entry.pack()
        
        def verify_login():
            username = username_entry.get()
            password = password_entry.get()
            self._verified = False
            
            if username == "admin" and password == "Password1":
                login_status.configure(text = "Success! Welcome Admin.", fg = "green")
                self.login_page.update_idletasks()
                time.sleep(2)
                self.login_page.destroy()
                self.open_settings_page()
                self._verified = True
            elif True == False:
                pass
            else:
                login_status.configure(text = "Login Failed.. Try Again.", fg = "red")
                
        login_button = tk.Button(self.login_page, text = "Login", command = verify_login)
        login_button.pack()
        login_status = tk.Label(self.login_page, text = "")
        login_status.pack()
        self.login_page.mainloop()
    
    def open_otp_page(self):
        
        self.account_creation_page.destroy()
        
        self.otp_page = tk.Tk()
        self.otp_page.title("Account Creation")
        self.otp_page.geometry("400x400")
        self.centre_page(self.otp_page)
        self.otp_page.iconbitmap("Icon.ico")
        otp_message = tk.Label(self.otp_page,text = "")
        otp_message.pack()
        otp_label = tk.Label(self.otp_page,text = "OTP:")
        otp_label.pack()
        otp_entry = tk.Entry(self.otp_page)
        otp_entry.pack()
        self._validated = False
        
        def confirm_otp():
            counter = 4
            if otp_entry.get() != "" and counter > 0:
                if email_manager.get_otp() == otp_entry.get():
                    self._validated = True
                    otp_message.configure(text = "OTP is valid!", fg = "green")
                    self.otp_page.update_idletasks()
                    time.sleep(2)
                    self.otp_page.destroy()
                else:
                    otp_message.configure(text = f"OTP was invalid. Try Again. {counter} tries left", fg = "red")
                    self.otp_page.update_idletasks()
                    counter -= 1
            elif counter == 0:
                otp_message.configure(text = "Too many tries. The application will close now.", fg = "red")
                self.otp_page.update_idletasks()
                time.sleep(2)
                
        confirm_otp_button = tk.Button(self.otp_page, text = "Enter", command=lambda: confirm_otp())
        confirm_otp_button.pack() 
        


    def open_account_creation_page(self):
        
        self.welcome_page.destroy()
        
        self.account_creation_page = tk.Tk()
        self.account_creation_page.title("Account Creation")
        self.account_creation_page.geometry("400x400")
        self.centre_page(self.account_creation_page)
        self.account_creation_page.iconbitmap("Icon.ico")
        email_message = tk.Label(self.account_creation_page,text = "")
        email_message.pack()
        email_label = tk.Label(self.account_creation_page,text = "Email:")
        email_label.pack()
        email_entry = tk.Entry(self.account_creation_page)
        email_entry.pack()
        
        def confirm_email():
            counter = 4
            if email_entry.get() != "" and counter > 0:
                self._email = str(email_entry.get())
                if email_manager.my_validate_email(self.get_email()):
                    email_message.configure(text = "Email is valid!", fg = "green")
                    self.account_creation_page.update_idletasks()
                    time.sleep(2)
                    if email_manager.send_email(self.get_email()):
                        self.open_otp_page()
                    else:
                        email_message.configure(text = "An OTP code could not be generated. Please try again later. The application will close now.", fg = "red")
                        self.account_creation_page.update_idletasks()
                        time.sleep(2)
                        self.account_creation_page.destroy()
                else:
                    email_message.configure(text = f"Email was invalid. Try Again. {counter} tries left", fg = "red")
                    self.account_creation_page.update_idletasks()
                    counter -= 1
            elif counter == 0:
                email_message.configure(text = "Too many tries. The application will close now.", fg = "red")
                self.account_creation_page.update_idletasks()
                time.sleep(2)
                self.account_creation_page.destroy()
                    
        confirm_email_button = tk.Button(self.account_creation_page, text = "Confirm Email", command = confirm_email)
        confirm_email_button.pack()        
        self.account_creation_page.mainloop()
        
        
    def get_verified(self):
        return self._verified
    
    def get_settings_confirmed(self):
        return self._settingsconfirmed
    
    def get_speed(self):
        return self._speed
    
    def get_foodnum(self):
        return self._foodnum
    
    def get_preynum(self):
        return self._preynum
    
    def get_predatornum(self):
        return self._predatornum
    
    def get_email(self):
        return self._email
    