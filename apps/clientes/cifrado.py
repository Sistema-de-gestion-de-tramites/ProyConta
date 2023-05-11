from cryptography.fernet import Fernet

class AES:
    
    def generaClave():
        clave = Fernet.generate_key()
        return clave

    def encript(text):
        key = str.encode("G_cmZcnxbnbftqRuKRtq9FGYu9s1JJvcFhlKGoUOjbs=")
        f = Fernet(key)
        encriptText = f.encrypt(text)
        return encriptText

    def decript(textEncript):
        key = str.encode("G_cmZcnxbnbftqRuKRtq9FGYu9s1JJvcFhlKGoUOjbs=")
        f = Fernet(key)
        text = f.decrypt(textEncript)
        return text
