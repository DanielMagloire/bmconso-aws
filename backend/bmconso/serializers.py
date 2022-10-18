from rest_framework import serializers
from bmconso.models import IACrigen, Rule, User, HeatingPlant, Location, Sensor, Silo, Snapshot, Planning, Boiler, Configuration

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'sub', 'role')

class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = ('admin','id', 'user_id','name', 'num', 'compl')

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('station', 'id_prev', 'id_histo', 'nom')

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ('id', 'config_id', 'num', 'name', 'unit')

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeatingPlant
        fields = ('config_id', 'silo_count', 'boiler_total', 'is_coge', 'power_coge', 'pilot_type')

class SiloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Silo
        fields = ('id', 'plant_id', 'wood_pci', 'wood_dens', 'limit_high', 'limit_low', 'cap', 'boiler_count')

class SnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snapshot
        fields = ('silo_id', 'goal', 'level', 'level_unit')

class PlanningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planning
        fields = ('silo_id', 'drop_min', 'drop_max', 'av')

class BoilerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boiler
        fields = ('id', 'silo_id', 'power_nom', 'power_min', 'output', 'load', 'order')

class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ('id', 'index', 'silo_id', 'name', 'value', 'date_begin', 'date_end', 'hour_begin', 'hour_end')

class IASerializer(serializers.ModelSerializer):
    class Meta:
        model = IACrigen
        fields = ('user_id', 'call_date', 'call_count')