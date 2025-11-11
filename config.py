import os

class Settings:
    def __init__(self):
        self.DB_SOCKET = os.getenv("DB_SOCKET")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASS = os.getenv("DB_PASS")
        self.DB_NAME = os.getenv("DB_NAME")
        self.TWILIO_SID = os.getenv("TWILIO_SID")
        self.TWILIO_AUTH = os.getenv("TWILIO_AUTH")
        self.TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")

    def dbconfig(self):
        return {
            "user": self.DB_USER,
            "password": self.DB_PASS,
            "database": self.DB_NAME,
            "unix_socket": self.DB_SOCKET
        }

settings = Settings()