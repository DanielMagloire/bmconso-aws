from multiprocessing.sharedctypes import Value
from operator import index
# from tkinter import FALSE
#from tkinter import TRUE
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator

import math
import pandas as pd
import numpy as np

from datetime import datetime
from datetime import timedelta
from datetime import date

import requests
import urllib
from bs4 import BeautifulSoup
import unicodedata
import requests

import time
import pickle

from IPython.display import display

import string
import random

def random_numstring():
    configs = Configuration.objects.all()

    while True:
        numstring = ''.join(random.choices(string.digits, k = 10))
        if not any(config.num == numstring for config in configs):
            break
    return numstring

class User(models.Model):
    name = models.CharField(max_length=99, default='')
    sub = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=14, default='Utilisateur')

class Configuration(models.Model):
    user = models.OneToOneField(User, unique=True, null=True, on_delete=models.SET_NULL)
    admin = models.PositiveBigIntegerField(null=True)
    num = models.CharField(max_length=10, unique=True, default=random_numstring)
    compl = models.PositiveIntegerField(default=0)
    name = models.CharField(default='', max_length=99)
    # 0: no completion
    # 1: meteo page done
    # 2: network page done
    # 3: defauflt configuration done 

class Location(models.Model):
    config = models.OneToOneField(Configuration, primary_key=True, on_delete=models.CASCADE)
    station = models.CharField(max_length=34, default='Abbeville (80)')
    id_histo = models.PositiveIntegerField(default=7005)
    id_prev = models.PositiveIntegerField(default=29592)
    nom = models.CharField(max_length=26, default='abbeville')

# heating plant
class HeatingPlant(models.Model):
    config = models.OneToOneField(Configuration, primary_key=True, on_delete=models.CASCADE)
    # auto incremented
    silo_count = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(3)])
    boiler_total = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(9)])
    # operating data
    is_coge = models.BooleanField(default=False)
    power_coge = models.FloatField(default=0)
    pilot_type = models.CharField(max_length=22, default='Maximum de chaudi??res')

class Sensor(models.Model):
    config = models.ForeignKey(Configuration, on_delete=models.CASCADE)
    num = models.PositiveBigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=50, default='')
    unit = models.CharField(max_length=3, default='W')

class Silo(models.Model):
    plant = models.ForeignKey(HeatingPlant, to_field='config', on_delete=models.CASCADE)
    wood_pci = models.FloatField(default=0)
    wood_dens = models.FloatField(default=0)
    limit_high = models.FloatField(default=100)
    limit_low = models.FloatField(default=0)
    boiler_count = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(3)])
    #conditional
    cap = models.FloatField(default=0)

class Snapshot(models.Model):
    silo = models.OneToOneField(Silo, primary_key=True, on_delete=models.CASCADE)
    goal = models.FloatField(default=0)
    level = models.FloatField(default=0)
    level_unit = models.CharField(max_length=2, default='m??')

class Planning(models.Model):
    silo = models.OneToOneField(Silo, primary_key=True, on_delete=models.CASCADE)
    drop_min = models.PositiveIntegerField(default=0)
    drop_max = models.PositiveIntegerField(default=0)
    av = models.FloatField(default=0)

class Boiler(models.Model):
    silo = models.ForeignKey(Silo, on_delete=models.CASCADE)
    output = models.FloatField(default=0)
    power_nom = models.FloatField(default=0)
    power_min = models.FloatField(default=0)
    load = models.FloatField(default=0)
    order = models.PositiveIntegerField()

class Rule(models.Model):
    silo = models.ForeignKey(Silo,  on_delete=models.CASCADE)
    # boiler_id = models.IntegerField(default=0)
    date_begin = models.DateField(default=date.today)
    date_end = models.DateField(default=date.today)
    hour_begin = models.PositiveIntegerField(default=datetime.today().hour)
    hour_end = models.PositiveIntegerField(default=datetime.today().hour)
    index = models.PositiveIntegerField(default=0)
    name = models.CharField(default='', max_length=50)
    value = models.PositiveIntegerField(default=0)

class IACrigen(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    call_date = models.DateField(default=date.today)
    call_count = models.IntegerField(default=0)

class CapteurCofelyVision(object):
    def __init__(self, numInstall):
        self.numInstall = numInstall
        pass

    def RecuperationListeCapteurCofelyVision_Json(self):
    
            # --------- Donn??es d???entr??es ---------
        # Num??ro de l'installation
        NUM_INSTALL = self.numInstall
        # Param??tres communs ?? toutes les requ??tes HTTP
        headers = {'Content-Type': 'text/json','x-subject-username': 'VZ5325','x-api-key': 'l7xx2c0a9eb112524bec9fa8ef3976750860','x-api-secret': 'c91fb9dd1f84487088fc34c51bd4bd27'}
        
        # --------- Param??tres interm??diaires ---------
        data=[]
        i=0
        
        # --------- CALCUL ---------
        
        # ===== R??cup??ration du num??ro du capteur =====
        # /// R??cup??ration de l'identifiant de l'installation ///
        # Ecriture de la requ??te HTTP
        strURL = 'http://es2.gses.gdfsuez.net:8080/m2m/api/v3/properties?$filter=code%20eq%20%27' + str(NUM_INSTALL) + '%27'
        # Envoi de la requ??te HTTP
        response = requests.get(strURL, headers=headers)
        # Exploitation de la r??ponse ?? la requ??te pour r??cup??rer le code de l'installation
        if response.status_code == 200:
            response_json = response.json()
            for valeur in response_json.values():
                id_install = valeur[0]['property_id']
                
        # /// R??cup??ration de la liste des capteurs disponibles (85 premiers) ///
        # Ecriture de la requ??te HTTP
        strURL = 'http://es2.gses.gdfsuez.net:8080/m2m/api/v3/properties/' + str(id_install) + '/controllers/0/measures_points'
        # Envoi de la requ??te HTTP
        response = requests.get(strURL, headers=headers)
        # Exploitation de la r??ponse ?? la requ??te pour r??cup??rer le num??ro du capteur
        if response.status_code == 200:
            response_json = response.json()
            for valeur in response_json.values():
                for capteur in valeur:
                    data.append(capteur['name'])
                    i+=1
                        
        # /// R??cup??ration de la liste des capteurs disponibles (85 suivants) ///
        # Ecriture de la requ??te HTTP
        strURL = 'http://es2.gses.gdfsuez.net:8080/m2m/api/v3/properties/' + str(id_install) + '/controllers/0/measures_points?%24skip=85'
        # Envoi de la requ??te HTTP
        response = requests.get(strURL, headers=headers)
        # Exploitation de la r??ponse ?? la requ??te pour r??cup??rer le num??ro du capteur
        if response.status_code == 200:
            response_json = response.json()
            for valeur in response_json.values():
                for capteur in valeur:
                    data.append(capteur['name'])
                    i+=1
        return data    

    def RecuperationListeCapteurCofelyVision(self):

        # --------- Donn??es d???entr??es ---------
        # Num??ro de l'installation
        NUM_INSTALL = self.numInstall
        
        # --------- Param??tres communs ?? toutes les requ??tes HTTP ---------
        headers = {'Content-Type': 'text/json', 'x-subject-username': 'VZ5325', 'x-api-key': 'l7xx2c0a9eb112524bec9fa8ef3976750860', 'x-api-secret': 'c91fb9dd1f84487088fc34c51bd4bd27'}
        
        # --------- Param??tres interm??diaires ---------
        data = []
        
        # --------- CALCUL ---------

        # /// R??cup??ration de l'identifiant de l'installation ///
        # Ecriture de la requ??te HTTP
        strURL = 'http://es2.gses.gdfsuez.net:8080/m2m/api/v3/properties?$filter=code%20eq%20%27' + str(NUM_INSTALL) + '%27'
        # Envoi de la requ??te HTTP
        response = requests.get(strURL, headers=headers)
        # Exploitation de la r??ponse ?? la requ??te pour r??cup??rer le code de l'installation
        if response.status_code == 200:
            response_json = response.json()
            for valeur in response_json.values():
                id_install = valeur[0]['property_id']
        else:
            id_install = np.nan

        # /// R??cup??ration de la liste des capteurs disponibles (85 premiers) ///
        # Ecriture de la requ??te HTTP
        strURL = 'http://es2.gses.gdfsuez.net:8080/m2m/api/v3/properties/' + str(id_install) + '/controllers/0/measures_points'
        # Envoi de la requ??te HTTP
        response = requests.get(strURL, headers=headers)
        # Exploitation de la r??ponse ?? la requ??te pour r??cup??rer le num??ro du capteur
        if response.status_code == 200:
            response_json = response.json()
            for valeur in response_json.values():
                for capteur in valeur:
                    data.append(capteur['name'])

        # /// R??cup??ration de la liste des capteurs disponibles (85 suivants) ///
        # Ecriture de la requ??te HTTP
        strURL = 'http://es2.gses.gdfsuez.net:8080/m2m/api/v3/properties/' + str(id_install) + '/controllers/0/measures_points?%24skip=160'
        # Envoi de la requ??te HTTP
        response = requests.get(strURL, headers=headers)
        # Exploitation de la r??ponse ?? la requ??te pour r??cup??rer le num??ro du capteur
        if response.status_code == 200:
            response_json = response.json()
            for valeur in response_json.values():
                for capteur in valeur:
                    data.append(capteur['name'])

        # --------- Donn??es de sorties ---------
        # Remplissage du tableau de sortie
        columns_tableauSortie = ['NOM_CAPTEUR']
        df_tableauSortie = pd.DataFrame(columns=columns_tableauSortie, data=data)
        listeCapteurs = df_tableauSortie
        return listeCapteurs

class Actualiser(object):
    
    global debug
    debug = True # Variable pour travailler en mode debug

    def __init__(self, localisationVille, nbSilo, numInstall, nomCapteur, uniteCapteur, \
                 pciBois, densiteBois, volumeMaxSilo, niveauMaxSilo,\
                 niveauMinSilo, niveauSilo, nbChaudiere, nbChaudiereTotal, \
                 siloChaudiere, pNomChaudiere, rendementChaudiere, pMinChaudiere, chargeChaudiere,\
                 isCoge, pCoge, typePilotage, prioriteChaudiere, nbCamionsMin, nbCamionsMax, \
                 volumeCamion, authentification, dateMaintenant):

        self.localisationVille = localisationVille # Localisation g??ographique du site
        self.nbSilo = nbSilo # Nombre de chaufferie = nombre de silo
        self.numInstall = numInstall # Num??ro d'installation
        self.nomCapteur = nomCapteur # Nom du capteur
        self.uniteCapteur = uniteCapteur # Unit?? du capteur
        self.pciBois = pciBois # PCI du bois
        self.densiteBois = densiteBois # Densit?? du bois
        self.volumeMaxSilo = volumeMaxSilo # Volume maximal du silo (en m3)
        self.niveauMaxSilo = niveauMaxSilo # Seuil limite haute du silo (en %, valeur entre 0 et 100)
        self.niveauMinSilo = niveauMinSilo # Seuil limite basse du silo (en %, valeur entre 0 et 100)
        self.niveauSilo = niveauSilo # Niveau actuel du silo (en %, valeur entre 0 et 100)
        self.nbChaudiere = nbChaudiere # Nombre de chaudi??res associ??es au silo
        self.nbChaudiereTotal = nbChaudiereTotal # Nombre de chaudi??re total
        self.siloChaudiere = siloChaudiere # Silo li?? ?? la chaudi??re
        self.pNomChaudiere = pNomChaudiere # Puissance nominale de la chaudi??re
        self.rendementChaudiere = rendementChaudiere # Rendement de la chaudi??re
        self.pMinChaudiere = pMinChaudiere # Puissance minimale de la chaudi??re
        self.chargeChaudiere = chargeChaudiere # Charge de la chaudi??re
        self.isCoge = isCoge # Pr??sence d'une cog??n??ration
        self.pCoge = pCoge # Puissance de la cog??n??ration
        self.typePilotage = typePilotage # Type de pilotage
        self.prioriteChaudiere = prioriteChaudiere # Priorit?? des chaudi??res
        self.nbCamionsMin = nbCamionsMin # Nombre de livraisons possibles sur une demi-journ??e, minimal
        self.nbCamionsMax = nbCamionsMax # Nombre de livraisons possibles sur une demi-journ??e, maximal
        self.volumeCamion = volumeCamion # Volume moyen de biomasse livr??e par camion (en m3)
        self.authentification = authentification
        self.dateMaintenant = dateMaintenant
        pass

    def to_minutes(self, time):
        """Fonction qui permet de r??cup??rer une date en minutes sur l'ann??e

        Args:
            self : Ensemble des param??tres de la configuration
            time (datetime): La date ?? convertir

        Returns:
            double : La valeur en minutes

        """
        return (time.days*24*3600 + time.seconds)/60

    def DonneesCofelyVision(self):
        """Fonction qui permet de r??cup??rer et traiter l'historique de la demande du r??seau sur une plage de temps donn??e via Cofely Vision
        
        Pour chaque compteur consid??r??, on r??cup??re les donn??es Cofely Vision et on les pr??traite.
        On reconstitue ensuite une demande globale du r??seau en agr??geant l'ensemble des compteurs.
    
        Args:
            self : Ensemble des param??tres de la configuration notamment le num??ro de l'installation Cofely Vision, le nom des compteurs et les unit??s des compteurs
    
        Returns:
            L'historique de la demande du r??seau pour l'ensemble des compteurs Cofely Vision au pas de temps horaire
    
        #TODO s'assurer que l'on peut bien utiliser l'API CofelyVision comme on le fait
        
        """
       
        if debug : print('---------- D??but r??cup??ration des donn??es Cofely Vision ----------')
        
        # --------- Donn??es d???entr??es --------
        # Tableau de capteurs
        columns_tableauCapteur = ['NUM_INSTALL', 'NOM_CAPTEUR', 'UNITE_CAPTEUR', 'NUM_CAPTEUR', 'F_CORR']
        # Cr??ation du tableau vide
        df_tableauCapteur = pd.DataFrame(columns=columns_tableauCapteur)
        # Ajout des donn??es
        for i in range(len(self.nomCapteur)):
            data_tableauCapteur = np.array([self.numInstall[i], self.nomCapteur[i], self.uniteCapteur[i], '', ''])
            df_tableauCapteur.loc[len(df_tableauCapteur)] = data_tableauCapteur
        # Dates
        DERNIERE_DATE = self.dateDernieresDonnees # on r??cup??re la date des derni??res donn??es t??l??charg??es
        DATE_MAINTENANT = self.dateMaintenant # on r??cup??re la date actuelle (au moment du lancement de l'API IA)
        
        # --------- Param??tres communs ?? toutes les requ??tes HTTP ---------
        headers = {'Content-Type': 'text/json', 'x-subject-username': 'VZ5325', 'x-api-key': 'l7xx2c0a9eb112524bec9fa8ef3976750860', 'x-api-secret': 'c91fb9dd1f84487088fc34c51bd4bd27'}

        # --------- D??finition de la plage d?????tude ---------
        # D??but de la plage d'??tude 
        if DERNIERE_DATE != None:
            if (DERNIERE_DATE-DATE_MAINTENANT).days <= 365:
                DATE_DEBUT = DERNIERE_DATE + timedelta(hours=1)
                DATE_DEBUT = DATE_DEBUT.replace(minute=0, second=0, microsecond=0)
            else:
                DATE_DEBUT = DATE_MAINTENANT - timedelta(hours=8760)
                DATE_DEBUT = DATE_DEBUT.replace(minute=0, second=0, microsecond=0)
        else:
            DATE_DEBUT = DATE_MAINTENANT - timedelta(hours=8760)
            DATE_DEBUT = DATE_DEBUT.replace(minute=0, second=0, microsecond=0)
        # Fin de la plage d'??tude
        DATE_FIN = DATE_MAINTENANT
        DATE_FIN = DATE_FIN.replace(minute=0, second=0, microsecond=0)
        # El??ments de comptage
        NB_MINUTES = math.floor((DATE_FIN-DATE_DEBUT).total_seconds() / 60)
        NB_HEURES = math.floor(NB_MINUTES / 60)
        NB_JOURS = math.floor(NB_HEURES / 24)
        
        # --------- Donn??es de sorties ---------
        # Initialisation du tableau de sortie
        columns_tableauSortie = ['DATE', 'DEMANDE_RESEAU']
        index_tableauSortie = range(NB_HEURES)
        df_tableauSortie = pd.DataFrame(index=index_tableauSortie, columns=columns_tableauSortie)
        # Remplissage de la colonne DATE
        for heures in range(NB_HEURES):
            df_tableauSortie['DATE'][heures] = DATE_DEBUT + timedelta(hours=heures)
            df_tableauSortie['DEMANDE_RESEAU'][heures] = 0
            
        # --------- CALCUL ---------

        # A ??? D??finition et initialisation des param??tres interm??diaires
        if debug : print('--- D??finition et initialisation des param??tres interm??diaires ---')
        # 1 - Compl??ment du tableau de capteurs
        for i in range(len(df_tableauCapteur.index)):
            # /// R??cup??ration du num??ro du capteur ///
            # == R??cup??ration de l'identifiant de l'installation ==
            # Ecriture de la requ??te HTTP
            strURL = 'http://es2.gses.gdfsuez.net:8080/m2m/api/v3/properties?$filter=code%20eq%20%27' + df_tableauCapteur['NUM_INSTALL'][i] + '%27'
            # Envoi de la requ??te HTTP
            response = requests.get(strURL, headers=headers)
            # Exploitation de la r??ponse ?? la requ??te pour r??cup??rer le code de l'installation
            if response.status_code == 200:
                response_json = response.json()
                for valeur in response_json.values():
                    id_install = valeur[0]['property_id']
            else:
                id_install = np.nan
            # == R??cup??ration de la liste des capteurs disponibles (85 premiers) ==
            # Ecriture de la requ??te HTTP
            strURL = 'http://es2.gses.gdfsuez.net:8080/m2m/api/v3/properties/' + str(id_install) + '/controllers/0/measures_points'
            # Envoi de la requ??te HTTP
            response = requests.get(strURL, headers=headers)
            # Exploitation de la r??ponse ?? la requ??te pour r??cup??rer le num??ro du capteur
            if response.status_code == 200:
                response_json = response.json()
                for valeur in response_json.values():
                    for capteur in valeur:
                        if capteur['name'] == df_tableauCapteur['NOM_CAPTEUR'][i]:
                            df_tableauCapteur['NUM_CAPTEUR'][i] = capteur['point_id']
            else:
                df_tableauCapteur['NUM_CAPTEUR'][i] = np.nan
            # == R??cup??ration de la liste des capteurs disponibles (85 suivants) ==
            # Ecriture de la requ??te HTTP
            strURL = 'http://es2.gses.gdfsuez.net:8080/m2m/api/v3/properties/' + str(id_install) + '/controllers/0/measures_points?%24skip=85'
            # Envoi de la requ??te HTTP
            response = requests.get(strURL, headers=headers)
            # Exploitation de la r??ponse ?? la requ??te pour r??cup??rer le num??ro du capteur
            if response.status_code == 200:
                response_json = response.json()
                for valeur in response_json.values():
                    for capteur in valeur:
                        if capteur['name'] == df_tableauCapteur['NOM_CAPTEUR'][i]:
                            df_tableauCapteur['NUM_CAPTEUR'][i] = capteur['point_id']
            else:
                df_tableauCapteur['NUM_CAPTEUR'][i] = np.nan
                
            # /// R??cup??ration du facteur correctif ///
            if df_tableauCapteur['UNITE_CAPTEUR'][i] == 'W' or df_tableauCapteur['UNITE_CAPTEUR'][i] == 'Wh':
                df_tableauCapteur['F_CORR'][i] = 0.001
            elif df_tableauCapteur['UNITE_CAPTEUR'][i] == 'kW' or df_tableauCapteur['UNITE_CAPTEUR'][i] == 'kWh':
                df_tableauCapteur['F_CORR'][i] = 1
            elif df_tableauCapteur['UNITE_CAPTEUR'][i] == 'MW' or df_tableauCapteur['UNITE_CAPTEUR'][i] == 'MWh':
                df_tableauCapteur['F_CORR'][i] = 1000
            else:
                df_tableauCapteur['F_CORR'][i] = 1000000
                
        if debug : 
            print('Valeur : df_tableauCapteur')
            print(df_tableauCapteur)

        # B ??? Traitement pour chaque capteur
        for i in range(len(df_tableauCapteur.index)):
           
           if debug : print('--- Traitement pour le capteur ' + str(i+1) + '/' + str(len(df_tableauCapteur.index)) + ' ---')

           # /// R??cup??ration des donn??es du capteur ///
           if debug : print('- R??cup??ration des donn??es du capteur')
           # == Remplissage du tableau de donn??es des capteurs pour tous les pas de temps ==
           # Initialisation des tableaux de donn??es des capteurs
           columns_tableauDonneesCapteur = ['DATE_CAPTEUR', 'VALEUR_CAPTEUR']
           index_tableauDonneesCapteur = range(NB_MINUTES)
           df_tableauDonneesCapteur = pd.DataFrame(columns=columns_tableauDonneesCapteur, index=index_tableauDonneesCapteur)
           df_tableauDonneesCapteur['DATE_CAPTEUR'] = DATE_DEBUT + pd.to_timedelta(df_tableauDonneesCapteur.index, unit='m')
           # Envoi de x requ??tes HTTP pour r??cup??rer les donn??es par paquets de 30 jours
           x = math.ceil(NB_JOURS/30)
           for k in range(0, x):
               if debug : print(k/x)
               START_DATE = DATE_DEBUT + timedelta(days=30*k)
               END_DATE = START_DATE + timedelta(days=30)
               START_DATE = START_DATE.strftime("%Y-%m-%dT%H%%3A%M%%3A%S") # pour la requ??te HTTP
               END_DATE = END_DATE.strftime("%Y-%m-%dT%H%%3A%M%%3A%S") # pour la requ??te HTTP
               # Ecriture de la requ??te HTTP
               strURL = 'http://es2.gses.gdfsuez.net:8080/m2m/api/v3/properties/0/controllers/0/measures_points/' + str(df_tableauCapteur['NUM_CAPTEUR'][i]) + '/historicals?start_date=' + START_DATE + '&end_date=' + END_DATE
               # Envoi de la requ??te HTTP
               response = requests.get(strURL, headers=headers)
               # Si la requ??te a r??ussi, r??cup??ration des valeurs
               if response.status_code == 200:
                   # -- Remplissage du tableau de donn??es des capteurs pour les valeurs --
                   response_json = response.json()
                   for valeur in response_json.values():
                       for point in valeur:
                           try:
                               h = datetime.strptime(point['datetime'], '%Y-%m-%dT%H:%M:%S%z')
                           except:
                               h = datetime.strptime(point['datetime'][:-6], '%Y-%m-%dT%H:%M:%S')
                           h = h.replace(second=0,tzinfo=None)
                           df_tableauDonneesCapteur.loc[self.to_minutes(h-DATE_DEBUT),'VALEUR_CAPTEUR'] = point['value']
               else:
                   print('erreur BM104 - API Cofely Vision indisponible, r??essayer plus tard. Si l\'erreur se reproduit, contacter Cylergie.')
                   
                   
           # /// Retraitement des valeurs ///
           if debug : print('- Retraitement des valeurs')
           # == Moyennage temporel ==
           periode = '1H'
           try:
               if df_tableauCapteur['UNITE_CAPTEUR'][i] in ('Wh', 'kWh', 'MWh', 'GWh'):
                   d = df_tableauDonneesCapteur
                   # Conversion de la mesure en float pour pouvoir calculer la moyenne
                   d = d.astype({'VALEUR_CAPTEUR':'float'}) 
                   # Correction des valeurs aberrantes avec compteur d'??nergie non continu
                   d = d.sort_values(by=['DATE_CAPTEUR'])
                   d = d.dropna()
                   while not d[d['VALEUR_CAPTEUR'] < d['VALEUR_CAPTEUR'].shift(+1)].empty:
                       d.drop(d[d['VALEUR_CAPTEUR'] < d['VALEUR_CAPTEUR'].shift(+1)].index, inplace=True)
                   # Moyenne au pas de temps horaire                
                   d.index = d['DATE_CAPTEUR']
                   A0 = d.resample(periode).fillna("pad")
                   A0['DATE_CAPTEUR'] = A0.index
                   # Pr??-traitement
                   # Passage d'??nergie ?? puissance
                   A0['TpsDiff'] = A0['DATE_CAPTEUR'].diff() # Cr??ation d'une colonne repr??sentant l'intervalle de temps entre deux lignes
                   A0['TpsDiff'] = A0['TpsDiff'].dt.total_seconds().div(3600, fill_value=0) # Conversion de cette colonne en heure (en passant par les secondes)
                   A0['VALEUR_CAPTEUR_ENERGIE'] = A0['VALEUR_CAPTEUR'] # Sauvergarde de la donn??e brute
                   A0['VALEUR_CAPTEUR'] = A0['VALEUR_CAPTEUR_ENERGIE'].diff().div(A0['TpsDiff'], axis=0) # C??ation d'une matrice des puissances ?? partir des donn??es d'??nergie et des intervalles de temps entre deux lignes
                   A0.drop(A0.tail(1).index, inplace=True)
               else:
                   d = df_tableauDonneesCapteur
                   # Conversion de la mesure en float pour pouvoir calculer la moyenne
                   d = d.astype({'VALEUR_CAPTEUR':'float'})
                   # Correction des valeurs aberrantes avec compteur d'??nergie non continu
                   d = d.sort_values(by=['DATE_CAPTEUR'])
                   d.drop(d[d['VALEUR_CAPTEUR'] < d['VALEUR_CAPTEUR'][0]].index, inplace=True)
                   d = d.dropna()
                   # Moyenne au pas de temps horaire
                   A0 = d.resample(periode, on='DATE_CAPTEUR', closed='right', label='right').mean()
               # == Suppression des points trop ??loign??s de la moyenne ou n??gatifs ==
               A0[A0['VALEUR_CAPTEUR'] > 4*A0[A0['VALEUR_CAPTEUR'] != 0]['VALEUR_CAPTEUR'].mean()] = np.nan
               A0[A0['VALEUR_CAPTEUR'] < 0] = np.nan
           except:
               A0 = df_tableauDonneesCapteur
           
           # /// Application du facteur correctif ///
           if debug : print('- Application du facteur correctif')
           A0['VALEUR_CAPTEUR'] = A0['VALEUR_CAPTEUR'] * df_tableauCapteur['F_CORR'][i]

           # /// Remplissage de la colonne DEMANDE_RESEAU ///
           if debug : print('- Remplissage de la colonne DEMANDE_RESEAU')
           i0 = 0
           for heures in range(NB_HEURES):
               for i in range(i0,len(A0.index),1):
                   if A0.index[i] == df_tableauSortie['DATE'][heures]:
                       df_tableauSortie['DEMANDE_RESEAU'][heures] += A0['VALEUR_CAPTEUR'][i]
                       i0 = i
                       break
               
        # --------- Donn??es de sorties ---------
        historiqueDemande = df_tableauSortie
        if debug : print('---------- Fin r??cup??ration des donn??es Cofely Vision ----------')
        return historiqueDemande
   
    def DonneesMeteo(self):
        """Fonction qui permet de r??cup??rer et traiter les donn??es m??t??o via M??t??oCiel
        
        Pour une station m??t??o donn??e, on r??cup??re l'historique et la pr??vision des donn??es m??t??o.
        Les donn??es m??t??o comprennent l'humidit?? et la temp??rature.
        
        Args:
            self : Ensemble des param??tres de la configuration notamment la localisation g??ographique de la station m??t??o
    
        Returns:
            L'historique et la pr??vision de la m??t??o au pas de temps horaire
            
        #TODO s'assurer que l'on peut bien utiliser les donn??es m??t??o comme on le fait
        #TODO d??couper la fonction en deux : une fonction pour l'historique, une fonction pour la pr??vision
    
        """
        
        if debug : print('---------- D??but r??cup??ration des donn??es m??t??o ----------')
        
        # --------- Donn??es d???entr??es ---------
        # Localisation
        VILLE = self.localisationVille
        # R??cup??ration des identifiants de la station m??t??o
        df = pd.read_csv("BDD_MeteoCiel.csv", sep=";")
        for i in range(len(df)):
            if df['Station'][i] == VILLE:
                ID_HISTO = str(int(df['ID_HISTO'][i]))
                ID_PREV = str(int(df['ID_PREV'][i]))
                NOM = df['NOM'][i]
        # Dates
        DERNIERE_DATE = self.dateDernieresDonnees # on r??cup??re la date des derni??res donn??es t??l??charg??es
        DATE_MAINTENANT = self.dateMaintenant # on r??cup??re la date actuelle (au moment du lancement de l'API IA)
        
        # --------- D??finition de la plage d?????tude ---------
        # D??but de la plage d'??tude 
        if DERNIERE_DATE != None:
            if (DERNIERE_DATE-DATE_MAINTENANT).days <= 365:
                DATE_DEBUT = DERNIERE_DATE + timedelta(hours=1)
                DATE_DEBUT = DATE_DEBUT.replace(minute=0, second=0, microsecond=0)
            else:
                DATE_DEBUT = DATE_MAINTENANT - timedelta(hours=8760)
                DATE_DEBUT = DATE_DEBUT.replace(minute=0, second=0, microsecond=0)
        else:
            DATE_DEBUT = DATE_MAINTENANT - timedelta(hours=8760)
            DATE_DEBUT = DATE_DEBUT.replace(minute=0, second=0, microsecond=0)
        # Fin de la plage d'??tude
        DATE_FIN = DATE_MAINTENANT
        DATE_FIN = DATE_FIN.replace(minute=0, second=0, microsecond=0)
        # Elements de comptage
        NB_HEURES_Reel = math.floor((DATE_FIN-DATE_DEBUT).total_seconds() / 3600) # Nombre d'heures dont il faut les donn??es d'historique
        NB_JOURS = math.floor(NB_HEURES_Reel / 24)
        NB_HEURES_Predit = 10 * 24 # Nombre d'heures dont il faut les donn??es de pr??diction
        
        # --------- Donn??es de sorties ---------
        # Initialisation du tableau de sortie des donn??es r??elles
        columns_tableauSortie_Reel = ['DATE', 'T_EXT', 'HR']
        index_tableauSortie_Reel = range(NB_HEURES_Reel)
        df_tableauSortie_Reel = pd.DataFrame(index=index_tableauSortie_Reel, columns=columns_tableauSortie_Reel)
        for heures in range(NB_HEURES_Reel):
            df_tableauSortie_Reel['DATE'][heures] = DATE_DEBUT + timedelta(hours=heures)
        # Initialisation du tableau de sortie des donn??es de pr??visions
        columns_tableauSortie_Predit = ['DATE', 'T_EXT', 'HR']
        index_tableauSortie_Predit = range(NB_HEURES_Predit)
        df_tableauSortie_Predit = pd.DataFrame(index=index_tableauSortie_Predit, columns=columns_tableauSortie_Predit)
        for heures in range(NB_HEURES_Predit):
            df_tableauSortie_Predit['DATE'][heures] = DATE_FIN + timedelta(hours=heures)

        # --------- CALCUL ---------

        # A - R??cup??ration des donn??es r??elles
        if debug : print('--- R??cup??ration des donn??es r??elles ---')
        for jour in range(NB_JOURS+1):
            # R??cup??ration des num??ros de la date (jour, mois et ann??e)
            DATE = DATE_DEBUT + timedelta(days=jour)
            if debug : print('- ' + str(DATE))
            NUM_JOUR = str(DATE.day)
            NUM_MOIS = str(DATE.month - 1)
            NUM_ANNEE = str(DATE.year)
            # Ecriture de la requ??te HTTP
            strURL = 'https://www.meteociel.fr/temps-reel/obs_villes.php?code2=' + ID_HISTO + '&jour2=' + NUM_JOUR + '&mois2=' + NUM_MOIS + '&annee2=' + NUM_ANNEE + '.htm'
            # Envoi de la requ??te HTTP
            response = None
            soup = None
            waiter = 0
            while response is None and waiter < 25:
                response = urllib.request.urlopen(strURL)
                time.sleep(0.5)
                waiter += 1
            response = urllib.request.urlopen(strURL)
            soup = BeautifulSoup(response.read(),features="lxml")
            try:
                # R??cup??ration des valeurs
                for i in range(0, 24):
                    n = 24 - i + 1
    
                    # Heure
                    A = soup.select('body > table:nth-child(1) > tbody > tr.texte > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > center:nth-child(14) > table:nth-child(3) > tr:nth-child(' + str(n) + ') > td:nth-child(1)')
                    B = unicodedata.normalize("NFKD", str(A))
                    pos1 = B.find('>')+1
                    pos2 = B.find('h')
                    try:
                        C = float(B[pos1:pos2])
                    except:
                        C = np.nan
                    heure = C
    
                    # S'il existe une ligne pour l'heure consid??r??e
                    if not np.isnan(heure):
    
                        # Temp??rature ext??rieure
                        A = soup.select('body > table:nth-child(1) > tbody > tr.texte > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > center:nth-child(14) > table:nth-child(3) > tr:nth-child(' + str(n) + ') > td:nth-child(5) > div')
                        B = unicodedata.normalize("NFKD", str(A))
                        pos1 = B.find('>')+1
                        pos2 = B.find('??C')
                        try:
                            C = float(B[pos1:pos2])
                        except:
                            C = np.nan
                        df_tableauSortie_Reel['T_EXT'][df_tableauSortie_Reel['DATE'] == DATE.replace(hour=0) + timedelta(hours=heure)] = C
    
                        # Humidit?? relative
                        A = soup.select('body > table:nth-child(1) > tbody > tr.texte > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > center:nth-child(14) > table:nth-child(3) > tr:nth-child(' + str(n) + ') > td:nth-child(6) > div')
                        B = unicodedata.normalize("NFKD", str(A))
                        pos1 = B.find('>')+1
                        pos2 = B.find('%')
                        try:
                            C = float(B[pos1:pos2])
                        except:
                            C = np.nan
                        df_tableauSortie_Reel['HR'][df_tableauSortie_Reel['DATE'] == DATE.replace(hour=0) + timedelta(hours=heure)] = C
            except:
                print('erreur BM105 - API m??t??o indisponible, r??essayer plus tard. Si l\'erreur se reproduit, contacter Cylergie.')
                        
        # B - R??cup??ration des donn??es de pr??visions
        if debug : print('--- R??cup??ration des donn??es de pr??visions ---')

        # B.1 ??? Import des donn??es de pr??vision toutes les 3 heures pour les 4 prochains jours
        if debug : print('- Import des donn??es de pr??vision toutes les 3 heures pour les 4 prochains jours')
        # Ecriture de la requ??te HTTP
        strURL = 'https://www.meteociel.fr/previsions/' + ID_PREV + '/' + NOM + '.htm'
        # Envoi de la requ??te HTTP
        response = urllib.request.urlopen(strURL)
        soup = BeautifulSoup(response.read(),features="lxml")
        try:      
            # R??cup??ration de la premi??re heure de pr??vision disponible
            day = DATE_MAINTENANT
            A = soup.select('body > table:nth-child(4) > tbody > tr.texte > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > center:nth-child(4) > table > tr > td:nth-child(1) > table:nth-child(1) > tr:nth-child(3) > td:nth-child(2)')
            B = unicodedata.normalize("NFKD", str(A))
            pos1 = B.find('>')+1
            pos2 = B.find(':')
            try:
                C = int(B[pos1:pos2])
                day = day.replace(hour=int(C), minute=0, second=0, microsecond=0)
            except:
                C = np.nan
    
            # R??cup??ration des valeurs
            for i in range(0, 24*4, 3):
                n = i/3 + 3
    
                # Temp??rature ext??rieure
                A = soup.select('body > table:nth-child(4) > tbody > tr.texte > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > center:nth-child(4) > table > tr > td:nth-child(1) > table:nth-child(1) > tr:nth-child(' + str(int(n)) + ') > td:nth-child(2)')
                B = unicodedata.normalize("NFKD", str(A))
                pos1 = B.find('>')+1
                pos2 = B.find('??C')
                try:
                    C = float(B[pos1:pos2])
                except:
                    C = np.nan
                if np.isnan(C):
                    A = soup.select('body > table:nth-child(4) > tbody > tr.texte > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > center:nth-child(4) > table > tr > td:nth-child(1) > table:nth-child(1) > tr:nth-child(' + str(int(n)) + ') > td:nth-child(3)')
                    B = unicodedata.normalize("NFKD", str(A))
                    pos1 = B.find('>')+1
                    pos2 = B.find('??C')
                    try:
                        C = float(B[pos1:pos2])
                    except:
                        C = np.nan
                if np.isnan(C):
                    A = soup.select('body > table:nth-child(4) > tbody > tr.texte > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > center:nth-child(4) > table > tr > td:nth-child(1) > table:nth-child(1) > tr:nth-child(' + str(int(n)) + ') > td:nth-child(2) > font')
                    B = unicodedata.normalize("NFKD", str(A))
                    pos1 = B.find('>')+1
                    pos2 = B.find('??C')
                    try:
                        C = float(B[pos1:pos2])
                    except:
                        C = np.nan
                df_tableauSortie_Predit['T_EXT'][df_tableauSortie_Predit['DATE'] == day + timedelta(hours=i)] = C
    
                # Humidit?? relative
                A = soup.select('body > table:nth-child(4) > tbody > tr.texte > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > center:nth-child(4) > table > tr > td:nth-child(1) > table:nth-child(1) > tr:nth-child(' + str(int(n)) + ') > td:nth-child(8)')
                B = unicodedata.normalize("NFKD", str(A))
                pos1 = B.find('>')+1
                pos2 = B.find('%')
                try:
                    C = float(B[pos1:pos2])
                except:
                    C = np.nan
                if np.isnan(C):
                    A = soup.select('body > table:nth-child(4) > tbody > tr.texte > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > center:nth-child(4) > table > tr > td:nth-child(1) > table:nth-child(1) > tr:nth-child(' + str(int(n)) + ') > td:nth-child(9)')
                    B = unicodedata.normalize("NFKD", str(A))
                    pos1 = B.find('>')+1
                    pos2 = B.find('%')
                    try:
                        C = float(B[pos1:pos2])
                    except:
                        C = np.nan
                df_tableauSortie_Predit['HR'][df_tableauSortie_Predit['DATE'] == day + timedelta(hours=i)] = C
        except:
            print('erreur BM105 - API m??t??o indisponible, r??essayer plus tard. Si l\'erreur se reproduit, contacter Cylergie.')
                 
        # B.2 ??? Import des donn??es de pr??vision toutes les 6 heures pour les 3 ?? 10 jours ?? venir
        if debug : print('- Import des donn??es de pr??vision toutes les 6 heures pour les 3 ?? 10 jours ?? venir')
        # Ecriture de la requ??te HTTP
        strURL = 'https://www.meteociel.fr/tendances/' + ID_PREV + '/' + NOM + '.htm'
        # Envoi de la requ??te HTTP
        response = urllib.request.urlopen(strURL)
        soup = BeautifulSoup(response.read(),features="lxml")
        try:  
            # R??cup??ration de la premi??re heure de pr??vision disponible
            day = DATE_MAINTENANT + timedelta(days=3)
            A = soup.select('body > table:nth-child(4) > tbody > tr.texte > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > center:nth-child(4) > table > tr > td:nth-child(1) > table:nth-child(1) > tr:nth-child(3) > td:nth-child(2)')
            B = unicodedata.normalize("NFKD", str(A))
            pos1 = B.find('>')+1
            pos2 = B.find(':')
            try:
                C = int(B[pos1:pos2])
                day = day.replace(hour=C, minute=0, second=0, microsecond=0)
            except:
                C = math.nan
    
            # R??cup??ration des valeurs
            for i in range(0, 24*7, 6):
                n = i/6 + 3
    
                # Temp??rature ext??rieure
                A = soup.select('body > table:nth-child(4) > tbody > tr.texte > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > center:nth-child(4) > table > tr > td:nth-child(1) > table:nth-child(1) > tr:nth-child(' + str(int(n)) + ') > td:nth-child(2)')
                B = unicodedata.normalize("NFKD", str(A))
                pos1 = B.find('>')+1
                pos2 = B.find('??C')
                try:
                    C = float(B[pos1:pos2])
                except:
                    C = np.nan
                if np.isnan(C):
                    A = soup.select('body > table:nth-child(4) > tbody > tr.texte > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > center:nth-child(4) > table > tr > td:nth-child(1) > table:nth-child(1) > tr:nth-child(' + str(int(n)) + ') > td:nth-child(3)')
                    B = unicodedata.normalize("NFKD", str(A))
                    pos1 = B.find('>')+1
                    pos2 = B.find('??C')
                    try:
                        C = float(B[pos1:pos2])
                    except:
                        C = np.nan
                if np.isnan(C):
                    A = soup.select('body > table:nth-child(4) > tbody > tr.texte > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > center:nth-child(4) > table > tr > td:nth-child(1) > table:nth-child(1) > tr:nth-child(' + str(int(n)) + ') > td:nth-child(3) > font')
                    B = unicodedata.normalize("NFKD", str(A))
                    pos1 = B.find('>')+1
                    pos2 = B.find('??C')
                    try:
                        C = float(B[pos1:pos2])
                    except:
                        C = np.nan        
                df_tableauSortie_Predit['T_EXT'][df_tableauSortie_Predit['DATE'] == day + timedelta(hours=i)] = C
    
                # Humidit?? relative
                A = soup.select('body > table:nth-child(4) > tbody > tr.texte > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > center:nth-child(4) > table > tr > td:nth-child(1) > table:nth-child(1) > tr:nth-child(' + str(int(n)) + ') > td:nth-child(8)')
                B = unicodedata.normalize("NFKD", str(A))
                pos1 = B.find('>')+1
                pos2 = B.find('%')
                try:
                    C = float(B[pos1:pos2])
                except:
                    C = np.nan
                if np.isnan(C):
                    A = soup.select('body > table:nth-child(4) > tbody > tr.texte > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > center:nth-child(4) > table > tr > td:nth-child(1) > table:nth-child(1) > tr:nth-child(' + str(int(n)) + ') > td:nth-child(9)')
                    B = unicodedata.normalize("NFKD", str(A))
                    pos1 = B.find('>')+1
                    pos2 = B.find('%')
                    try:
                        C = float(B[pos1:pos2])
                    except:
                        C = np.nan
                df_tableauSortie_Predit['HR'][df_tableauSortie_Predit['DATE'] == day + timedelta(hours=i)] = C
        except:
            print('erreur BM105 - API m??t??o indisponible, r??essayer plus tard. Si l\'erreur se reproduit, contacter Cylergie.')
                     
        # B.3 - R??chantillonage pour combler les trous dans les pr??visions
        if debug : print('- R??chantillonage pour combler les trous dans les pr??visions')
        df_tableauSortie_Predit['T_EXT'] = df_tableauSortie_Predit['T_EXT'].astype(float).interpolate(method='linear', limit_area='inside')
        df_tableauSortie_Predit['HR'] = df_tableauSortie_Predit['HR'].astype(float).interpolate(method='linear', limit_area='inside')

        # --------- Donn??es de sorties ---------
        historiqueMeteo = df_tableauSortie_Reel
        previsionMeteo = df_tableauSortie_Predit
        if debug : print('---------- Fin r??cup??ration des donn??es m??t??o ----------')
        return historiqueMeteo, previsionMeteo        
        

    def IA(self):
        """Fonction qui permet de pr??dire une demande du r??seau
        
        Fonctionnement : 
            - t??l??chargement et mise en forme des donn??es d'entr??es (historique demande, historique m??t??o et pr??vision m??t??o)
                * soit des donn??es historique ont d??j?? ??t?? r??cup??r??es et on compl??te ces donn??es pour avoir un an de donn??es
                * soit on t??l??charge un historique d'un an de donn??es
            - appel ?? l'API
            - r??cup??ration et mise en forme de la pr??vision de la demande
            - Enregistrement des r??sultats dans des fichiers pickle
                * authentification --> DFtoCSV (donn??es historique)
                * authentification_meteo --> previsionMeteo
                * authentification_demande --> previsionDemande
        
        Args:
            self : Ensemble des param??tres de la configuration notamment le num??ro de la configuration
    
        Returns:
            La pr??vision de la demande du r??seau au pas de temps horaire
                
        """

        if debug : print('---------- D??but calcul pr??visionnel avec l\'IA ----------')
        
        # --------- Donn??es d???entr??es ---------
        if debug : print('--- R??cup??ration des donn??es d\'entr??es ---')
        # Nombre de jours de pr??visions
        Nb_jours_prevision = 11
        # Chargement des donn??es historique d??j?? r??cup??r??es
        try: # Tentative d'ouverture du fichier de donn??es
            with open(str(self.authentification)+'.pickle', 'rb') as BDD:
                if debug : print('- Fichier historique ' + self.authentification + '.pickle' + ' trouv??')
                # Chargement des donn??es
                self.BDD_historique = pickle.load(BDD)
                # Suppression des lignes cr????es pour la pr??vision
                self.BDD_historique.drop(self.BDD_historique.columns[[3,4]], axis = 1, inplace = True) 
                while np.isnan(self.BDD_historique['heat.hist'][-1]) and np.isnan(self.BDD_historique['temp.hist'][-1]) and np.isnan(self.BDD_historique['humi.hist'][-1]):
                    self.BDD_historique.drop(self.BDD_historique.tail(1).index,inplace=True)
                # R??cup??ration de la derni??re date de la base de donn??es
                self.dateDernieresDonnees = self.BDD_historique.index[-1]
                if debug : print('- Derni??re donn??e datant du ' + str(self.dateDernieresDonnees))
                # Renomage des colonnes ?? supprimer si non n??cessaire
                self.BDD_historique.rename(columns={"time":"DATE","heat.hist":"DEMANDE_RESEAU","temp.hist":"T_EXT","humi.hist":"HR"},inplace=True)
                self.BDD_historique.insert(0, 'DATE', self.BDD_historique.index, allow_duplicates = False)
                # Chargement de la BDD r??alis??
                self.BDD_ok = True
        except OSError: # Si le fichier de donn??es n'existe pas
            if debug : print('Fichier historique ' + str(self.authentification) + '.pickle' + ' non trouv??')
            self.BDD_ok = False
            self.dateDernieresDonnees = None
        # Dates
        DERNIERE_DATE = self.dateDernieresDonnees # on r??cup??re la date des derni??res donn??es t??l??charg??es
        DATE_MAINTENANT = self.dateMaintenant # on r??cup??re la date actuelle (au moment du lancement de l'API IA)

       
        # --------- Lancement de la pr??vision de la demande (si n??cessaire) ---------
        if DERNIERE_DATE == None or (DATE_MAINTENANT-DERNIERE_DATE).total_seconds() /3600 >= 2:
            
            # --- Donn??es de sorties ---
            previsionDemande = pd.DataFrame(columns=['DATE', 'DEMANDE'])
            DATE_PREDITE = []
            DEMANDE_RESEAU_PREDITE = []
            for i in range (0,240):
                DATE_PREDITE.append(DERNIERE_DATE + timedelta(hours=i))
                DEMANDE_RESEAU_PREDITE.append(np.nan)
            
            # --- D??finition de la plage d?????tude ---
            # D??but de la plage d'??tude
            DATE_DEBUT = DATE_MAINTENANT - timedelta(hours=8760)
            DATE_DEBUT = DATE_DEBUT.replace(minute=0, second=0, microsecond=0)
            # Fin de la plage d'??tude
            DATE_FIN = DATE_MAINTENANT + timedelta(days=Nb_jours_prevision)
            DATE_FIN = DATE_FIN.replace(minute=0, second=0, microsecond=0)  
        
            # --- Construction du fichier d'entr??es de l'IA ---
            if debug : print('--- Construction du fichier d\'entr??es de l\'IA ---')
            # /// Initialisation du fichier d'appel ?? l'IA ///
            index_DFtoCSV = pd.date_range(start=DATE_DEBUT, end=DATE_FIN, freq='1H')
            columns_DFtoCSV = ['time']
            DFtoCSV = pd.DataFrame(data=index_DFtoCSV, columns=columns_DFtoCSV)
            DFtoCSV['time'] = pd.to_datetime(DFtoCSV['time'])
            DFtoCSV.set_index('time', inplace=True)
            # /// R??cup??ration des donn??es historique et pr??vision ///
            if self.BDD_ok:
                # Chargement de l'historique existant
                historiqueDemande_1 = self.BDD_historique[['DATE','DEMANDE_RESEAU']]
                historiqueMeteo_1 = self.BDD_historique[['DATE','T_EXT','HR']]
                # T??l??chargement de l'historique manquant et des pr??visions m??t??o si besoin
                historiqueDemande_2 = self.DonneesCofelyVision()
                [historiqueMeteo_2, previsionMeteo] = self.DonneesMeteo()
                historiqueDemande = pd.concat([historiqueDemande_1, historiqueDemande_2], ignore_index=True)
                historiqueMeteo = pd.concat([historiqueMeteo_1, historiqueMeteo_2], ignore_index=True)
            else:
                # T??l??chargement de l'historique complet et des pr??visions m??t??o
                historiqueDemande = self.DonneesCofelyVision()
                [historiqueMeteo, previsionMeteo] = self.DonneesMeteo()
            # /// Mise en forme des donn??es re??ues ///
            historiqueDemande['time'] = pd.to_datetime(historiqueDemande['DATE'])
            historiqueMeteo['time'] = pd.to_datetime(historiqueMeteo['DATE'])
            previsionMeteo['time'] = pd.to_datetime(previsionMeteo['DATE'])
            historiqueDemande.set_index('time', inplace=True)
            historiqueMeteo.set_index('time', inplace=True)
            previsionMeteo.set_index('time', inplace=True)
            historiqueDemande = historiqueDemande.loc[~historiqueDemande.index.duplicated(), :]
            historiqueMeteo = historiqueMeteo.loc[~historiqueMeteo.index.duplicated(), :]
            previsionMeteo = previsionMeteo.loc[~previsionMeteo.index.duplicated(), :]
            # /// Remplissage du Dataframe pour l'IA ///
            # Ecriture des donn??es dans les bonnes colonnes
            DFtoCSV['heat.hist'] = historiqueDemande['DEMANDE_RESEAU']
            DFtoCSV['temp.hist'] = historiqueMeteo['T_EXT']
            DFtoCSV['humi.hist'] = historiqueMeteo['HR']
            DFtoCSV['temp.fore'] = previsionMeteo['T_EXT']
            DFtoCSV['humi.fore'] = previsionMeteo['HR']
            DFtoCSV = DFtoCSV[['heat.hist', 'temp.hist', 'humi.hist', 'temp.fore', 'humi.fore']]
            # Remise des donn??es au bon format
            DFtoCSV['heat.hist'] = DFtoCSV['heat.hist'].astype('float')
            DFtoCSV['temp.hist'] = DFtoCSV['temp.hist'].astype('float')
            DFtoCSV['humi.hist'] = DFtoCSV['humi.hist'].astype('float')
            DFtoCSV['humi.fore'] = DFtoCSV['humi.fore'].astype('float')
            DFtoCSV['temp.fore'] = DFtoCSV['temp.fore'].astype('float')
            DFtoCSV.sort_index(inplace=True)
            # Suppression des derni??res lignes si aucune donn??e de pr??vision
            while DFtoCSV.iloc[-1,:].isnull().sum()==5:
                DFtoCSV.drop(DFtoCSV.tail(1).index, inplace = True) 
            # /// Sauvegarde des donn??es historique ///
            with open(str(self.authentification)+'.pickle', 'wb') as BDD:
                pickle.dump(DFtoCSV, BDD)
            # /// Sauvegarde des donn??es de pr??vision m??t??o ///
            with open(str(self.authentification)+'_meteo.pickle', 'wb') as BDD:
                pickle.dump(previsionMeteo, BDD)
            # /// Ecriture des donn??es dans un fichier csv pour envoi ?? l'API IA ///
            filename = 'filetoIA.csv'
            DFtoCSV.to_csv(filename, encoding='utf-8', na_rep="", decimal=',', sep=';', date_format='%d/%m/%Y %H:%M')
            
            # --- Appel de l'IA ---
            if debug == 1 : print('--- Appel de l\'IA ---')
            # Status de fonctionnement de l'IA
            outcome_status = list()
            outcome_status.append("DONE")
            outcome_status.append("ERROR")
            # Param??tres de connexion ?? l'IA
            URL = "https://api.preprod.csai.crigen.myengie.com/bmc/" # API URL
            keyId = {'KeyId': '2a564819-f601-4e32-8be6-9863578d6353'} # keyId for the meeting     
            # Test de connexion
            API_ENDPOINT = URL + "health"
            requete = requests.get(url=API_ENDPOINT, headers=keyId)
            status = requete.status_code
            # Lancement de la pr??vision via l'API IA
            if status == 200: # connection ok
                data = {"network_name": "Network.001"}  # nom du site utilis??, ne sera pas utile dans la V2
                files = {'history': (filename, open(filename, 'rb')),} # nom du fichier de donn??es
                # Envoi de la requ??te
                reponse = requests.post(url=URL+'inferences', data=data, files=files, headers=keyId)
                token = reponse.json()['token']
                task_status = ""
                while task_status not in outcome_status:
                    requete1 = requests.get(url=URL + "tasks/" + token, headers=keyId)
                    task_status = requete1.json()["status"]
                    time.sleep(1)
                if task_status == 'DONE':
                    requete2 = requests.get(url=URL+ "/tasks/" + token, headers=keyId)
                    reponse2 = requests.get(url=URL + "inferences/" + requete2.json()['resourceId'], headers=keyId)
                    # R??cuperation des donn??es
                    Data = reponse2.json()
                    # R??cup??ration des donn??es de pr??visions
                    for index in range(len(Data[0]['inferenceResult'])):
                        for i in range (0,240):
                            if DATE_PREDITE[i].strftime("%Y-%m-%d %H:%M:%S") == Data[0]['inferenceResult'][index]['date']:
                                if isinstance(Data[0]['inferenceResult'][index]['value'], str):
                                    DEMANDE_RESEAU_PREDITE[i] = Data[0]['inferenceResult'][index]['value']
                                else:
                                    DEMANDE_RESEAU_PREDITE[i] = round(Data[0]['inferenceResult'][index]['value'], 2)
                elif task_status == 'ERROR':
                    print('erreur BM101 - Contacter Cylergie.')
                else:
                    print('erreur BM102 - Contacter Cylergie.')
            else:
                print('erreur BM103 - API IA indisponible, r??essayer plus tard. Si l\'erreur se reproduit, contacter Cylergie.')

            # --- Donn??es de sorties ---
            previsionDemande['DATE'] = DATE_PREDITE
            previsionDemande['DEMANDE'] = DEMANDE_RESEAU_PREDITE
        
        else:
            # Chargement des donn??es historique d??j?? r??cup??r??es
            with open(str(self.authentification)+'_demande.pickle', 'rb') as BDD:
                if debug : print('- Fichier pr??vision ' + self.authentification + '_demande.pickle' + ' trouv??')
                # Chargement des donn??es
                previsionDemande = pickle.load(BDD)

        # --------- Donn??es de sorties ---------
        # Sauvegarde des pr??visions de la demande
        with open(str(self.authentification)+'_demande.pickle', 'wb') as BDD:
            if debug : print('--- Sauvegarde de la prevision demande de chaleur ---')
            pickle.dump(previsionDemande, BDD)
        if debug : print('---------- Fin calcul pr??visionnel avec l\'IA ----------')
        return previsionDemande


    def FonctionnementChaudiere(self):
        """Fonction qui permet de simuler le fonctionnement de la chaufferie et des chaudi??res
        
        Fonctionnement :
            - Appel de la fonction IA pour r??cup??rer la demande du r??seau
            - Simulation de la cascade des chaudi??res pour couvrir la demande du r??seau
            - Calcul du besoin de biomasse pour faire fonctionner les chaudi??res
            - Enregistrement des r??sultats dans un fichier pickle
                * authentification_biomasse --> previsionBesoinBiomasse
        
        Args:
            self : Ensemble des param??tres de la configuration notamment les param??tres de la chaufferie
    
        Returns:
            Le besoin de biomasse au pas de temps horaire sur les 10 jours ?? venir
            
        #TODO ajouter un param??tre pour faire une alimentation de chaudi??re mixte cad par plusieurs silos
                    
        """
        
        if debug : print('---------- D??but calcul du fonctionnement des chaudi??res ----------')
            
        # --------- Donn??es d???entr??es ---------
        # Tableau de la demande du r??seau pr??dite
        columns_tableauEntrees = ['DATE', 'DEMANDE']
        data_tableauEntrees = self.IA()
        df_tableauEntree = pd.DataFrame(data=data_tableauEntrees, columns=columns_tableauEntrees)
        df_tableauEntree['DATE'] = pd.to_datetime(df_tableauEntree['DATE'])
        DEMANDE = df_tableauEntree['DEMANDE'].astype(float)
        # Caract??ristiques de la chaufferie
        IS_COGE = self.isCoge # Pr??sence d'une cog??n??ration
        P_BASE = self.pCoge # Puissance d'un syst??me en base
        PILOTAGE = self.typePilotage # Type de pilotage des chaudi??res
        NB_SILO = self.nbSilo # Nombre de silo r??pondant ?? la m??me demande r??seau
        PCI = self.pciBois # PCI du bois de chaque silo
        DENSITE = self.densiteBois # Densit?? du bois de chaque silo
        NB_CHAUDIERE = self.nbChaudiere # Nombre de chaudi??res associ??es ?? chaque silo
        # Caract??ristiques des chaudi??res
        PRIORITE = self.prioriteChaudiere # Priorit?? d'allumage des chaudi??res
        SILO = self.siloChaudiere # Silo d'appartenance des chaudi??res
        P_NOM = self.pNomChaudiere # Puissance nominale des chaudi??res
        RENDEMENT = self.rendementChaudiere # Rendement des chaudi??res
        P_MIN = self.pMinChaudiere # Puissance minimale des chaudi??res
        CHARGE = self.chargeChaudiere # Charge des chaudi??res
        
        if debug : 
            print('Valeur : IS_COGE')
            print(IS_COGE)
            print('Valeur : P_BASE')
            print(P_BASE[0])
            print('Dimensions : P_BASE --> ' + str(len(P_BASE)))
            print('Valeur : PILOTAGE')
            print(PILOTAGE)
            print('Valeur : NB_SILO')
            print(NB_SILO)
            print('Valeur : PCI')
            print(PCI[0])
            print('Dimensions : PCI --> ' + str(len(PCI)))
            print('Valeur : DENSITE')
            print(DENSITE[0])
            print('Dimensions : DENSITE --> ' + str(len(DENSITE)))
            print('Valeur : NB_CHAUDIERE')
            print(NB_CHAUDIERE)
            print('Valeur : PRIORITE')
            print(PRIORITE)
            print('Valeur : SILO')
            print(SILO)
            print('Valeur : P_NOM')
            print(P_NOM)
            print('Valeur : RENDEMENT')
            print(RENDEMENT[0])
            print('Dimensions : RENDEMENT --> ' + str(len(RENDEMENT)))
            print('Valeur : P_MIN')
            print(P_MIN[0])
            print('Dimensions : P_MIN --> ' + str(len(P_MIN)))
            print('Valeur : CHARGE')
            print(CHARGE[0])
            print('Dimensions : CHARGE --> ' + str(len(CHARGE)))
            
        
        # --------- D??finition de la plage d?????tude ---------
        DATE_DEBUT = df_tableauEntree['DATE'][0]
        DATE_FIN = df_tableauEntree['DATE'][len(df_tableauEntree)-1]
        NB_HEURES = math.floor((DATE_FIN-DATE_DEBUT).total_seconds() / 3600) + 1
        if debug : 
            print('Valeur : DATE_DEBUT')
            print(DATE_DEBUT)
            print('Valeur : DATE_FIN')
            print(DATE_FIN)
            print('Valeur : NB_HEURES')
            print(NB_HEURES)
        
        # --------- Param??tres interm??diaires ---------
        NB_CHAUDIERE_TOTAL = int(sum(NB_CHAUDIERE)) # Nombre de chaudi??res biomasse total
        NB_ALLUME = NB_CHAUDIERE_TOTAL # Nombre de chaudi??res biomasse qui doivent ??tre allum??es pour r??pondre ?? la demande r??seau (pour le cas d'un pilotage de type maximum de chaudi??res)
        if debug : 
            print('Valeur : NB_CHAUDIERE_TOTAL')
            print(NB_CHAUDIERE_TOTAL)
            print('Valeur : NB_ALLUME')
            print(NB_ALLUME)
        CH_NUM = np.zeros(NB_CHAUDIERE_TOTAL, int) # Variable permettant de classer les chaudi??res par num??ro de priorit??
        CPT = -1 # Compteur
        
        # Compl??ment du tableau de donn??es d'entr??es
        P_BIOMASSE_CH = np.zeros([NB_HEURES, NB_CHAUDIERE_TOTAL]) # Puissance ?? fournir pour chaque chaudi??re biomasse
        P_DISPO_CH = np.zeros([NB_HEURES, NB_CHAUDIERE_TOTAL]) # Puissance disponible pour chaque chaudi??re biomasse
        P_BIOMASSE = np.zeros(NB_HEURES) # Puissance totale restant ?? fournir pour toutes les chaudi??res biomasse
        P_DISPO = np.zeros(NB_HEURES) # Puissance totale disponible pour toutes les chaudi??res biomasse

        # --------- Donn??es de sorties ---------
        # Initialisation du tableau de sortie
        columns_tableauSortie = ['DATE']
        for i in range(NB_SILO):
            columns_tableauSortie += ['BESOIN_BIOMASSE_SILO'+str(i+1)]
        df_tableauSortie = pd.DataFrame(columns=columns_tableauSortie)
        # Remplissage de la colonne DATE
        df_tableauSortie['DATE'] = df_tableauEntree['DATE']

        # --------- CALCUL ---------

        # /// Calcul de la puissance ?? fournir par l'ensemble de chaudi??res biomasse ///
        if debug : print('--- Calcul de la puissance ?? fournir par l\'ensemble de chaudi??res biomasse ---')
        for i in range(NB_HEURES):
            if IS_COGE[0]: #TODO JLE mettre is coge sur 240 valeurs
                if DEMANDE[i] - P_BASE[i] > 0:
                    P_BIOMASSE[i] = DEMANDE[i] - P_BASE[i]
                else:
                    P_BIOMASSE[i] = 0.0
            else:
                P_BIOMASSE[i] = DEMANDE[i]
        if debug : 
            print('Valeur : DEMANDE')
            print(DEMANDE)
            print('Valeur : P_BIOMASSE')
            print(P_BIOMASSE)
        
        # /// Calcul de la puissance disponible pour chaque chaudi??re biomasse ///
        if debug : print('--- Calcul de la puissance disponible pour chaque chaudi??re biomasse ---')
        for ch in range(NB_CHAUDIERE_TOTAL):
            P_DISPO_CH[:, ch] = P_NOM[ch] * CHARGE[:, ch] / 100
            for i in range(NB_HEURES):
                if P_DISPO_CH[i, ch] < P_MIN[i, ch]:
                    P_DISPO_CH[i, ch] = 0
        if debug : 
            print('Valeur : P_DISPO_CH')
            print(P_DISPO_CH[0])
            print('Dimensions : P_DISPO_CH --> ' + str(len(P_DISPO_CH)))
        
        # /// Reclassement des chaudi??res biomasse par ordre de priorit?? ///
        if debug : print('--- Reclassement des chaudi??res biomasse par ordre de priorit?? ---')
        for ch in range(NB_CHAUDIERE_TOTAL):
            CH_NUM[PRIORITE[ch]-1] = ch
        if debug : 
            print('Valeur : CH_NUM')
            print(CH_NUM)
        
        # /// Calcul de la puissance ?? fournir pour chaque chaudi??re biomasse ///
        if debug : print('--- Calcul de la puissance ?? fournir pour chaque chaudi??re biomasse ---')
        for i in range(NB_HEURES):
            if PILOTAGE == 1: # Pilotage de type minimum de chaudi??res
                for ch in range(NB_CHAUDIERE_TOTAL):
                    if P_BIOMASSE[i] > 0:
                        if P_BIOMASSE[i] > P_DISPO_CH[i, CH_NUM[ch]]:
                            P_BIOMASSE_CH[i, CH_NUM[ch]] = P_DISPO_CH[i, CH_NUM[ch]]
                            P_BIOMASSE[i] -= P_BIOMASSE_CH[i, CH_NUM[ch]]
                        else:
                            if P_BIOMASSE[i] < P_MIN[i,CH_NUM[ch]]:
                                P_BIOMASSE_CH[i, CH_NUM[ch]] = 0
                            else:
                                P_BIOMASSE_CH[i, CH_NUM[ch]] = P_BIOMASSE[i]
                                P_BIOMASSE[i] -= P_BIOMASSE_CH[i, CH_NUM[ch]]
                    else:
                        P_BIOMASSE_CH[i, CH_NUM[ch]] = 0

            elif PILOTAGE == 2: # Pilotage de type maximum de chaudi??res
                CPT = 0
                # On allume toutes les chaudi??res possibles
                NB_ALLUME = NB_CHAUDIERE_TOTAL
                for ch in range(NB_CHAUDIERE_TOTAL):
                    if P_DISPO_CH[i, CH_NUM[ch]] == 0:
                        NB_ALLUME -= 1       
                # On calcule la puissance disponible totale
                for ch in range(NB_CHAUDIERE_TOTAL):
                    P_DISPO[i] += P_DISPO_CH[i, CH_NUM[ch]]
                # Calcul de la cascade
                while CPT != NB_ALLUME:
                    for ch in range(NB_ALLUME):
                        ch = NB_ALLUME - ch - 1
                        if P_DISPO_CH[i, CH_NUM[ch]] == 0:
                            ch += 1
                            while (P_BIOMASSE_CH[i, CH_NUM[ch]] != 0) and (ch < NB_CHAUDIERE_TOTAL-1):
                                ch += 1
                        P = P_DISPO_CH[i, CH_NUM[ch]] * P_BIOMASSE[i] / P_DISPO[i]
                        if P == 0:
                            CPT += 1
                        elif P < P_MIN[i, CH_NUM[ch]]:
                            NB_ALLUME -= 1
                            P_BIOMASSE_CH[i, :] = 0
                            P_DISPO[i] -= P_DISPO_CH[i, CH_NUM[ch]]
                            CPT = max(0,CPT-1)
                            break
                        elif P > P_DISPO_CH[i, CH_NUM[ch]]:
                            P_BIOMASSE_CH[i, CH_NUM[ch]] = P_DISPO_CH[i, CH_NUM[ch]]
                            CPT += 1
                        else:
                            P_BIOMASSE_CH[i, CH_NUM[ch]] = P
                            CPT += 1
        if debug : 
            print('Valeur : P_BIOMASSE_CH')
            print(P_BIOMASSE_CH)
        # /// Calcul du volume de bois n??cessaire par site ou silo ///
        if debug : print('--- Calcul du volume de bois n??cessaire par site ou silo ---')
        for silo in range(NB_SILO):
            # Initialisation
            df_tableauSortie['BESOIN_BIOMASSE_SILO'+str(silo+1)] = 0.0
            # Ajout des besoins par chaudi??re
            for ch in range(NB_CHAUDIERE_TOTAL):
                if SILO[ch]-1 == silo:
                    for i in range(NB_HEURES):
                        df_tableauSortie.loc[i,'BESOIN_BIOMASSE_SILO'+str(silo+1)] += P_BIOMASSE_CH[i, ch] / (RENDEMENT[i, ch]/100) / PCI[i, silo] / DENSITE[i, silo]
        
        # --------- Donn??es de sorties ---------
        previsionBesoinBiomasse = df_tableauSortie
        if debug : 
            print('Valeur : previsionBesoinBiomasse')
            print(previsionBesoinBiomasse)
        with open(str(self.authentification)+'_biomasse.pickle', 'wb') as BDD:
            if debug : print('--- Sauvegarde de la pr??vision demande de biomasse ---')
            pickle.dump(previsionBesoinBiomasse, BDD)
        if debug : print('---------- Fin calcul du fonctionnement des chaudi??res ----------')
        return previsionBesoinBiomasse


    def CalculPlanningAppro(self):
        """Fonction qui permet de calculer le planning d'approvisionnement
        
        Fonctionnement :
            - Appel de la fonction pour calculer le besoin de biomasse sur les 10 jours ?? venir
            - Calcul au pas de temps horaire des camions n??cessaires pour remplir l'objectif de remplissage du ou des silos
            - Aggr??gation des camions n??cessaires par demi-journ??e
            - Enregistrement des r??sultats dans des fichiers pickle
                * authentification_livraison --> df_tableauSortie_camions
                * authentification_stockAvecLivraison --> df_tableauSortie_volume
        
        Args:
            self : Ensemble des param??tres de la configuration notamment les param??tres des silos et les contraintes sur les livraisons
    
        Returns:
            df_tableauSortie_camions : Le planning d'approvisionnement de camions sur les 10 jours ?? venir par demi-journ??e
            df_tableauSortie_volume : L'??volution du volume de biomasse dans les silos sur les 10 jours ?? venir au pas de temps horaire
                    
        #TODO v??rifier le changement de mois    
        
        """
        
        if debug : 
            print('Valeur : authentification')
            print(self.authentification)

        if debug : print('---------- D??but calcul du planning d\'approvisionnement ----------')

        # --------- Donn??es d???entr??es ---------
        H_DEBUT_MATIN = 8
        H_FIN_MATIN = 13
        H_DEBUT_APRESMIDI = 14
        H_FIN_APRESMIDI = 19
        # Tableau du besoin de biomasse n??cessaire aux chaudi??res pour couvrir la demande du r??seau (pr??dite)
        df_tableauEntree = self.FonctionnementChaudiere()

        # Caract??ristiques de la chaufferie
        NB_SILO = self.nbSilo # Nombre de silo r??pondant ?? la m??me demande r??seau
        # Contraintes sur le planning (une ligne = un silo)
        NB_CAMIONS_MIN = self.nbCamionsMin # Nombre de livraisons minimum qu'il est possible de recevoir
        NB_CAMIONS_MAX = self.nbCamionsMax # Nombre de livraisons maximum qu'il est possible de recevoir
        VOLUME_CAMIONS = self.volumeCamion # Volume des camions livr??s
         # Contraintes sur le stockage de bois (une ligne = un silo)
        NIVEAU_MIN = self.niveauMinSilo # Seuil de remplissage minimum ?? respecter
        NIVEAU_MAX = self.niveauMaxSilo # Seuil de remplissage maximum ?? respecter
        # Volume de stockage
        VOLUME_STOCK = self.volumeMaxSilo
        # Niveau actuel du stock
        NIVEAU_ACTUEL_INITIAL = self.niveauSilo
        if debug : 
            print('Valeur : NB_SILO')
            print(NB_SILO)
            print('Valeur : NB_CAMIONS_MIN')
            print(NB_CAMIONS_MIN[0])
            print('Dimensions : NB_CAMIONS_MIN --> ' + str(len(NB_CAMIONS_MIN)))
            print('Valeur : NB_CAMIONS_MAX')
            print(NB_CAMIONS_MAX[0])
            print('Dimensions : NB_CAMIONS_MAX --> ' + str(len(NB_CAMIONS_MAX)))
            print('Valeur : VOLUME_CAMIONS')
            print(VOLUME_CAMIONS[0])
            print('Dimensions : VOLUME_CAMIONS --> ' + str(len(VOLUME_CAMIONS)))
            print('Valeur : NIVEAU_MIN')
            print(NIVEAU_MIN[0])
            print('Dimensions : NIVEAU_MIN --> ' + str(len(NIVEAU_MIN)))
            print('Valeur : NIVEAU_MAX')
            print(NIVEAU_MAX[0])
            print('Dimensions : NIVEAU_MAX --> ' + str(len(NIVEAU_MAX)))
            print('Valeur : VOLUME_STOCK')
            print(VOLUME_STOCK[0])
            print('Dimensions : VOLUME_STOCK --> ' + str(len(VOLUME_STOCK)))
            print('Valeur : NIVEAU_ACTUEL_INITIAL')
            print(NIVEAU_ACTUEL_INITIAL)
                                        
        
        # --------- D??finition de la plage d?????tude ---------
        DATE_DEBUT = df_tableauEntree['DATE'][0]
        DATE_FIN = df_tableauEntree['DATE'][len(df_tableauEntree)-1]
        NB_HEURES = math.floor((DATE_FIN-DATE_DEBUT).total_seconds() / 3600) + 1
        NB_JOURS = math.floor(NB_HEURES/24)

        # --------- Param??tres interm??diaires ---------
        # Compl??ment du tableau de donn??es d'entr??es (pas de temps horaire)
        df_tableauEntree['JOUR'] = -9999
        jour = 0
        df_tableauEntree.loc[0,'JOUR'] = jour
        for h in range(1,NB_HEURES):
            if df_tableauEntree.loc[h,'DATE'].day != df_tableauEntree.loc[h-1,'DATE'].day:
                jour +=1
            df_tableauEntree.loc[h,'JOUR'] = jour
        df_tableauEntree['HEURE'] = -9999
        for h in range(NB_HEURES):
            df_tableauEntree.loc[h,'HEURE'] = df_tableauEntree.loc[h,'DATE'].hour
        for silo in range(NB_SILO):
            # Sur les contraintes de livraison
            df_tableauEntree['NB_CAMIONS_MIN'+str(silo+1)] = np.nan # Nombre de livraisons minimum qu???il faut encore recevoir jusqu????? la fin de la demi-journ??e
            df_tableauEntree['NB_CAMIONS_MAX'+str(silo+1)] = np.nan # Nombre de livraisons maximum qu???il est encore possible de recevoir sur la demi-journ??e
            df_tableauEntree['VOLUME_CAMION'+str(silo+1)] = np.nan # Quantit?? maximale de bois qui peut encore ??tre livr??e sur la demi-journ??e
            #df_tableauEntree['RESPECT_NB_CAMIONS_MIN'+str(silo+1)] = np.nan # Bool??en qui indique si le nombre de livraison minimum est respect??
            #df_tableauEntree['RESPECT_NB_CAMIONS_MAX'+str(silo+1)] = np.nan # Bool??en qui indique si le nombre de livraison maximum est respect??
            # Sur les contraintes sur le stockage de bois
            df_tableauEntree['NIVEAU_MIN'+str(silo+1)] = np.nan # Seuil limite basse de remplissage du stockage
            df_tableauEntree['VOLUME_MIN'+str(silo+1)] = np.nan # Volume minimum de remplissage du stockage
            df_tableauEntree['NIVEAU_MAX'+str(silo+1)] = np.nan # Seuil limite haute de remplissage du stockage
            df_tableauEntree['VOLUME_MAX'+str(silo+1)] = np.nan # Volume maximum de remplissage du stockage
            df_tableauEntree['NIVEAU_ACTUEL'+str(silo+1)] = np.nan # Niveau du stock
            df_tableauEntree['VOLUME_ACTUEL'+str(silo+1)] = np.nan # Volume du stock
            # Sur les livraisons
            df_tableauEntree['NB_CAMIONS'+str(silo+1)] = np.nan # Nombre de camions n??cessaires

        # --------- Donn??es de sorties ---------
        # Initialisation du tableau de sorties contenant le planning de commande des camions
        columns_tableauSortie_camions = ['DATE']
        for silo in range(NB_SILO):
            columns_tableauSortie_camions += ['NB_CAMIONS_1_SILO'+str(silo+1)]
            #columns_tableauSortie_camions += ['RESPECT_NB_CAMIONS_1_SILO'+str(silo+1)]
            columns_tableauSortie_camions += ['NB_CAMIONS_2_SILO'+str(silo+1)]
            #columns_tableauSortie_camions += ['RESPECT_NB_CAMIONS_2_SILO'+str(silo+1)]
        index_tableauSortie_camions = range(NB_JOURS)
        df_tableauSortie_camions = pd.DataFrame(index=index_tableauSortie_camions, columns=columns_tableauSortie_camions)
        # Initialisation du tableau de sorties contenant l'??volution du volume de biomasse dans le silo
        columns_tableauSortie_volume = ['DATE']
        for silo in range(NB_SILO):
            columns_tableauSortie_volume += ['VOLUME_ACTUEL'+str(silo+1)]
            columns_tableauSortie_volume += ['VOLUME_MAX'+str(silo+1)]
            columns_tableauSortie_volume += ['VOLUME_MIN'+str(silo+1)]
        index_tableauSortie_volume = range(NB_JOURS)
        df_tableauSortie_volume = pd.DataFrame(index=index_tableauSortie_volume, columns=columns_tableauSortie_volume)
        # Remplissage de la colonne DATE des deux tableaux de sorties
        for j in range(NB_JOURS):
            df_tableauSortie_camions.loc[j,'DATE'] = (DATE_DEBUT + timedelta(j)).strftime('%Y-%m-%d')
        for j in range(NB_HEURES):
            df_tableauSortie_volume.loc[j,'DATE'] = df_tableauEntree.loc[j,'DATE']

        # --------- CALCUL ---------

        # /// Calcul heure par heure du nombre de camions n??cessaire par site ou silo ///
        if debug : print('--- Calcul heure par heure du nombre de camions n??cessaire par site ou silo ---')

        for silo in range(NB_SILO):
            
            if debug : print('- Calcul pour le silo ' + str(silo+1) + '/' + str(NB_SILO))
            
            # == Initialisation des lignes dans le tableau de donn??es d???entr??es ==
            for j in range(NB_JOURS+1):
                for h in range(NB_HEURES):
                    if df_tableauEntree['JOUR'][h] == j:
                        if (df_tableauEntree['HEURE'][h]>=H_DEBUT_MATIN and df_tableauEntree['HEURE'][h]<H_FIN_MATIN):
                            df_tableauEntree.loc[h,'NB_CAMIONS_MIN'+str(silo+1)] = NB_CAMIONS_MIN[j][silo]
                            df_tableauEntree.loc[h,'NB_CAMIONS_MAX'+str(silo+1)] = NB_CAMIONS_MAX[j][silo]
                        elif (df_tableauEntree['HEURE'][h]>=H_DEBUT_APRESMIDI and df_tableauEntree['HEURE'][h]<H_FIN_APRESMIDI):
                            df_tableauEntree.loc[h,'NB_CAMIONS_MIN'+str(silo+1)] = NB_CAMIONS_MIN[j][silo]
                            df_tableauEntree.loc[h,'NB_CAMIONS_MAX'+str(silo+1)] = NB_CAMIONS_MAX[j][silo]
                        else:
                            df_tableauEntree.loc[h,'NB_CAMIONS_MIN'+str(silo+1)] = 0
                            df_tableauEntree.loc[h,'NB_CAMIONS_MAX'+str(silo+1)] = 0
                        df_tableauEntree.loc[h,'VOLUME_CAMION'+str(silo+1)] = VOLUME_CAMIONS[j][silo]
                        df_tableauEntree.loc[h,'NIVEAU_MIN'+str(silo+1)] = NIVEAU_MIN[j][silo]
                        df_tableauEntree.loc[h,'VOLUME_MIN'+str(silo+1)] = NIVEAU_MIN[j][silo]/100 * VOLUME_STOCK[j][silo]
                        df_tableauEntree.loc[h,'NIVEAU_MAX'+str(silo+1)] = NIVEAU_MAX[silo]
                        df_tableauEntree.loc[h,'VOLUME_MAX'+str(silo+1)] = NIVEAU_MAX[silo]/100 * VOLUME_STOCK[j][silo]   

            # == Initialisation de la toute premi??re ligne dans le tableau de donn??es d???entr??es ==
            df_tableauEntree.loc[0,'NIVEAU_ACTUEL'+str(silo+1)] = NIVEAU_ACTUEL_INITIAL[silo]
            df_tableauEntree.loc[0,'VOLUME_ACTUEL'+str(silo+1)] = NIVEAU_ACTUEL_INITIAL[silo]/100 * VOLUME_STOCK[j][silo]

            # == Calcul horaire ==
            for h in range(NB_HEURES):

                # Test si on a les donn??es sur la ligne d'??tude
                CPT = 0
                if np.isnan(df_tableauEntree['NIVEAU_MAX'+str(silo+1)][h]):
                    CPT += 1
                if np.isnan(df_tableauEntree['NIVEAU_MIN'+str(silo+1)][h]):
                    CPT += 1
                if np.isnan(df_tableauEntree['NIVEAU_ACTUEL'+str(silo+1)][h]):
                    CPT += 1

                # Nombre de camions
                if CPT == 0:
  
                    # Si l'utilisateur renseigne un m??me nombre de camions min et max, cela signifie que la commande est d??j?? pass??e donc c'est cette valeur la contrainte principale
                    if df_tableauEntree['NB_CAMIONS_MIN'+str(silo+1)][h] == df_tableauEntree['NB_CAMIONS_MAX'+str(silo+1)][h]:
                        df_tableauEntree.loc[h,'NB_CAMIONS'+str(silo+1)] = df_tableauEntree['NB_CAMIONS_MIN'+str(silo+1)][h]
                    # Sinon
                    else :
                        NB = 0
                        # On calcule le nombre de camions n??cessaires pour atteindre le niveau max dans le stock
                        if df_tableauEntree['NIVEAU_ACTUEL'+str(silo+1)][h] < df_tableauEntree['NIVEAU_MAX'+str(silo+1)][h]:
                            NB = math.floor((df_tableauEntree['VOLUME_MAX'+str(silo+1)][h] - df_tableauEntree['VOLUME_ACTUEL'+str(silo+1)][h])/df_tableauEntree['VOLUME_CAMION'+str(silo+1)][h])
                        # Si le nombre de camions calcul?? est sup??rieur au nombre de camion maximum, on limite la commande
                        NB = min(NB, df_tableauEntree['NB_CAMIONS_MAX'+str(silo+1)][h])
                        # On calcule le niveau que l'on atteindra avec cette quantit?? de camions command??s
                        NIV = df_tableauEntree['VOLUME_ACTUEL'+str(silo+1)][h] - df_tableauEntree['BESOIN_BIOMASSE_SILO'+str(silo+1)][h] + df_tableauEntree['NB_CAMIONS'+str(silo+1)][h] * df_tableauEntree['VOLUME_CAMION'+str(silo+1)][h]
                        # Si le niveau calcul?? ne respecte pas le niveau minimal autoris??, on commande plus de camions pour assurer cette limite minimum
                        if NIV < df_tableauEntree['NIVEAU_MIN'+str(silo+1)][h]:
                            NB = math.floor((df_tableauEntree['VOLUME_MIN'+str(silo+1)][h] - df_tableauEntree['VOLUME_ACTUEL'+str(silo+1)][h])/df_tableauEntree['VOLUME_CAMION'+str(silo+1)][h])
                        # On attribue la valeur calcul??e
                        df_tableauEntree.loc[h,'NB_CAMIONS'+str(silo+1)] = NB
                        
                    # Si le nombre de camions ?? commander est inf??rieur ?? la limite minimum
                    #if df_tableauEntree['NB_CAMIONS'+str(silo+1)][h] < df_tableauEntree['NB_CAMIONS_MIN'+str(silo+1)][h]:
                    #    df_tableauEntree.loc[h,'RESPECT_NB_CAMIONS_MIN'+str(silo+1)] = False
                    #else:
                    #    df_tableauEntree.loc[h,'RESPECT_NB_CAMIONS_MIN'+str(silo+1)] = True                        
                    
                    # Si le nombre de camions ?? commander est sup??rieur ?? la limite maximum
                    #if df_tableauEntree['NB_CAMIONS'+str(silo+1)][h] > df_tableauEntree['NB_CAMIONS_MAX'+str(silo+1)][h]:
                    #    df_tableauEntree.loc[h,'RESPECT_NB_CAMIONS_MAX'+str(silo+1)] = False
                    #else:
                    #    df_tableauEntree.loc[h,'RESPECT_NB_CAMIONS_MAX'+str(silo+1)] = True   
                    
                # Calcul des contraintes sur le pas de temps suivant
                if h != NB_HEURES-1:
                    # Actualisation du nombre de camion minimum
                    if df_tableauEntree['HEURE'][h] >= H_DEBUT_MATIN and df_tableauEntree['HEURE'][h] < H_FIN_MATIN:
                        df_tableauEntree.loc[h+1,'NB_CAMIONS_MIN'+str(silo+1)] = max(0, df_tableauEntree['NB_CAMIONS_MIN'+str(silo+1)][h+1] - df_tableauEntree['NB_CAMIONS'+str(silo+1)][h])
                    elif df_tableauEntree['HEURE'][h] >= H_DEBUT_APRESMIDI and df_tableauEntree['HEURE'][h] < H_FIN_APRESMIDI:
                        df_tableauEntree.loc[h+1,'NB_CAMIONS_MIN'+str(silo+1)] = max(0, df_tableauEntree['NB_CAMIONS_MIN'+str(silo+1)][h+1] - df_tableauEntree['NB_CAMIONS'+str(silo+1)][h])
                    # Actualisation du nombre de camion maximum
                    if df_tableauEntree['HEURE'][h] >= H_DEBUT_MATIN and df_tableauEntree['HEURE'][h] < H_FIN_MATIN:
                        df_tableauEntree.loc[h+1,'NB_CAMIONS_MAX'+str(silo+1)] = max(0, df_tableauEntree['NB_CAMIONS_MAX'+str(silo+1)][h+1] - df_tableauEntree['NB_CAMIONS'+str(silo+1)][h])
                    elif df_tableauEntree['HEURE'][h] >= H_DEBUT_APRESMIDI and df_tableauEntree['HEURE'][h] < H_FIN_APRESMIDI:
                        df_tableauEntree.loc[h+1,'NB_CAMIONS_MAX'+str(silo+1)] = max(0, df_tableauEntree['NB_CAMIONS_MAX'+str(silo+1)][h+1] - df_tableauEntree['NB_CAMIONS'+str(silo+1)][h])
                    # Actualisation du niveau et du volume dans le stock
                    df_tableauEntree.loc[h+1,'VOLUME_ACTUEL'+str(silo+1)] = max(0, df_tableauEntree['VOLUME_ACTUEL'+str(silo+1)][h] - df_tableauEntree['BESOIN_BIOMASSE_SILO'+str(silo+1)][h] + df_tableauEntree['NB_CAMIONS'+str(silo+1)][h] * df_tableauEntree['VOLUME_CAMION'+str(silo+1)][h])
                    df_tableauEntree.loc[h+1,'NIVEAU_ACTUEL'+str(silo+1)] = 100 * df_tableauEntree.loc[h+1,'VOLUME_ACTUEL'+str(silo+1)] / VOLUME_STOCK[silo]
                    
        # --------- Donn??es de sorties ---------
        # /// Calcul du nombre total de camions n??cessaire par site ou silo ///
        if debug : print('--- Calcul du nombre total de camions n??cessaire par site ou silo ---')
        for silo in range(NB_SILO):
            for j in range(NB_JOURS):
                df_tableauSortie_camions.loc[j,'NB_CAMIONS_1_SILO'+str(silo+1)] = 0
                #df_tableauSortie_camions.loc[j,'RESPECT_NB_CAMIONS_1_SILO'+str(silo+1)] = 0
                df_tableauSortie_camions.loc[j,'NB_CAMIONS_2_SILO'+str(silo+1)] = 0
                #df_tableauSortie_camions.loc[j,'RESPECT_NB_CAMIONS_2_SILO'+str(silo+1)] = 0
                for h in range(NB_HEURES):
                    if df_tableauEntree['JOUR'][h] == j:
                        if df_tableauEntree['HEURE'][h] >= H_DEBUT_MATIN and df_tableauEntree['HEURE'][h] < H_FIN_MATIN:
                            # Cumul du nombre de camions ?? commander sur la matin??e
                            df_tableauSortie_camions.loc[j,'NB_CAMIONS_1_SILO'+str(silo+1)] += df_tableauEntree['NB_CAMIONS'+str(silo+1)][h]
                            # Messages d'alerte
                            #if not df_tableauEntree.loc[h,'RESPECT_NB_CAMIONS_MIN'+str(silo+1)]:
                            #    df_tableauSortie_camions.loc[j,'RESPECT_NB_CAMIONS_1_SILO'+str(silo+1)] = -1
                            #elif not df_tableauEntree.loc[h,'RESPECT_NB_CAMIONS_MAX'+str(silo+1)]:
                            #    df_tableauSortie_camions.loc[j,'RESPECT_NB_CAMIONS_1_SILO'+str(silo+1)] = 1
                        elif df_tableauEntree['HEURE'][h] >= H_DEBUT_APRESMIDI and df_tableauEntree['HEURE'][h] <= H_FIN_APRESMIDI:
                            # Cumul du nombre de camions ?? commander sur l'apr??s-midi
                            df_tableauSortie_camions.loc[j,'NB_CAMIONS_2_SILO'+str(silo+1)] += df_tableauEntree['NB_CAMIONS'+str(silo+1)][h]
                            # Messages d'alerte
                            #if not df_tableauEntree.loc[h,'RESPECT_NB_CAMIONS_MIN'+str(silo+1)]:
                            #    df_tableauSortie_camions.loc[j,'RESPECT_NB_CAMIONS_2_SILO'+str(silo+1)] = -1
                            #elif not df_tableauEntree.loc[h,'RESPECT_NB_CAMIONS_MAX'+str(silo+1)]:
                            #    df_tableauSortie_camions.loc[j,'RESPECT_NB_CAMIONS_2_SILO'+str(silo+1)] = 1
        with open(str(self.authentification)+'_livraison.pickle', 'wb') as BDD:
            if debug : print('--- Sauvegarde du planning de livraison ---')
            pickle.dump(df_tableauSortie_camions, BDD)                    
        # /// Calcul de l'??volution du stock de bois dans le silo ///
        if debug : print('--- Calcul de l\'??volution du stock de bois dans les silos ---')
        for silo in range(NB_SILO):
            df_tableauSortie_volume['VOLUME_ACTUEL'+str(silo+1)] = df_tableauEntree['VOLUME_ACTUEL'+str(silo+1)]
            df_tableauSortie_volume['VOLUME_MAX'+str(silo+1)] = df_tableauEntree['VOLUME_MAX'+str(silo+1)]
            df_tableauSortie_volume['VOLUME_MIN'+str(silo+1)] = df_tableauEntree['VOLUME_MIN'+str(silo+1)]
        with open(str(self.authentification)+'_stockAveclivraison.pickle', 'wb') as BDD:
            if debug : print('--- Sauvegarde de la pr??vision de l\'??volution stock de biomasse ---')
            pickle.dump(df_tableauSortie_volume, BDD)
            
        if debug : print('---------- Fin calcul du planning d\'approvisionnement ----------')
   
    
    