from apps.sat.models import Empleados
 
def usuarioExiste(usuario_id):
        empleados = Empleados.objects.all()
        for empleado in empleados:
            if empleado.empleado_id == usuario_id:
                return True
        return False