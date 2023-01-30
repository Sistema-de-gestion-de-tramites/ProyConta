from django import forms

from apps.sat.models import Personas, Clientes, Empleados, TipoEmp

class EmpleadoForm(forms.ModelForm):
    tipo_emp_id = forms.ChoiceField(choices=[(choice.pk, choice.tipo_e) for choice in TipoEmp.objects.all()])

    class Meta:
        model = Empleados

        fields = [
            'tipo_emp_id',
            #'clie_s',
            'permisos_add'

        ]

        labels = {
            'tipo_emp': 'Tipo de empleado:',
            # 'clie_s': '',
            'permisos_add': 'Permisos adicionales'
        }