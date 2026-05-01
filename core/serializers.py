from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# ==========================================
# 1. SERIALIZERS DE AUTENTICACIÓN (image_6caa5a.png)
# ==========================================
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # BUSCAMOS LOS RECURSOS REALES EN LA BASE DE DATOS
        # Filtramos la tabla 'RecursoHasRol' por el rol del usuario que inicia sesión
        recursos_vinculados = RecursoHasRol.objects.filter(rol__usuariohasrol__usuario=self.user)
        
        # Los convertimos a una lista de nombres
        data['recursos'] = [{'nombre': r.recurso.nombre} for r in recursos_vinculados]
        
        data['user'] = {
            'username': self.user.username,
            'nombre': self.user.first_name or self.user.username
        }
        return data
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}} # La contraseña no se muestra al consultar

    def create(self, validated_data):
        # Esta línea es la que cifra la contraseña antes de guardarla en la DB
        user = User.objects.create_user(**validated_data)
        return user
    
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['idusuarios', 'nombre', 'apellido', 'username','password'] # No incluimos password por seguridad

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class RecursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recurso
        fields = '__all__'

class UsuarioHasRolSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioHasRol
        fields = '__all__'

class RecursoHasRolSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecursoHasRol
        fields = '__all__'

# ==========================================
# 2. SERIALIZERS IOT (jeiner_playa_2.png)
# ==========================================

class ZonaMonitoreoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZonaMonitoreo
        fields = '__all__'

class DispositivoIotSerializer(serializers.ModelSerializer):
    class Meta:
        model = DispositivoIot
        fields = '__all__'

class TipoVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoVariable
        fields = '__all__'

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'

class LecturaSensorSerializer(serializers.ModelSerializer):
    # Campos de solo lectura para facilitar la visualización en el Frontend
    sensor_nombre = serializers.ReadOnlyField(source='id_sensor.nombre')
    variable_nombre = serializers.ReadOnlyField(source='id_tipo_variable.nombre')
    unidad = serializers.ReadOnlyField(source='id_tipo_variable.unidad_medida')

    class Meta:
        model = LecturaSensor
        fields = '__all__'

class EstadoAmbientalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoAmbiental
        fields = '__all__'

class UmbralAlertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UmbralAlerta
        fields = '__all__'

class AlertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerta
        fields = '__all__'

class BuzzerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buzzer
        fields = '__all__'

class EstadoBuzzerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoBuzzer
        fields = '__all__'

class ComandoRemotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComandoRemoto
        fields = '__all__'

class RespuestaComandoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespuestaComando
        fields = '__all__'

class AuditoriaSistemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditoriaSistema
        fields = '__all__'