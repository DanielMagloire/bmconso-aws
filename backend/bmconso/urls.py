from django.urls import re_path

from .views import *

urlpatterns = [
    re_path(r'^users$', UserListCreateView.as_view(), name='list-create-user'),
    re_path(r'^users/(?P<id>[0-9]+)$', UserRetrieveUpdateDestroyView.as_view(), name='retrive-update-destroy-user'),

    # CONFIGURATION related urls
    re_path(r'^configurations$', ConfigListCreateView.as_view(), name='list-create-plant'),
    re_path(r'^users/(?P<user_id>[0-9]+)/configurations/(?P<id>[0-9]+)$', ConfigRetrieveUpdateDestroyView.as_view(), name='retrieve-update-destroy-plant'),
    # LOCATION related urls
    re_path(r'^locations$', LocationListView.as_view(), name='list-create-location'),
    re_path(r'^configurations/(?P<id>[0-9]+)/locations$', LocationCreateView.as_view(), name='list-create-location'),
    re_path(r'^configurations/(?P<config_id>[0-9]+)/locations/(?P<id>[0-9]+)$', LocationRetrieveUpdateDestroyView.as_view(), name='retrieve-update-destroy-location'),

    re_path(r'^heatingplants$', PlantListView.as_view(), name='list-create-plant'),
    re_path(r'^configurations/(?P<id>[0-9]+)/heatingplants$', PlantCreateView.as_view(), name='list-create-plant'),
    re_path(r'^configurations/(?P<config_id>[0-9]+)/heatingplants/(?P<id>[0-9]+)$', PlantRetrieveUpdateDestroyView.as_view(), name='retrieve-update-destroy-plant'),

    #  SENSOR related urls
    re_path(r'^configurations/(?P<id>[0-9]+)/sensors$', SensorListCreateView.as_view(), name='list-create-sensors'),
    re_path(r'^configurations/(?P<config_id>[0-9]+)/sensors/(?P<id>[0-9]+)', SensorRetrieveUpdateDestroyView.as_view(), name='add-sensor'),
    re_path(r'^sensors/cofely_vision$', SensorOptionsView.as_view(), name='cofelyvision-data'),

    # SILO related urls 
    re_path(r'^heatingplants/(?P<id>[0-9]+)/silos$', SiloListCreateView.as_view(), name='list-silos'),
    re_path(r'^heatingplants/(?P<plant_id>[0-9]+)/silos/(?P<id>[0-9]+)$', SiloRetrieveUpdateDestroyView.as_view(), name='add-silo'),

    # BOILER related urls 
    re_path(r'^heatingplants/(?P<id>[0-9]+)/boilers$', BoilerListView.as_view(), name='list-boilers'),
    re_path(r'^heatingplants/(?P<plant_id>[0-9]+)/silos/(?P<silo_id>[0-9]+)/boilers$', BoilerCreateView.as_view(), name='list-boilers'),
    re_path(r'^heatingplants/(?P<plant_id>[0-9]+)/silos/(?P<silo_id>[0-9]+)/boilers/(?P<id>[0-9]+)$', BoilerRetrieveUpdateDestroyView.as_view(), name='add-boiler'),

    # PLANNING related urls
    re_path(r'^heatingplants/(?P<plant_id>[0-9]+)/silos/(?P<silo_id>[0-9]+)/plannings/(?P<id>[0-9]+)$', PlanningRetrieveUpdateDestroyView.as_view(), name='list-plannings'),
    re_path(r'^heatingplants/(?P<plant_id>[0-9]+)/plannings$', PlanningListView.as_view(), name='add-planning'),
    re_path(r'^silos/(?P<id>[0-9]+)/plannings$', PlanningCreateView.as_view(), name='add-planning'),

    # SNAPSHOT related urls
    re_path(r'^heatingplants/(?P<id>[0-9]+)/snapshots$', SnapshotListView.as_view(), name='list-snapshots'),
    re_path(r'^silos/(?P<id>[0-9]+)/snapshots$', SnapshotCreateView.as_view(), name='list-snapshots'),    
    re_path(r'^heatingplants/(?P<plant_id>[0-9]+)/silos/(?P<silo_id>[0-9]+)/snapshots/(?P<id>[0-9]+)$', SnapshotRetrieveUpdateDestroyView.as_view(), name='add-snapshot'),

    # CONSTRAINT related urls
    re_path(r'^heatingplants/(?P<id>[0-9]+)/rules$', RuleListView.as_view(), name='list-constrtaints'),
    re_path(r'^silos/(?P<id>[0-9]+)/rules$', RuleCreateView.as_view(), name='add-rule'),
    re_path(r'^heatingplants/(?P<plant_id>[0-9]+)/silos/(?P<silo_id>[0-9]+)/rules/(?P<id>[0-9]+)$', RuleRetrieveUpdateDeleteView.as_view(), name='retrieve-update-delete-rule'),

    re_path(r'^users/(?P<user_id>[0-9]+)/biomass_stock/(?P<id>[0-9]+)$', StockBiomasseRetrieveView.as_view(), name='get-appro'),
    re_path(r'^users/(?P<user_id>[0-9]+)/biomass_need/(?P<id>[0-9]+)$', BesoinBiomasseRetrieveView.as_view(), name='get-stock'),
    re_path(r'^users/(?P<user_id>[0-9]+)/demand_prevision/(?P<id>[0-9]+)$', PrevisionDemandeRetrieveView.as_view(), name='get-demand'),
    re_path(r'^users/(?P<user_id>[0-9]+)/weather_prevision/(?P<id>[0-9]+)$', PrevisionMeteoRetrieveView.as_view(), name='get-meteo'),
    re_path(r'^users/(?P<user_id>[0-9]+)/historics/(?P<id>[0-9]+)$', HistoricsRetrieveView.as_view(), name='get-historics'),

    re_path(r'^users/(?P<user_id>[0-9]+)/previsions/(?P<id>[0-9]+)$', PrevisionsRetrieveView.as_view(), name='get-previsions'),

]
