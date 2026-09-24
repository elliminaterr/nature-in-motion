import email
import smtplib
import email_validator
from email_validator import *
import requests
API_URL = "https://qrng.anu.edu.au/API/jsonI.php?length=20&type=uint16"

class EmailManager():
    
    def __init__(self):
        self.sender = 'atikshtemp@gmail.com'
        self.app_password = "ehci qwaf xsbj biwa"
        self.receiver = ""
        self.otp = ""
        self.otp_status = False
        self.status = 0
        
    def get_numbers(self):
        try:
            response = requests.get(API_URL, timeout= 6)
            self.status = response.status_code
            data = response.json()
            
            if data["success"] == True:
                return data
            else:
                print("Request unsuccessful")
        except:
            print(f"Response failed with error code: {self.status}")
            
    def generate_otp(self):
        numbers = self.get_numbers()
        otp_list = []
        if type(numbers) is dict:
            for i in list(numbers["data"]):
                i = i % (126-33)
                i = chr(i+33)
                otp_list.append(i)
            self.otp = "".join(otp_list)
            self.otp_status = True
            return self.otp
        else:
            self.otp_status = False
    
    def get_otp(self):
        return self.otp
    
    def get_otp_status(self):
        return self.otp_status
        
    def send_email(self, receiver_email):
        self.my_validate_email(receiver_email)
        self.generate_otp()
        if self.get_otp_status == False:
            return False
        else:    
            msg = email.message_from_string(f'Welcome to the simulation!\nYou will need to confirm that you are a human user by entering this code into the window:\n*** {self.otp} *** (Copy this code manually)\nPlease note that this window will close after 3 minutes ')
            msg['From'] = self.sender
            msg['To'] = self.receiver
            msg['Subject'] = "Welcome to the simulation"

            s = smtplib.SMTP("smtp.gmail.com",587)
            s.ehlo() # Hostname to send for this command defaults to the fully qualified domain name of the local host.
            s.starttls() #Puts connection to SMTP server in TLS mode
            s.ehlo()
            s.login(self.sender, self.app_password)
            s.sendmail(self.sender, receiver_email, msg.as_string())
            return True

    
    def my_validate_email(self,email):
        try:
            if validate_email(email):
                self.receiver = email
                return True
        except:
            return False
