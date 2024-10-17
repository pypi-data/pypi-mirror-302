import pyotp 
import qrcode 
from decouple import config


user_email = "sunnex@mail.co"
service_name = config("SERVICE_NAME")

class MFA:
    def __init__(self,service_name, user_email):
        self.secret_key = pyotp.random_base32()
        self.service_name = service_name
        self.user_email = user_email

    def generate_mfa_code(self):
        totp_auth = pyotp.totp.TOTP( 
            self.secret_key).provisioning_uri( 
            name=self.service_name, 
            issuer_name=f"{self.service_name}: {self.user_email}") 
            
            # Developer will be expected to the secret Key for the use ( it should be unique for each user)
            
            # End User should be asked to save the secret key or I will suggest you save it in a db with a
            #  key value pair where the key is the recovery code (unique) and value is the secret key. So you share the recovery code with the user

            # When they can't recover the qr or lost the mobile device, you can ask them for the recovery code then use it to get the secret 
            # key then use it to setup on the 3rd party authenticator app.
    
        return totp_auth,self.secret_key
    

    def generate_qr_code(self,totp_auth):
        return qrcode.make(totp_auth).save(f"{self.user_email}.png") 


    def verify_mfa(self,code):
        totp = pyotp.TOTP(self.secret_key) 
        return totp.verify(code)