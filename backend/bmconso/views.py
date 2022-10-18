from asyncio.windows_events import NULL
from itertools import chain
from unicodedata import name

from bmconso.serializers import *
from . models import *
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status, generics

import json
from datetime import timedelta
from datetime import date
from datetime import datetime 
from dateutil.relativedelta import *

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import numpy as np 

# USER related views
class UserListCreateView(generics.ListCreateAPIView):
    def get(self, request):
        users = User.objects.all()
        user_serializer = UserSerializer(users, many=True)
        return JsonResponse(user_serializer.data, safe=False)
    
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            user_serializer = UserSerializer(user)
            return JsonResponse(user_serializer.data)
        except User.DoesNotExist:
            return JsonResponse({ 'message': 'The user does not exist' }, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(request_body=UserSerializer)
    def put(self, request, id):
        try:
            user = User.objects.get(id=id)
            user_data  = JSONParser().parse(request)
            user_serializer = UserSerializer(user, data=user_data)
            if user_serializer.is_valid():
                user_serializer.save()
                return JsonResponse(user_serializer.data)
            return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return JsonResponse({ 'message': 'The user does not exist' }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            user = User.objects.get(id = id)
            user.delete()
            return JsonResponse({ 'message': 'user deleted' }, status=status.HTTP_202_ACCEPTED)
        except User.DoesNotExist:
            return JsonResponse({ 'message': 'The user does not exist' }, status=status.HTTP_404_NOT_FOUND)

# CONFIG related views
class ConfigListCreateView(generics.ListCreateAPIView):
    def get(self, request):
        configs = Configuration.objects.all()
        config_serializer = ConfigSerializer(configs, many=True)
        return JsonResponse(config_serializer.data, safe=False)

    config_param = openapi.Parameter('id', openapi.IN_QUERY, description="user id", type=openapi.TYPE_INTEGER)
    config_response = openapi.Response('config list', ConfigSerializer(many=True))

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))['params']
        name = data['name']
        user_id = data['user'] 
        role = data['role']
        admin = None
        user = None
        if role == 'Administrateur':
            admin = user_id
        else:
            user = User.objects.get(id=user_id)
        config = Configuration(admin=admin, name=name, user=user)
        config.save()
        config_serializer = ConfigSerializer(config)
        return JsonResponse(config_serializer.data, status=status.HTTP_201_CREATED)

class ConfigRetrieveUpdateDestroyView(generics.RetrieveUpdateAPIView):
    def get(self, request, **kwargs):
        id = kwargs.get('id')
        try:
            config = Configuration.objects.get(user_id=id)
            config_serializer = ConfigSerializer(config)
            return JsonResponse(config_serializer.data)
        except Configuration.DoesNotExist:
            return JsonResponse({ 'message': 'The config does not exist' }, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=ConfigSerializer)
    def put(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        print(user)
        config = Configuration.objects.get(id=id)
        print(config)
        if user.role != 'Administrateur' and config.user_id != user.id:
            print('--- searching ---')
            try:
                queried_config = Configuration.objects.get(user_id=user_id)
                print(queried_config)
                if queried_config.num != config.num:
                    queried_config.user_id = None
                    queried_config.save()
            except Configuration.DoesNotExist:
                print('--- found nothing ---')
            config.user = user
        config_data  = JSONParser().parse(request)
        config_serializer = ConfigSerializer(config, data=config_data)
        if config_serializer.is_valid():
            config_serializer.save()
            return JsonResponse(config_serializer.data)
        return JsonResponse(config_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        id = kwargs.get('id')

        user = User.objects.get(id=user_id)
        try:
            config = Configuration.objects.get(id=id)
            if user.role == 'Administrateur' or config.user_id == user.id:
                config.delete()
                return JsonResponse({ 'message': 'config deleted' }, status=status.HTTP_202_ACCEPTED)
            else:
                return JsonResponse({ 'message': 'Unauthorized request' }, status=status.HTTP_401_UNAUTHORIZED)
        except Configuration.DoesNotExist:
            return JsonResponse({ 'message': 'The config does not exist' }, status=status.HTTP_404_NOT_FOUND)

# LOCATION related views
class LocationListView(generics.ListAPIView):
    def get(self, request):
        locations = Location.objects.all()
        location_serializer = LocationSerializer(locations, many=True)
        return JsonResponse(location_serializer.data, safe=False)

class LocationCreateView(generics.CreateAPIView):
    location_param = openapi.Parameter('id', openapi.IN_QUERY, description="user id", type=openapi.TYPE_INTEGER)
    location_response = openapi.Response('location list', LocationSerializer(many=True))
    @swagger_auto_schema(manual_parameters=[location_param], responses={200: location_response})
    def post(self, request, **kwargs):
        id = kwargs.get('id')
        location = Location(config_id=id)
        try:
            location.save()
            location_serializer = LocationSerializer(location)
            return JsonResponse(location_serializer.data, status=status.HTTP_201_CREATED)
        except:
            return JsonResponse({'message':'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)   

class LocationRetrieveUpdateDestroyView(generics.RetrieveUpdateAPIView):
    def get(self, request, **kwargs):
        id = kwargs.get('id')
        try:
            location = Location.objects.get(config_id=id)
            location_serializer = LocationSerializer(location)
            return JsonResponse(location_serializer.data)
        except Location.DoesNotExist:
            return JsonResponse({ 'message': 'The location does not exist' }, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=LocationSerializer)
    def put(self, request, **kwargs):
        id = kwargs.get('id')
        location = Location.objects.get(config_id=id)
        location_data  = JSONParser().parse(request)
        location_serializer = LocationSerializer(location, data=location_data)
        if location_serializer.is_valid():
            location_serializer.save()
            return JsonResponse(location_serializer.data)
        return JsonResponse(location_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        id = kwargs.get('id')
        try:
            location = Location.objects.get(id=id)
            location.delete()
            return JsonResponse({ 'message': 'location deleted' }, status=status.HTTP_200_OK)
        except Location.DoesNotExist:
            return JsonResponse({ 'message': 'The location does not exist' }, status=status.HTTP_404_NOT_FOUND)

# HEATING PLANT related views
class PlantListView(generics.ListAPIView):
    def get(self, request):
        plants = HeatingPlant.objects.all()
        plant_serializer = PlantSerializer(plants, many=True)
        return JsonResponse(plant_serializer.data, safe=False)

class PlantCreateView(generics.CreateAPIView):
    plant_param = openapi.Parameter('id', openapi.IN_QUERY, description="user id", type=openapi.TYPE_INTEGER)
    plant_response = openapi.Response('plant list', PlantSerializer(many=True))
    @swagger_auto_schema(manual_parameters=[plant_param], responses={200: plant_response})
    def post(self, request, **kwargs):
        id = kwargs.get('id')
        plant = HeatingPlant(config_id=id)
        plant.save()
        plant_serializer = PlantSerializer(plant)
        return JsonResponse(plant_serializer.data, status=status.HTTP_201_CREATED)

class PlantRetrieveUpdateDestroyView(generics.RetrieveUpdateAPIView):
    def get(self, request, **kwargs):
        try:
            config_id = kwargs.get('config_id')
            plant = HeatingPlant.objects.get(config_id=config_id)
            plant_serializer = PlantSerializer(plant)
            return JsonResponse(plant_serializer.data)
        except HeatingPlant.DoesNotExist:
            return JsonResponse({ 'message': 'The plant does not exist' }, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=PlantSerializer)
    def put(self, request, **kwargs):
        config_id = kwargs.get('config_id')
        plant = HeatingPlant.objects.get(config_id=config_id)
        plant_data  = JSONParser().parse(request)
        plant_serializer = PlantSerializer(plant, data=plant_data)
        if plant_serializer.is_valid():
            plant_serializer.save()
            return JsonResponse(plant_serializer.data)
        return JsonResponse(plant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        config_id = kwargs.get('config_id')
        try:
            plant = HeatingPlant.objects.get(config_id=config_id)
            plant.delete()
            return JsonResponse({ 'message': 'plant deleted' }, status=status.HTTP_200_OK)
        except HeatingPlant.DoesNotExist:
            return JsonResponse({ 'message': 'The plant does not exist' }, status=status.HTTP_404_NOT_FOUND)

# SENSOR related views
class SensorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    def get_sensor(self, request):
        id = request.query_params.get('id')
        try:
            sensor = Sensor.objects.get(id=id)
            return sensor
        except Sensor.DoesNotExist:
            return JsonResponse({ 'message': 'The sensor does not exist' }, status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        sensor = self.get_sensor(request)
        sensor_serializer = SensorSerializer(sensor)
        return JsonResponse(sensor_serializer.data)

    def put(self, request):
        sensor = self.get_sensor(request)
        sensor_data  = JSONParser().parse(request)
        sensor_serializer = SensorSerializer(sensor, data=sensor_data)
        if sensor_serializer.is_valid():
            sensor_serializer.save()
            return JsonResponse(sensor_serializer.data)
        return JsonResponse(sensor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        id = kwargs.get('id')
        try:
            sensor = Sensor.objects.get(id=id)
            sensor.delete()
            return JsonResponse({ 'message': 'sensor deleted' }, status=status.HTTP_200_OK)
        except Sensor.DoesNotExist:
            return JsonResponse({ 'message': 'The sensor does not exist' }, status=status.HTTP_404_NOT_FOUND)
        
class SensorListCreateView(generics.ListCreateAPIView):
    def get(self, request, id):
        try:
            sensors = Sensor.objects.filter(config_id=id).order_by('id')
            sensor_serializer = SensorSerializer(sensors, many=True)
            return JsonResponse(sensor_serializer.data, safe=False)
        except Sensor.DoesNotExist:
            return JsonResponse({ 'message': 'The sensor does not exist' }, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, id):
        config = Configuration.objects.get(id=id)
        sensor_data = JSONParser().parse(request)
        sensor = Sensor(config=config, num=sensor_data['num'], name=sensor_data['name'] , unit=sensor_data['unit'])
        sensor_serializer = SensorSerializer(sensor, data=sensor_data)
        if sensor_serializer.is_valid():
            sensor.save()
            return JsonResponse(sensor_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse({ 'message': 'Something went wrong' }, status=status.HTTP_400_BAD_REQUEST)

class SensorOptionsView(generics.RetrieveAPIView):
    def get(self, request):
        num = request.query_params.get('number')
        try:
            calcul = CapteurCofelyVision(num)
            result = calcul.RecuperationListeCapteurCofelyVision_Json()
            return JsonResponse(result, safe=False)    
        except:
            return JsonResponse({ 'message': 'Invalid installation number' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# SILO related vews
class SiloListCreateView(generics.ListAPIView):
    def get(self, request, id):
        silos = Silo.objects.filter(plant_id=id).order_by('id')
        silo_serializer = SiloSerializer(silos, many=True)
        return JsonResponse(silo_serializer.data, safe=False)

    def post(self, request, id):
        silo = Silo(plant_id=id)
        silo.save()
        silo_serializer = SiloSerializer(silo)
        return JsonResponse(silo_serializer.data, status=status.HTTP_201_CREATED)

class SiloRetrieveUpdateDestroyView(generics.RetrieveUpdateAPIView):
    def get_silo(self, request):
        id = request.query_params.get('id')
        try:
            silo = Silo.objects.get(id=id)
            return silo
        except Silo.DoesNotExist:
            return JsonResponse({ 'message': 'The silo does not exist' }, status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        silo = self.get_silo(request)
        silo_serializer = SiloSerializer(silo)
        return JsonResponse(silo_serializer.data)

    def put(self, request, plant_id, id):
        silo = Silo.objects.get(id=id)
        silo_data  = JSONParser().parse(request)
        silo_serializer = SiloSerializer(silo, data=silo_data)
        if silo_serializer.is_valid():
            silo_serializer.save()
            return JsonResponse(silo_serializer.data)
        return JsonResponse(silo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, plant_id, id):
        try:
            silo = Silo.objects.get(id = id)
            silo.delete()
            return JsonResponse({ 'message': 'silo deleted' }, status=status.HTTP_200_OK)
        except Silo.DoesNotExist:
            return JsonResponse({ 'message': 'The silo does not exist' }, status=status.HTTP_404_NOT_FOUND)

# SNAPSHOT related vews
class SnapshotListView(generics.ListAPIView):
    def get(self, request, id):
        silos = Silo.objects.filter(plant_id=id).order_by('id')
        snapshots = [ ]
        for silo in silos:
            try:
                snapshot = Snapshot.objects.get(silo_id=silo.id)
                snapshot_serializer = SnapshotSerializer(instance=snapshot)
                snapshots.append(snapshot_serializer.data)
            except Snapshot.DoesNotExist:
                pass
        return JsonResponse(snapshots, safe=False)

class SnapshotCreateView(generics.ListAPIView):
    def post(self, request, id):
        silo = Silo.objects.get(id=id)
        snapshot = Snapshot(silo_id=silo.id, goal=silo.limit_high, level=silo.cap)
        snapshot.save()
        snapshot_serializer = SnapshotSerializer(snapshot)
        return JsonResponse(snapshot_serializer.data, status=status.HTTP_201_CREATED)

class SnapshotRetrieveUpdateDestroyView(generics.RetrieveUpdateAPIView):

    def get(self, request, **kwargs):
        silo_id = kwargs.get('silo_id')
        try:
            snapshot = Snapshot.objects.get(silo_id=silo_id)
            snapshot_serializer = SnapshotSerializer(snapshot)
            return JsonResponse(snapshot_serializer.data)
        except Snapshot.DoesNotExist:
            return JsonResponse({ 'message': 'The snapshot does not exist' }, status=status.HTTP_404_NOT_FOUND)


    def put(self, request, **kwargs):
        silo_id = kwargs.get('silo_id')
        try:
            snapshot = Snapshot.objects.get(silo_id=silo_id)
            snapshot_data  = JSONParser().parse(request)
            snapshot_serializer = SnapshotSerializer(snapshot, data=snapshot_data)
            if snapshot_serializer.is_valid():
                snapshot_serializer.save()
                return JsonResponse(snapshot_serializer.data)
            return JsonResponse(snapshot_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Snapshot.DoesNotExist:
            return JsonResponse({ 'message': 'The snapshot does not exist' }, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, **kwargs):
        silo_id = kwargs.get('silo_id')
        try:
            snapshot = Snapshot.objects.get(silo_id=silo_id)
            snapshot.delete()
            return JsonResponse({ 'message': 'snapshot deleted' }, status=status.HTTP_200_OK)
        except Snapshot.DoesNotExist:
            return JsonResponse({ 'message': 'The snapshot does not exist' }, status=status.HTTP_404_NOT_FOUND)
        
# PLANNING related vews
class PlanningListView(generics.ListAPIView):
    def get(self, request, plant_id):
        silos = Silo.objects.filter(plant_id=plant_id).order_by('id')
        plannings = [ ]
        for silo in silos:
            try:
                planning = Planning.objects.get(silo_id=silo.id)
                planning_serializer = PlanningSerializer(instance=planning)
                plannings.append(planning_serializer.data)
            except Planning.DoesNotExist:
                pass
        return JsonResponse(plannings, safe=False)

class PlanningCreateView(generics.CreateAPIView):
    def post(self, request, id):
        silo = Silo.objects.get(id=id)
        planning = Planning(silo=silo)
        planning.save()
        planning_serializer = PlanningSerializer(planning)
        return JsonResponse(planning_serializer.data, status=status.HTTP_201_CREATED)

class PlanningRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    def get_planning(self, request, **kwargs):
        silo_id = kwargs.get('silo_id')
        try:
            planning = Planning.objects.get(silo_id=silo_id)
            return planning
        except Planning.DoesNotExist:
            return JsonResponse({ 'message': 'The planning does not exist' }, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, **kwargs):
        planning = self.get_planning(request)
        planning_serializer = PlanningSerializer(planning)
        return JsonResponse(planning_serializer.data)

    def put(self, request, **kwargs):
        silo_id = kwargs.get('silo_id')
        try:
            planning = Planning.objects.get(silo_id=silo_id)
            planning_data  = JSONParser().parse(request)
            planning_serializer = PlanningSerializer(planning, data=planning_data)
            if planning_serializer.is_valid():
                planning_serializer.save()
                return JsonResponse(planning_serializer.data)
        except Planning.DoesNotExist:
            return JsonResponse(planning_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        silo_id = kwargs.get("silo_id")
        try:
            planning = Planning.objects.get(silo_id=silo_id)
            planning.delete()
            return JsonResponse({ 'message': 'planning deleted' }, status=status.HTTP_200_OK)
        except Planning.DoesNotExist:
            return JsonResponse({ 'message': 'The planning does not exist' }, status=status.HTTP_404_NOT_FOUND)

# BOILER related vews
class BoilerListView(generics.ListAPIView):
    def get(self, request, id):
        silos = Silo.objects.filter(plant_id=id).order_by('id')
        list = [ ]
        for silo in silos:
            try:
                boilers = Boiler.objects.filter(silo_id = silo.id).order_by('id')
                for boiler in boilers:
                    boiler_serializer = BoilerSerializer(instance=boiler)
                    list.append(boiler_serializer.data)
            except Boiler.DoesNotExist:
                pass
        return JsonResponse(list, safe=False)

class BoilerCreateView(generics.ListAPIView):
    def post(self, request, silo_id, plant_id):
        boiler_data = JSONParser().parse(request)
        silo = Silo.objects.get(id=silo_id)
        boiler = Boiler(silo=silo, order=boiler_data.get('order'))
        boiler.save()
        boiler_serializer = BoilerSerializer(boiler)
        return JsonResponse(boiler_serializer.data, status=status.HTTP_201_CREATED)

class BoilerRetrieveUpdateDestroyView(generics.RetrieveUpdateAPIView):
    def get(self, request, plant_id, silo_id, id):
        boiler = self.get_boiler(request)
        boiler_serializer = BoilerSerializer(boiler)
        return JsonResponse(boiler_serializer.data)

    def put(self, request, plant_id, silo_id, id):
        try:
            boiler = Boiler.objects.get(id=id)
            boiler_data  = JSONParser().parse(request)
            boiler_serializer = BoilerSerializer(boiler, data=boiler_data)
            if boiler_serializer.is_valid():
                boiler_serializer.save()
                return JsonResponse(boiler_serializer.data)
            return JsonResponse(boiler_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Boiler.DoesNotExist:
            return JsonResponse({ 'message': 'The boiler does not exist' }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, plant_id, silo_id, id):
        try:
            boiler = Boiler.objects.get(id = id)
            boiler.delete()
            return JsonResponse({ 'message': 'boiler deleted' }, status=status.HTTP_200_OK)
        except Boiler.DoesNotExist:
            return JsonResponse({ 'message': 'The boiler does not exist' }, status=status.HTTP_404_NOT_FOUND)

# CONSTRAINT related views
class RuleListView(generics.ListAPIView):
    def get(self, request, id):
        silos = Silo.objects.filter(plant_id=id).order_by('id')
        list = [ ]
        for silo in silos:
            try:
                rules = Rule.objects.filter(silo_id=silo.id).order_by('id')
                for rule in rules:
                    rule_serializer = RuleSerializer(instance=rule)
                    list.append(rule_serializer.data)
            except Boiler.DoesNotExist:
                pass
        return JsonResponse(list, safe=False)

class RuleCreateView(generics.CreateAPIView):
    def post(self, request, id):
        silo = Silo.objects.get(id=id)
        rule_data = JSONParser().parse(request)
        rule = Rule(silo=silo, name=rule_data['name'], value=rule_data['value'], date_begin = rule_data['date_begin'], date_end = rule_data['date_end'], hour_begin = rule_data['hour_begin'], hour_end = rule_data['hour_end'])
        rule.save()
        rule_serializer = RuleSerializer(rule)
        return JsonResponse(rule_serializer.data, status=status.HTTP_201_CREATED)

class RuleRetrieveUpdateDeleteView(generics.RetrieveUpdateAPIView):
    def get(self, request, plant_id, silo_id, id):
        try:
            rule = Rule.objects.get(id=id)
            rule_serializer = RuleSerializer(rule)
            return JsonResponse(rule_serializer.data)
        except Rule.DoesNotExist:
            return JsonResponse({'message': 'rule does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, plant_id, silo_id, id):
        try:
            rule = Rule.objects.get(id=id)
        except Rule.DoesNotExist:
            return JsonResponse({'message': 'rule does not exist'}, status=status.HTTP_404_NOT_FOUND)
        rule_data = JSONParser().parse(request)
        rule_serializer = RuleSerializer(rule, data=rule_data)
        if rule_serializer.is_valid():
            rule_serializer.save()
            return JsonResponse(rule_serializer.data)
        return JsonResponse(rule_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, plant_id, silo_id, id):
        try:
            rule = Rule.objects.get(id=id)
            rule.delete()
            return JsonResponse({'message': 'rule deleted'}, status=status.HTTP_200_OK)
        except Rule.DoesNotExist:
            return JsonResponse({'message': 'The rule does not exist'}, status=status.HTTP_404_NOT_FOUND)

class PrevisionsRetrieveView(generics.RetrieveAPIView):
    def get(self, request, **kwargs):
        nb_day = 11
        nbHours = 240

        user_id = kwargs.get('user_id')
        idConfig = kwargs.get('id')
        user = User.objects.get(id=user_id)
        config = Configuration.objects.get(id=idConfig)
        AORU = 'U'
        if user.role == 'Administrateur':
            AORU = 'A'     
        authentification = AORU + str(user_id) + 'N' + config.num
        authentification = 'test'
        location = Location.objects.get(config_id=idConfig)
        sensors = Sensor.objects.filter(config_id=idConfig).order_by('id')
        plant = HeatingPlant.objects.get(config_id=idConfig)
        silos = Silo.objects.filter(plant_id=idConfig).order_by('id')

        # safeguard for hour
        dateMaintenant = datetime.now()

        # location related values ok
        localisationVille = location.station
        
        # plant related values ok
        nbSilo = plant.silo_count
        nbChaudiereTotal = plant.boiler_total
        typePilotage = 1
        if plant.pilot_type == 'maximum de chaudières':
            typePilotage = 2
        pCoge = [plant.power_coge]
        isCoge = False
        if pCoge != 0:
            isCoge = True

        # sensors related values ok
        numInstall = [ ]
        nomCapteur = [ ]
        uniteCapteur  = [ ]

        for sensor in sensors:
            numInstall.append(sensor.num)
            nomCapteur.append(sensor.name)
            uniteCapteur.append(sensor.unit)

        # silos related values
        pciBois = [ ]
        densiteBois = [ ]
        volumeMaxSilo = [ ]
        nbChaudiere = [ ]
        niveauMaxSilo = [ ]
        niveauMinSilo = [ ]

        # planning
        volumeCamion = [ ]
        nbCamionsMax = [ ]
        nbCamionsMin = [ ]

        # all boilers related values
        siloChaudiere = [ ]
        pNomChaudiere = [ ] 
        rendementChaudiere = [ ]
        pMinChaudiere = [ ]
        prioriteChaudiere = [ ]
        chargeChaudiere = [ ]

        # default lists
        idSiloList = [ ]

        # snapshots
        niveauSilo = [ ]

        for sl in range(nbSilo):
            idSiloList.append(silos[sl].id)
            pciBois.append(silos[sl].wood_pci)
            densiteBois.append(silos[sl].wood_dens)
            volumeMaxSilo.append(silos[sl].cap)
            nbChaudiere.append(silos[sl].boiler_count)
            niveauMinSilo.append(silos[sl].limit_low)

            planning = Planning.objects.get(silo_id=silos[sl].id)
            volumeCamion.append(planning.av)
            nbCamionsMax.append(planning.drop_max)
            nbCamionsMin.append(planning.drop_min)

            snapshot = Snapshot.objects.get(silo_id=silos[sl].id)
            niveauSilo.append(snapshot.level)
            niveauMaxSilo.append(snapshot.goal)

            boilers = Boiler.objects.filter(silo=silos[sl].id).order_by('id')
            for boiler in boilers:
                chargeChaudiere.append(boiler.load)
                siloChaudiere.append(sl + 1)
                pNomChaudiere.append(boiler.power_nom)
                rendementChaudiere.append(boiler.output)
                pMinChaudiere.append(boiler.power_min)
                prioriteChaudiere.append(boiler.order)

        nmax = createArray(niveauMaxSilo, nbHours, nbSilo)

        noConfig = 0
        noSiloList = [ ]
        noColumn = 1

        chargeChaudiere = computeRule(noConfig, noSiloList, dateMaintenant, chargeChaudiere, 'Charge de la chaudière', nbHours, nbChaudiereTotal)
        rendementChaudiere = computeRule(noConfig, noSiloList, dateMaintenant, rendementChaudiere, 'Rendement de la chaudière', nbHours, nbChaudiereTotal)
        pMinChaudiere = computeRule(noConfig, noSiloList, dateMaintenant, pMinChaudiere, 'Puissance minimale de la chaudière', nbHours, nbChaudiereTotal)

        cogeArray = computeRule(noConfig, noSiloList, dateMaintenant, pCoge, 'Puissance de la cogénération', nbHours, noColumn)
        isCoge = cogeArray[0]
        pCoge = cogeArray[1]

        pciBois = computeRule(noConfig, idSiloList, dateMaintenant, pciBois, 'PCI du bois', nbHours, nbSilo)
        densiteBois = computeRule(noConfig, idSiloList, dateMaintenant, densiteBois, 'Densité du bois', nbHours, nbSilo)
        volumeMaxSilo = computeRule(noConfig, idSiloList, dateMaintenant, volumeMaxSilo, 'Volume maximal du silo', nbHours, nbSilo)
        niveauMinSilo = computeRule(noConfig, idSiloList, dateMaintenant, niveauMinSilo, 'Seuil limite basse du silo', nbHours, nbSilo)
        
        volumeCamion = computeRule(noConfig, idSiloList, dateMaintenant, volumeCamion, 'Volume moyen de biomasse par camion', nbHours, nbSilo)
        nbCamionsMax = computeRule(noConfig, idSiloList, dateMaintenant, nbCamionsMax, 'Livraisons maximales sur la demi-journée', nbHours, nbSilo)
        nbCamionsMin = computeRule(noConfig, idSiloList, dateMaintenant, nbCamionsMin, 'Livraisons minimales sur la demi-jopurnée', nbHours, nbSilo)

        actu_list = [
            niveauMaxSilo, 
            niveauMinSilo.tolist(), 
            chargeChaudiere.tolist(), 
            nbCamionsMin.tolist(), 
            nbCamionsMax.tolist(), 
            localisationVille, 
            nbSilo, 
            numInstall, 
            nomCapteur, 
            uniteCapteur, 
            pciBois.tolist(), 
            densiteBois.tolist(), 
            volumeMaxSilo.tolist(), 
            niveauSilo, 
            nbChaudiere, 
            nbChaudiereTotal, 
            siloChaudiere, 
            pNomChaudiere, 
            rendementChaudiere.tolist(), 
            pMinChaudiere.tolist(),
            isCoge.tolist(), 
            pCoge.tolist(), 
            typePilotage, 
            prioriteChaudiere,
            volumeCamion.tolist(),
            authentification
        ]

        print(isCoge)
        show = showStrToBool(request)
        if show == True:
            return JsonResponse(actu_list, safe=False, status=status.HTTP_200_OK)


        calcul = Actualiser(localisationVille, nbSilo, numInstall, nomCapteur, uniteCapteur, pciBois, densiteBois, volumeMaxSilo, niveauMaxSilo,\
                niveauMinSilo, niveauSilo, nbChaudiere, nbChaudiereTotal, siloChaudiere, pNomChaudiere, rendementChaudiere, pMinChaudiere, chargeChaudiere,\
                isCoge, pCoge, typePilotage, prioriteChaudiere, nbCamionsMin, nbCamionsMax, volumeCamion, authentification, dateMaintenant)

        return calcul

def createArray(list, sizeLine, sizeColumn):
    npArray = np.zeros([sizeLine, sizeColumn])
    with np.nditer(npArray, flags=['multi_index'], op_flags=['readwrite'], order='C') as it:
        for x in it:
            x[...] = list[it.multi_index[1]]
    return npArray

def computeRule(idPlant, idList, hour, dfList, ruleName, sizeLine, sizeColumn):

    nbDays = 11
    nbHours = 240

    npArray = createArray(dfList, sizeLine, sizeColumn)

    for iCol in range(sizeColumn):
        if idPlant != 0:
            rules = Rule.objects.filter(plant_id=idPlant, name__contains=ruleName).order_by('id')
        elif len(idList) > 0:
            rules = Rule.objects.filter(silo=idList[iCol], name__contains=ruleName).order_by('id')
        else:
            rules = Rule.objects.filter(name__contains=ruleName + ' ' + str(iCol+1))

        for rule in rules:
            full_begin = date.today()
            full_end = date.today() + timedelta(days=nbDays)

            date_begin = rule.date_begin
            date_end = rule.date_end

            hour_begin = rule.hour_begin
            hour_end = rule.hour_end

            iLine = 0
            hour_now = hour

            if  full_begin <= date_end and date_begin <= full_end:
                while full_begin < date_begin:
                    iLine += 24 - hour_now
                    hour_now = 0
                    full_begin += timedelta(days=nbDays)

                if hour_now < hour_begin:
                    iLine += hour_begin - hour_now
                    hour_now = hour_begin 

                while date_begin < date_end and date_begin < full_end:
                    while hour_now < 24:
                        if iLine == nbHours:
                            break
                        npArray[iLine][iCol] = rule.value
                        iLine += 1
                        hour_now += 1

                    hour_now = 0
                    date_begin += timedelta(days=1)

                while hour_now < hour_end:
                    if iLine == nbHours:
                        break
                    npArray[iLine][iCol] = rule.value
                    iLine += 1
                    hour_now += 1

    if idPlant != 0:
        isArray = np.full((sizeLine, sizeColumn), False, dtype=bool)
        for iCoge in range(npArray.size):
            if npArray[iCoge, 0] > 0:
                isArray[iCoge, 0] = True
        return np.array([isArray, npArray])
    return npArray

def updateCallCount(request, id):
    user = User.objects.get(id = id)
    if(user.call_date != date.today()):
        user.call_date = date.today()
        user.call_count = 1
    else:
        user.call_count += 1
    try:
        user.save()
    except:
        return JsonResponse({'message':'user save failed'}, status=status.HTTP_400_BAD_REQUEST)

def refreshStrToBool(request):
    refresh = request.query_params.get('refresh')
    if refresh is None:
        return False
    elif isinstance(refresh, str):
        return True

def showStrToBool(request):
    show = request.query_params.get('show')
    if show is None:
        return False
    elif isinstance(show, str):
        return True

class StockBiomasseRetrieveView(generics.RetrieveAPIView):
    def get(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        config_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        config = Configuration.objects.get(id=config_id)
        AORU = 'U'
        if user.role == 'Administrateur':
            AORU = 'A'     
        authentification = AORU + str(user_id) + 'N' + config.num
        authentification = 'test'
        refresh = refreshStrToBool(request)
        if refresh == False:
            try:
                with open(str(authentification)+'_livraison.pickle', 'rb') as openfile:
                    meteo_pickle = pickle.load(openfile)
                    # print(meteo_pickle)
                    meteo_dict = meteo_pickle.to_json(orient='index')
                    meteo_json = json.loads(meteo_dict)
                    return JsonResponse(meteo_json, safe=False)
            except IOError:
                print('livraison file not found')
                refresh = True
        if refresh == True:
            calcul = PrevisionsRetrieveView().get(request, **kwargs)
            result = calcul.CalculPlanningAppro()
            try:
                with open(str(authentification)+'_livraison.pickle', 'rb') as openfile:
                    meteo_pickle = pickle.load(openfile)
                    # print(meteo_pickle)
                    meteo_dict = meteo_pickle.to_json(orient='index')
                    meteo_json = json.loads(meteo_dict)
                    return JsonResponse(meteo_json, safe=False)
            except IOError:
                print('livraison file not found')
        return JsonResponse({'message':'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

class BesoinBiomasseRetrieveView(generics.RetrieveAPIView):
    def get(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        config_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        config = Configuration.objects.get(id=config_id)
        AORU = 'U'
        if user.role == 'Administrateur':
            AORU = 'A'     
        authentification = AORU + str(user_id) + 'N' + config.num
        authentification = 'test'
        try:
            with open(str(authentification)+'_stockAveclivraison.pickle', 'rb') as openfile:
                meteo_pickle = pickle.load(openfile)
                # print(meteo_pickle)
                meteo_dict = meteo_pickle.to_json(orient='index')
                meteo_json = json.loads(meteo_dict)
                return JsonResponse(meteo_json, safe=False)
        except IOError:
            return JsonResponse({'message':'biomasse file not found'}, status=status.HTTP_404_NOT_FOUND)

class PrevisionDemandeRetrieveView(generics.RetrieveAPIView):
    def get(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        config_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        config = Configuration.objects.get(id=config_id)
        AORU = 'U'
        if user.role == 'Administrateur':
            AORU = 'A'     
        authentification = AORU + str(user_id) + 'N' + config.num
        authentification = 'test'
        try:
            with open(str(authentification)+'_demande.pickle', 'rb') as openfile:
                meteo_pickle = pickle.load(openfile)
                # print(meteo_pickle)
                meteo_dict = meteo_pickle.to_json(orient='index')
                meteo_json = json.loads(meteo_dict)
                return JsonResponse(meteo_json, safe=False)
        except IOError:
            return JsonResponse({'message':'prevision file not found'}, status=status.HTTP_404_NOT_FOUND)

class PrevisionMeteoRetrieveView(generics.RetrieveAPIView):
    def get(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        config_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        config = Configuration.objects.get(id=config_id)
        AORU = 'U'
        if user.role == 'Administrateur':
            AORU = 'A'     
        authentification = AORU + str(user_id) + 'N' + config.num
        authentification = 'test'
        try:
            with open(str(authentification)+'_meteo.pickle', 'rb') as openfile:
                meteo_pickle = pickle.load(openfile)
                # print(meteo_pickle)
                meteo_dict = meteo_pickle.to_json(orient='index')
                meteo_json = json.loads(meteo_dict)
                return JsonResponse(meteo_json, safe=False)
        except IOError:
            return JsonResponse({'message':'meteo file not found'}, status=status.HTTP_404_NOT_FOUND)

class HistoricsRetrieveView(generics.RetrieveAPIView):
    def get(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        config_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        config = Configuration.objects.get(id=config_id)
        AORU = 'U'
        if user.role == 'Administrateur':
            AORU = 'A'     
        authentification = AORU + str(user_id) + 'N' + config.num
        authentification = 'test'
        try:
            with open(str(authentification)+'.pickle', 'rb') as openfile:
                histo_pickle = pickle.load(openfile)
                # print(histo_pickle)
                histo_dict = histo_pickle.to_json(orient='index')
                histo_json = json.loads(histo_dict)
                return JsonResponse(histo_json, safe=False)
        except IOError:
            return JsonResponse({'message':'meteo file not found'}, status=status.HTTP_404_NOT_FOUND)