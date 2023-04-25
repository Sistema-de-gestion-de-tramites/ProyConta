import datetime
from apps.sat.models import Notificaciones
from apps.sat.session import usuarioExiste

class Notificacion:
    
    def  enviarNotificacion(remitente,destino,mensaje):
        if usuarioExiste(destino):
            nuevaNotifiacion = Notificaciones(mensaje=mensaje,remitente_id=remitente,destino_id=destino)
            nuevaNotifiacion.save()
        else:
            print("El usuario destino no existe")