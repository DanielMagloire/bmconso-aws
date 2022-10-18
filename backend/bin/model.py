class Actualiser(object):
    
    # --------- Paramètres globaux ---------
    global d, A0, heures, response_json, NB_HEURES

    def __init__(self, localisationVille, nbSilo, numInstall, nomCapteur, uniteCapteur, \
                 pciBois, densiteBois, volumeMaxSilo, niveauMaxSilo,\
                 niveauMinSilo, niveauSilo, nbChaudiere, nbChaudiereTotal, \
                 siloChaudiere, pNomChaudiere, rendementChaudiere, pMinChaudiere, chargeChaudiere,\
                 isCoge, pCoge, typePilotage, prioriteChaudiere, nbCamionsMin, nbCamionsMax, \
                 volumeCamion, authentification, dateMaintenant):

        self.localisationVille = localisationVille # Localisation géographique du site
        self.nbSilo = nbSilo # Nombre de chaufferie = nombre de silo
        self.numInstall = numInstall # Numéro d'installation
        self.nomCapteur = nomCapteur # Nom du capteur
        self.uniteCapteur = uniteCapteur # Unité du capteur
        self.pciBois = pciBois # PCI du bois
        self.densiteBois = densiteBois # Densité du bois
        self.volumeMaxSilo = volumeMaxSilo # Volume maximal du silo
        self.niveauMaxSilo = niveauMaxSilo # Seuil limite haute du silo
        self.niveauMinSilo = niveauMinSilo # Seuil limite basse du silo
        self.niveauSilo = niveauSilo # Niveau actuel du silo
        self.nbChaudiere = nbChaudiere # Nombre de chaudières associées au silo
        self.nbChaudiereTotal = nbChaudiereTotal # Nombre de chaudière total
        self.siloChaudiere = siloChaudiere # Silo lié à la chaudière
        self.pNomChaudiere = pNomChaudiere # Puissance nominale de la chaudière
        self.rendementChaudiere = rendementChaudiere # Rendement de la chaudière
        self.pMinChaudiere = pMinChaudiere # Puissance minimale de la chaudière
        self.chargeChaudiere = chargeChaudiere # Charge de la chaudière
        self.isCoge = isCoge # Présence d'une cogénération
        self.pCoge = pCoge # Puissance de la cogénération
        self.typePilotage = typePilotage # Type de pilotage
        self.prioriteChaudiere = prioriteChaudiere # Priorité des chaudières
        self.nbCamionsMin = nbCamionsMin # Nombre de livraisons possibles sur une demi-journée, minimal
        self.nbCamionsMax = nbCamionsMax # Nombre de livraisons possibles sur une demi-journée, maximal
        self.volumeCamion = volumeCamion # Volume moyen de biomasse livrée par camion
        self.authentification = authentification
        self.dateMaintenant = dateMaintenant
        pass

    def to_minutes(self, time):
        return (time.days*24*3600 + time.seconds)/60

    def DonneesCofelyVision(self):
        print('---------- Début récupération des données Cofely Vision ----------') # pour les tests
        
        # --------- Données d’entrées --------
        # Tableau de capteurs
        columns_tableauCapteur = ['NUM_INSTALL', 'NOM_CAPTEUR', 'UNITE_CAPTEUR', 'NUM_CAPTEUR', 'F_CORR']
        # Création du tableau vide
        df_tableauCapteur = pd.DataFrame(columns=columns_tableauCapteur)
        # Ajout des données
        for i in range(len(self.nomCapteur)):
            data_tableauCapteur = np.array([self.numInstall[i], self.nomCapteur[i], self.uniteCapteur[i], '', ''])
            df_tableauCapteur.loc[len(df_tableauCapteur)] = data_tableauCapteur
        # Dates
        DERNIERE_DATE = self.dateDernieresDonnees # on récupère la date des dernières données téléchargées
        DATE_MAINTENANT = self.dateMaintenant # on récupère la date actuelle (au moment du lancement de l'API IA)
       
        # --------- Paramètres communs à toutes les requêtes HTTP ---------
        headers = {'Content-Type': 'text/json', 'x-subject-username': 'VZ5325', 'x-api-key': 'l7xx2c0a9eb112524bec9fa8ef3976750860', 'x-api-secret': 'c91fb9dd1f84487088fc34c51bd4bd27'}

        # --------- Définition de la plage d’étude ---------
        # Début de la plage d'étude 
        if DERNIERE_DATE != None:
            if (DERNIERE_DATE-DATE_MAINTENANT).days <= 365:
                DATE_DEBUT = DERNIERE_DATE.replace(hour=DERNIERE_DATE.hour + 1)
                DATE_DEBUT = DATE_DEBUT.replace(minute=0, second=0, microsecond=0)
            else:
                DATE_DEBUT = DATE_MAINTENANT.replace(year=DATE_MAINTENANT.year - 1)
                DATE_DEBUT = DATE_DEBUT.replace(minute=0, second=0, microsecond=0)
        else:
            DATE_DEBUT = DATE_MAINTENANT.replace(year=DATE_MAINTENANT.year - 1)
            DATE_DEBUT = DATE_DEBUT.replace(minute=0, second=0, microsecond=0)
        # Fin de la plage d'étude
        DATE_FIN = DATE_MAINTENANT
        DATE_FIN = DATE_FIN.replace(minute=0, second=0, microsecond=0)
        # Eléments de comptage
        NB_MINUTES = math.floor((DATE_FIN-DATE_DEBUT).total_seconds() / 60)
        NB_HEURES = math.floor(NB_MINUTES / 60)
        NB_JOURS = math.floor(NB_HEURES / 24)
        
        # --------- Données de sorties ---------
        # Initialisation du tableau de sortie
        columns_tableauSortie = ['DATE', 'DEMANDE_RESEAU']
        index_tableauSortie = range(NB_HEURES)
        df_tableauSortie = pd.DataFrame(index=index_tableauSortie, columns=columns_tableauSortie)
        # Remplissage de la colonne DATE
        for heures in range(NB_HEURES):
            df_tableauSortie['DATE'][heures] = DATE_DEBUT + timedelta(hours=heures)
            df_tableauSortie['DEMANDE_RESEAU'][heures] = 0
            
        # --------- CALCUL ---------

        # A – Définition et initialisation des paramètres intermédiaires
        print('--- Définition et initialisation des paramètres intermédiaires ---') # pour les tests
        # 1 - Complément du tableau de capteurs
        for i in range(len(df_tableauCapteur.index)):
            # /// Récupération du numéro du capteur ///
            # == Récupération de l'identifiant de l'installation ==
            # Ecriture de la requête HTTP
            strURL = 'http://es2.gses.gdfsuez.net:8080/m2m/api/v3/properties?$filter=code%20eq%20%27' + df_tableauCapteur['NUM_INSTALL'][i] + '%27'
            # Envoi de la requête HTTP
            response = requests.get(strURL, headers=headers)
            # Exploitation de la réponse à la requête pour récupérer le code de l'installation
            if response.status_code == 200:
                response_json = response.json()
                for valeur in response_json.values():
                    id_install = valeur[0]['property_id']
            else:
                id_install = np.nan
            # == Récupération de la liste des capteurs disponibles (85 premiers) ==
            # Ecriture de la requête HTTP
            strURL = 'http://es2.gses.gdfsuez.net:8080/m2m/api/v3/properties/' + str(id_install) + '/controllers/0/measures_points'
            # Envoi de la requête HTTP
            response = requests.get(strURL, headers=headers)
            # Exploitation de la réponse à la requête pour récupérer le numéro du capteur
            if response.status_code == 200:
                response_json = response.json()
                for valeur in response_json.values():
                    for capteur in valeur:
                        if capteur['name'] == df_tableauCapteur['NOM_CAPTEUR'][i]:
                            df_tableauCapteur['NUM_CAPTEUR'][i] = capteur['point_id']
            else:
                df_tableauCapteur['NUM_CAPTEUR'][i] = np.nan
            # == Récupération de la liste des capteurs disponibles (85 suivants) ==
            # Ecriture de la requête HTTP
            strURL = 'http://es2.gses.gdfsuez.net:8080/m2m/api/v3/properties/' + str(id_install) + '/controllers/0/measures_points?%24skip=85'
            # Envoi de la requête HTTP
            response = requests.get(strURL, headers=headers)
            # Exploitation de la réponse à la requête pour récupérer le numéro du capteur
            if response.status_code == 200:
                response_json = response.json()
                for valeur in response_json.values():
                    for capteur in valeur:
                        if capteur['name'] == df_tableauCapteur['NOM_CAPTEUR'][i]:
                            df_tableauCapteur['NUM_CAPTEUR'][i] = capteur['point_id']
            else:
                df_tableauCapteur['NUM_CAPTEUR'][i] = np.nan
                
            # /// Récupération du facteur correctif ///
            if df_tableauCapteur['UNITE_CAPTEUR'][i] == 'W' or df_tableauCapteur['UNITE_CAPTEUR'][i] == 'Wh':
                df_tableauCapteur['F_CORR'][i] = 0.001
            elif df_tableauCapteur['UNITE_CAPTEUR'][i] == 'kW' or df_tableauCapteur['UNITE_CAPTEUR'][i] == 'kWh':
                df_tableauCapteur['F_CORR'][i] = 1
            elif df_tableauCapteur['UNITE_CAPTEUR'][i] == 'MW' or df_tableauCapteur['UNITE_CAPTEUR'][i] == 'MWh':
                df_tableauCapteur['F_CORR'][i] = 1000
            else:
                df_tableauCapteur['F_CORR'][i] = 1000000
                
        print(df_tableauCapteur) # pour les tests

        # B – Traitement pour chaque capteur
        for i in range(len(df_tableauCapteur.index)):
            
            print('--- Traitement pour le capteur ' + str(i+1) + '/' + str(len(df_tableauCapteur.index)) + ' ---') # pour les tests

            # /// Récupération des données du capteur ///
            print('- Récupération des données du capteur') # pour les tests
            # == Remplissage du tableau de données des capteurs pour tous les pas de temps ==
            # Initialisation des tableaux de données des capteurs
            columns_tableauDonneesCapteur = ['DATE_CAPTEUR', 'VALEUR_CAPTEUR']
            index_tableauDonneesCapteur = range(NB_MINUTES)
            df_tableauDonneesCapteur = pd.DataFrame(columns=columns_tableauDonneesCapteur, index=index_tableauDonneesCapteur)
            df_tableauDonneesCapteur['DATE_CAPTEUR'] = DATE_DEBUT + pd.to_timedelta(df_tableauDonneesCapteur.index, unit='m')
            # Envoi de x requêtes HTTP pour récupérer les données par paquets de 30 jours
            x = math.ceil(NB_JOURS/30)
            for k in range(0, x):
                START_DATE = DATE_DEBUT + timedelta(days=30*k)
                END_DATE = START_DATE + timedelta(days=30)
                START_DATE = START_DATE.strftime("%Y-%m-%dT%H%%3A%M%%3A%S") # pour la requête HTTP
                END_DATE = END_DATE.strftime("%Y-%m-%dT%H%%3A%M%%3A%S") # pour la requête HTTP
                # Ecriture de la requête HTTP
                strURL = 'http://es2.gses.gdfsuez.net:8080/m2m/api/v3/properties/0/controllers/0/measures_points/' + str(df_tableauCapteur['NUM_CAPTEUR'][i]) + '/historicals?start_date=' + START_DATE + '&end_date=' + END_DATE
                # Envoi de la requête HTTP
                response = requests.get(strURL, headers=headers)
                # Si la requête a réussi, récupération des valeurs
                if response.status_code == 200:
                    # -- Remplissage du tableau de données des capteurs pour les valeurs --
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
                    print('erreur BM104 - API Cofely Vision indisponible, réessayer plus tard. Si l\'erreur se reproduit, contacter Cylergie.')
                    
                    
            # /// Retraitement des valeurs ///
            print('- Retraitement des valeurs') # pour les tests
            # == Moyennage temporel ==
            periode = '1H'
            try:
                if df_tableauCapteur['UNITE_CAPTEUR'][i] in ('2', '4', '6', '8'):
                    d = df_tableauDonneesCapteur
                    # Conversion de la mesure en float pour pouvoir calculer la moyenne
                    d = d.astype({'VALEUR_CAPTEUR':'float'}) 
                    # Correction des valeurs aberrantes avec compteur d'énergie non continu
                    d = d.sort_values(by=['DATE_CAPTEUR'])
                    d = d.dropna()
                    while not d[d['VALEUR_CAPTEUR'] < d['VALEUR_CAPTEUR'].shift(+1)].empty:
                        d.drop(d[d['VALEUR_CAPTEUR'] < d['VALEUR_CAPTEUR'].shift(+1)].index, inplace=True)
                    # Moyenne au pas de temps horaire                
                    d.index = d['DATE_CAPTEUR']
                    A0 = d.resample(periode).fillna("pad")
                    A0['DATE_CAPTEUR'] = A0.index
                    # Pré-traitement
                    # Passage d'énergie à puissance
                    A0['TpsDiff'] = A0['DATE_CAPTEUR'].diff() # Création d'une colonne représentant l'intervalle de temps entre deux lignes
                    A0['TpsDiff'] = A0['TpsDiff'].dt.total_seconds().div(3600, fill_value=0) # Conversion de cette colonne en heure (en passant par les secondes)
                    A0['VALEUR_CAPTEUR_ENERGIE'] = A0['VALEUR_CAPTEUR'] # Sauvergarde de la donnée brute
                    A0['VALEUR_CAPTEUR'] = A0['VALEUR_CAPTEUR_ENERGIE'].diff().div(A0['TpsDiff'], axis=0) # Céation d'une matrice des puissances à partir des données d'énergie et des intervalles de temps entre deux lignes
                    A0.drop(A0.tail(1).index, inplace=True)
                else:
                    d = df_tableauDonneesCapteur
                    # Conversion de la mesure en float pour pouvoir calculer la moyenne
                    d = d.astype({'VALEUR_CAPTEUR':'float'})
                    # Correction des valeurs aberrantes avec compteur d'énergie non continu
                    d = d.sort_values(by=['DATE_CAPTEUR'])
                    d.drop(d[d['VALEUR_CAPTEUR'] < d['VALEUR_CAPTEUR'][0]].index, inplace=True)
                    d = d.dropna()
                    # Moyenne au pas de temps horaire
                    A0 = d.resample(periode, on='DATE_CAPTEUR', closed='right', label='right').mean()
                # == Suppression des points trop éloignés de la moyenne ou négatifs ==
                A0[A0['VALEUR_CAPTEUR'] > 4*A0[A0['VALEUR_CAPTEUR'] != 0]['VALEUR_CAPTEUR'].mean()] = np.nan
                A0[A0['VALEUR_CAPTEUR'] < 0] = np.nan
            except:
                A0 = df_tableauDonneesCapteur
            
            # /// Application du facteur correctif ///
            print('- Application du facteur correctif') # pour les tests
            A0['VALEUR_CAPTEUR'] = A0['VALEUR_CAPTEUR'] * df_tableauCapteur['F_CORR'][i]

            # /// Remplissage de la colonne DEMANDE_RESEAU ///
            print('- Remplissage de la colonne DEMANDE_RESEAU') # pour les tests
            i0 = 0
            for heures in range(NB_HEURES):
                for i in range(i0,len(A0.index),1):
                    if A0.index[i] == df_tableauSortie['DATE'][heures]:
                        df_tableauSortie['DEMANDE_RESEAU'][heures] += A0['VALEUR_CAPTEUR'][i]
                        i0 = i
                        break
                
        # --------- Données de sorties ---------
        historiqueDemande = df_tableauSortie
        print('---------- Fin récupération des données Cofely Vision ----------') # pour les tests
        return historiqueDemande

    def DonneesMeteo(self):
        print('---------- Début récupération des données météo ----------') # pour les tests
        
        # --------- Données d’entrées ---------
        # Tableau de capteurs 
        VILLE = self.localisationVille
        # Dates
        DERNIERE_DATE = self.dateDernieresDonnees # on récupère la date des dernières données téléchargées
        DATE_MAINTENANT = self.dateMaintenant # on récupère la date actuelle (au moment du lancement de l'API IA)
        
        # --------- Paramètres intermédiaires ---------
        # 1 - Récupération des identifiants de la station météo
        df = pd.read_csv("BDD_MeteoCiel.csv", sep=";")
        for i in range(len(df)):
            if df['Station'][i] == VILLE:
                ID_HISTO = str(int(df['ID_HISTO'][i]))
                ID_PREV = str(int(df['ID_PREV'][i]))
                NOM = df['NOM'][i]
        # 2 - Définition de la plage d’étude
        # Début de la plage d'étude 
        if DERNIERE_DATE != None:
            if (DERNIERE_DATE-DATE_MAINTENANT).days <= 365:
                DATE_DEBUT = DERNIERE_DATE.replace(hour=DERNIERE_DATE.hour + 1)
                DATE_DEBUT = DATE_DEBUT.replace(minute=0, second=0, microsecond=0)
            else:
                DATE_DEBUT = DATE_MAINTENANT.replace(year=DATE_MAINTENANT.year - 1)
                DATE_DEBUT = DATE_DEBUT.replace(minute=0, second=0, microsecond=0)
        else:
            DATE_DEBUT = DATE_MAINTENANT.replace(year=DATE_MAINTENANT.year - 1)
            DATE_DEBUT = DATE_DEBUT.replace(minute=0, second=0, microsecond=0)
        # Fin de la plage d'étude
        DATE_FIN = DATE_MAINTENANT
        DATE_FIN = DATE_FIN.replace(minute=0, second=0, microsecond=0)
        # Elements de comptage
        NB_HEURES_Reel = math.floor((DATE_FIN-DATE_DEBUT).total_seconds() / 3600) # Nombre d'heures dont il faut les données d'historique
        NB_JOURS = math.floor(NB_HEURES_Reel / 24)
        NB_HEURES_Predit = 11 * 24 # Nombre d'heures dont il faut les données de prédiction
        
        # --------- Données de sorties ---------
        # Initialisation du tableau de sortie des données réelles
        columns_tableauSortie_Reel = ['DATE', 'T_EXT', 'HR']
        index_tableauSortie_Reel = range(NB_HEURES_Reel)
        df_tableauSortie_Reel = pd.DataFrame(index=index_tableauSortie_Reel, columns=columns_tableauSortie_Reel)
        for heures in range(NB_HEURES_Reel):
            df_tableauSortie_Reel['DATE'][heures] = DATE_DEBUT + timedelta(hours=heures)
        # Initialisation du tableau de sortie des données de prévisions
        columns_tableauSortie_Predit = ['DATE', 'T_EXT', 'HR']
        index_tableauSortie_Predit = range(NB_HEURES_Predit)
        df_tableauSortie_Predit = pd.DataFrame(index=index_tableauSortie_Predit, columns=columns_tableauSortie_Predit)
        for heures in range(NB_HEURES_Predit):
            df_tableauSortie_Predit['DATE'][heures] = DATE_FIN + timedelta(hours=heures)

        # --------- CALCUL ---------

        # A - Récupération des données réelles
        print('--- Récupération des données réelles ---') # pour les tests
        for jour in range(NB_JOURS+1):
            # Récupération des numéros de la date (jour, mois et année)
            DATE = DATE_DEBUT + timedelta(days=jour)
            print('- ' + str(DATE)) # pour les tests
            NUM_JOUR = str(DATE.day)
            NUM_MOIS = str(DATE.month - 1)
            NUM_ANNEE = str(DATE.year)
            # Ecriture de la requête HTTP
            strURL = 'https://www.meteociel.fr/temps-reel/obs_villes.php?code2=' + ID_HISTO + '&jour2=' + NUM_JOUR + '&mois2=' + NUM_MOIS + '&annee2=' + NUM_ANNEE + '.htm'
            # Envoi de la requête HTTP
            response = None
            soup = None
            waiter = 0
            while response is None and waiter < 25:
                response = urllib.request.urlopen(strURL)
                time.sleep(0.5)
                waiter += 1
            response = urllib.request.urlopen(strURL)
            soup = BeautifulSoup(response.read())
            try:
                # Récupération des valeurs
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
    
                    # S'il existe une ligne pour l'heure considérée
                    if not np.isnan(heure):
    
                        # Température extérieure
                        A = soup.select('body > table:nth-child(1) > tbody > tr.texte > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > center:nth-child(14) > table:nth-child(3) > tr:nth-child(' + str(n) + ') > td:nth-child(5) > div')
                        B = unicodedata.normalize("NFKD", str(A))
                        pos1 = B.find('>')+1
                        pos2 = B.find('°C')
                        try:
                            C = float(B[pos1:pos2])
                        except:
                            C = np.nan
                        df_tableauSortie_Reel['T_EXT'][df_tableauSortie_Reel['DATE'] == DATE.replace(hour=0) + timedelta(hours=heure)] = C
    
                        # Humidité relative
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
                print('erreur BM105 - API météo indisponible, réessayer plus tard. Si l\'erreur se reproduit, contacter Cylergie.')
                        
        # B - Récupération des données de prévisions
        print('--- Récupération des données de prévisions ---') # pour les tests

        # B.1 – Import des données de prévision toutes les 3 heures pour les 4 prochains jours
        print('- Import des données de prévision toutes les 3 heures pour les 4 prochains jours') # pour les tests
        # Ecriture de la requête HTTP
        strURL = 'http://www.meteociel.fr/previsions/' + ID_PREV + '/' + NOM + '.htm'
        # Envoi de la requête HTTP
        response = urllib.request.urlopen(strURL)
        soup = BeautifulSoup(response.read())
        try:      
            # Récupération de la première heure de prévision disponible
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
    
            # Récupération des valeurs
            for i in range(0, 24*4, 3):
                n = i/3 + 3
    
                # Température extérieure
                A = soup.select('body > table:nth-child(4) > tbody > tr.texte > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > center:nth-child(4) > table > tr > td:nth-child(1) > table:nth-child(1) > tr:nth-child(' + str(int(n)) + ') > td:nth-child(2)')
                B = unicodedata.normalize("NFKD", str(A))
                pos1 = B.find('>')+1
                pos2 = B.find('°C')
                try:
                    C = float(B[pos1:pos2])
                except:
                    C = np.nan
                if np.isnan(C):
                    A = soup.select('body > table:nth-child(4) > tbody > tr.texte > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > center:nth-child(4) > table > tr > td:nth-child(1) > table:nth-child(1) > tr:nth-child(' + str(int(n)) + ') > td:nth-child(3)')
                    B = unicodedata.normalize("NFKD", str(A))
                    pos1 = B.find('>')+1
                    pos2 = B.find('°C')
                    try:
                        C = float(B[pos1:pos2])
                    except:
                        C = np.nan
                df_tableauSortie_Predit['T_EXT'][df_tableauSortie_Predit['DATE'] == day + timedelta(hours=i)] = C
    
                # Humidité relative
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
            print('erreur BM105 - API météo indisponible, réessayer plus tard. Si l\'erreur se reproduit, contacter Cylergie.')
                 
        # B.2 – Import des données de prévision toutes les 6 heures pour les 3 à 10 jours à venir
        print('- Import des données de prévision toutes les 6 heures pour les 3 à 10 jours à venir') # pour les tests
        # Ecriture de la requête HTTP
        strURL = 'http://www.meteociel.fr/tendances/' + ID_PREV + '/' + NOM + '.htm'
        # Envoi de la requête HTTP
        response = urllib.request.urlopen(strURL)
        soup = BeautifulSoup(response.read())
        try:  
            # Récupération de la première heure de prévision disponible
            day = DATE_MAINTENANT + timedelta(days=4)
            A = soup.select('body > table:nth-child(4) > tbody > tr.texte > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > center:nth-child(4) > table > tr > td:nth-child(1) > table:nth-child(1) > tr:nth-child(3) > td:nth-child(2)')
            B = unicodedata.normalize("NFKD", str(A))
            pos1 = B.find('>')+1
            pos2 = B.find(':')
            try:
                C = int(B[pos1:pos2])
                day = day.replace(hour=C, minute=0, second=0, microsecond=0)
            except:
                C = math.nan
    
            # Récupération des valeurs
            for i in range(0, 24*7, 6):
                n = i/6 + 3
    
                # Température extérieure
                A = soup.select('body > table:nth-child(4) > tbody > tr.texte > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > center:nth-child(4) > table > tr > td:nth-child(1) > table:nth-child(1) > tr:nth-child(' + str(int(n)) + ') > td:nth-child(2)')
                B = unicodedata.normalize("NFKD", str(A))
                pos1 = B.find('>')+1
                pos2 = B.find('°C')
                try:
                    C = float(B[pos1:pos2])
                except:
                    C = np.nan
                if np.isnan(C):
                    A = soup.select('body > table:nth-child(4) > tbody > tr.texte > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > center:nth-child(4) > table > tr > td:nth-child(1) > table:nth-child(1) > tr:nth-child(' + str(int(n)) + ') > td:nth-child(3)')
                    B = unicodedata.normalize("NFKD", str(A))
                    pos1 = B.find('>')+1
                    pos2 = B.find('°C')
                    try:
                        C = float(B[pos1:pos2])
                    except:
                        C = np.nan
                df_tableauSortie_Predit['T_EXT'][df_tableauSortie_Predit['DATE'] == day + timedelta(hours=i)] = C
    
                # Humidité relative
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
            print('erreur BM105 - API météo indisponible, réessayer plus tard. Si l\'erreur se reproduit, contacter Cylergie.')
                     
        # B.3 - Réchantillonage pour combler les trous dans les prévisions
        print('- Réchantillonage pour combler les trous dans les prévisions') # pour les tests
        df_tableauSortie_Predit['T_EXT'] = df_tableauSortie_Predit['T_EXT'].astype(float).interpolate(method='linear', limit_area='inside')
        df_tableauSortie_Predit['HR'] = df_tableauSortie_Predit['HR'].astype(float).interpolate(method='linear', limit_area='inside')

        # --------- Données de sorties ---------
        historiqueMeteo = df_tableauSortie_Reel
        previsionMeteo = df_tableauSortie_Predit
        print(historiqueMeteo)
        print(previsionMeteo)
        print('---------- Fin récupération des données météo ----------') # pour les tests
        return historiqueMeteo, previsionMeteo        
        

    def IA(self):
        
        # pour les tests
        global DFtoCSV
        global previsionMeteo
        global historiqueDemande
        global historiqueMeteo
        global previsionDemande
        global DEMANDE_RESEAU_PREDITE
        print('---------- Début calcul prévisionnel avec l\'IA ----------') # pour les tests
        
        # --------- Données d’entrées ---------
        print('--- Récupération des données d\'entrées ---') # pour les tests
        # Nombre de jours de prévisions
        Nb_jours_prevision = 11
        # Chargement des données historique déjà récupérées
        try: # Tentative d'ouverture du fichier de données
            with open(str(self.authentification)+'.pickle', 'rb') as BDD:
                print('- Fichier historique ' + self.authentification + '.pickle' + ' trouvé') # pour les tests
                # Chargement des données
                self.BDD_historique = pickle.load(BDD)
                # Suppression des lignes créées pour la prévision
                self.BDD_historique.drop(self.BDD_historique.tail(Nb_jours_prevision*24).index,inplace=True)
                # Récupération de la dernière date de la base de données
                self.dateDernieresDonnees = self.BDD_historique.index[-1]
                print('- Dernière donnée datant du ' + str(self.dateDernieresDonnees)) # pour les tests
                # Renomage des colonnes à supprimer si non nécessaire
                self.BDD_historique.rename(columns={"time":"DATE","heat.hist":"DEMANDE_RESEAU","temp.hist":"T_EXT","humi.hist":"HR"},inplace=True)
                self.BDD_historique.insert(0, 'DATE', self.BDD_historique.index, allow_duplicates = False)
                # Chargement de la BDD réalisé
                self.BDD_ok = True
        except OSError: # Si le fichier de données n'existe pas
            print('Fichier historique ' + str(self.authentification) + '.pickle' + ' non trouvé') # pour les tests
            self.BDD_ok = False
            self.dateDernieresDonnees = None
        # Dates
        DERNIERE_DATE = self.dateDernieresDonnees # on récupère la date des dernières données téléchargées
        DATE_MAINTENANT = self.dateMaintenant # on récupère la date actuelle (au moment du lancement de l'API IA)

        # --------- Définition de la plage d’étude ---------
        # Début de la plage d'étude
        DATE_DEBUT = DATE_MAINTENANT.replace(year=DATE_MAINTENANT.year - 1)
        DATE_DEBUT = DATE_DEBUT.replace(minute=0, second=0, microsecond=0)
        # Fin de la plage d'étude
        DATE_FIN = DATE_MAINTENANT + timedelta(days=Nb_jours_prevision)
        DATE_FIN = DATE_FIN.replace(minute=0, second=0, microsecond=0)    
            
        # --------- Données de sorties ---------
        # Création du fichier de sorties
        index_DFtoCSV = pd.date_range(start=DATE_DEBUT, end=DATE_FIN, freq='1H')
        columns_DFtoCSV = ['time']
        DFtoCSV = pd.DataFrame(data=index_DFtoCSV, columns=columns_DFtoCSV)
        DFtoCSV['time'] = pd.to_datetime(DFtoCSV['time'])
        DFtoCSV.set_index('time', inplace=True)

        # --------- Construction du fichier d'entrées de l'IA ---------
        print('--- Construction du fichier d\'entrées de l\'IA ---') # pour les tests
        # /// Récupération des données historique et prévision ///
        if self.BDD_ok:
            # Chargement de l'historique existant
            historiqueDemande_1 = self.BDD_historique[['DATE','DEMANDE_RESEAU']]
            historiqueMeteo_1 = self.BDD_historique[['DATE','T_EXT','HR']]
            # Téléchargement de l'historique manquant et des prévisions météo si besoin
            if (DATE_MAINTENANT-DERNIERE_DATE).total_seconds() /3600 < 1:
                historiqueDemande = historiqueDemande_1
                historiqueMeteo = historiqueMeteo_1
            else:
                historiqueDemande_2 = self.DonneesCofelyVision()
                [historiqueMeteo_2, previsionMeteo] = self.DonneesMeteo()
                historiqueDemande = pd.concat([historiqueDemande_1, historiqueDemande_2], ignore_index=True)
                historiqueMeteo = pd.concat([historiqueMeteo_1, historiqueMeteo_2], ignore_index=True)
        else:
            # Téléchargement de l'historique complet et des prévisions météo
            historiqueDemande = self.DonneesCofelyVision()
            [historiqueMeteo, previsionMeteo] = self.DonneesMeteo()
        # /// Mise en forme des données reçues ///
        historiqueDemande['time'] = pd.to_datetime(historiqueDemande['DATE'])
        historiqueMeteo['time'] = pd.to_datetime(historiqueMeteo['DATE'])
        previsionMeteo['time'] = pd.to_datetime(previsionMeteo['DATE'])
        historiqueDemande.set_index('time', inplace=True)
        historiqueMeteo.set_index('time', inplace=True)
        previsionMeteo.set_index('time', inplace=True)
        # /// Remplissage du Dataframe pour l'IA ///
        # Ecriture des données dans les bonnes colonnes
        DFtoCSV['heat.hist'] = historiqueDemande['DEMANDE_RESEAU']
        DFtoCSV['temp.hist'] = historiqueMeteo['T_EXT']
        DFtoCSV['humi.hist'] = historiqueMeteo['HR']
        DFtoCSV['temp.fore'] = previsionMeteo['T_EXT']
        DFtoCSV['humi.fore'] = previsionMeteo['HR']
        DFtoCSV = DFtoCSV[['heat.hist', 'temp.hist', 'humi.hist', 'temp.fore', 'humi.fore']]
        # Remise des données au bon format
        DFtoCSV['heat.hist'] = DFtoCSV['heat.hist'].astype('float')
        DFtoCSV['temp.hist'] = DFtoCSV['temp.hist'].astype('float')
        DFtoCSV['humi.hist'] = DFtoCSV['humi.hist'].astype('float')
        DFtoCSV['humi.fore'] = DFtoCSV['humi.fore'].astype('float')
        DFtoCSV['temp.fore'] = DFtoCSV['temp.fore'].astype('float')
        DFtoCSV.sort_index(inplace=True)
        # Suppression des dernières lignes si aucune donnée de prévision
        while DFtoCSV.iloc[-1,:].isnull().sum()==5:
            DFtoCSV.drop(DFtoCSV.tail(1).index, inplace = True) 
        # /// Sauvegarde des données historique ///
        with open(str(self.authentification)+'.pickle', 'wb') as BDD:
            pickle.dump(DFtoCSV, BDD)
        # /// Sauvegarde des données de prévision météo ///
        with open(str(self.authentification)+'_meteo.pickle', 'wb') as BDD:
            pickle.dump(previsionMeteo, BDD)
        # /// Ecriture des données dans un fichier csv pour envoi à l'API IA ///
        filename = 'filetoIA.csv'
        # DFtoCSV.to_csv(filename, encoding='utf-8', na_rep="", decimal=',', sep=';', date_format='%d/%m/%Y %H:%M')
        
        # --------- Appel de l'IA ---------
        print('--- Appel de l\'IA ---') # pour les tests
        # Status de fonctionnement de l'IA
        outcome_status = list()
        outcome_status.append("DONE")
        outcome_status.append("ERROR")
        # Paramètres de connexion à l'IA
        URL = "https://api.preprod.csai.crigen.myengie.com/bmc/" # API URL
        keyId = {'KeyId': '2a564819-f601-4e32-8be6-9863578d6353'} # keyId for the meeting     
        # Test de connexion
        API_ENDPOINT = URL + "health"
        requete = requests.get(url=API_ENDPOINT, headers=keyId)
        status = requete.status_code
        # Lancement de la prévision via l'API IA
        if status == 200: # connection ok
            data = {"network_name": "Network.001"}  # nom du site utilisé, ne sera pas utile dans la V2
            files = {'history': (filename, open(filename, 'rb')),} # nom du fichier de données
            # Envoi de la requête
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
                # Récuperation des données
                Data = reponse2.json()
                # Récupération des données de prévisions
                DATE_PREDITE = []
                DEMANDE_RESEAU_PREDITE = []
                for index in range(len(Data[0]['inferenceResult'])):
                    DATE_PREDITE.append(Data[0]['inferenceResult'][index]['date'])
                    if(isinstance(Data[0]['inferenceResult'][index]['value'], str)):
                        DEMANDE_RESEAU_PREDITE.append(Data[0]['inferenceResult'][index]['value'])
                    else:
                        DEMANDE_RESEAU_PREDITE.append(round(Data[0]['inferenceResult'][index]['value'], 2))
                previsionDemande = pd.DataFrame(columns=['DATE', 'DEMANDE'])
                previsionDemande['DATE'] = DATE_PREDITE
                previsionDemande['DEMANDE'] = DEMANDE_RESEAU_PREDITE
                # Sauvegarde des prévisions de la demande
                with open(str(self.authentification)+'_demande.pickle', 'wb') as BDD:
                    print('--- Sauvegarde de la prevision demande de chaleur ---') # pour les tests
                    pickle.dump(previsionDemande, BDD)
            elif task_status == 'ERROR':
                print('erreur BM101 - Contacter Cylergie.')
            else:
                print('erreur BM102 - Contacter Cylergie.')
        else:
            print('erreur BM103 - API IA indisponible, réessayer plus tard. Si l\'erreur se reproduit, contacter Cylergie.')

        # --------- Données de sorties ---------
        print('---------- Fin calcul prévisionnel avec l\'IA ----------') # pour les tests
        return previsionDemande


    def FonctionnementChaudiere(self):
        
        global df_tableauEntree, data_tableauEntrees, Prev_Demande # pour les tests
        print('---------- Début calcul du fonctionnement des chaudières ----------') # pour les tests
            
        # --------- Données d’entrées ---------
        # Tableau de la demande du réseau prédite
        columns_tableauEntrees = ['DATE', 'DEMANDE']
        
        # === CHGT JLE POUR DEMO
        #data_tableauEntrees = self.IA()
        with open(str(self.authentification)+'_demande.pickle', 'rb') as BDD:
            data_tableauEntrees = pickle.load(BDD)
        # === CHGT JLE POUR DEMO

        df_tableauEntree = pd.DataFrame(data=data_tableauEntrees, columns=columns_tableauEntrees)
        df_tableauEntree['DATE'] = pd.to_datetime(df_tableauEntree['DATE'])
        DEMANDE = df_tableauEntree['DEMANDE'].astype(float)
        # Caractéristiques de la chaufferie
        P_BASE = self.pCoge # Puissance d'un système en base
        print('--- puissance d\'un système en base ---') # pour les tests
        print(P_BASE) # pour les tests
        PILOTAGE = self.typePilotage # Type de pilotage des chaudières
        print('--- type de pilotage des chaudières ---') # pour les tests
        print(PILOTAGE) # pour les tests
        NB_SILO = self.nbSilo # Nombre de silo répondant à la même demande réseau
        print('--- nombre de silo répondant à la même demande réseau ---') # pour les tests
        print(NB_SILO) # pour les tests
        PCI = self.pciBois # PCI du bois de chaque silo
        print('--- pci du bois de chaque silo ---') # pour les tests
        print(PCI) # pour les tests
        DENSITE = self.densiteBois # Densité du bois de chaque silo
        print('--- densité du bois de chaque silo ---') # pour les tests
        print(DENSITE) # pour les tests
        NB_CHAUDIERE = self.nbChaudiere # Nombre de chaudières associées à chaque silo
        print('--- nombre de chaudières associées à chaque silo ---') # pour les tests
        print(NB_CHAUDIERE) # pour les tests
        # Caractéristiques des chaudières
        PRIORITE = self.prioriteChaudiere # Priorité d'allumage des chaudières
        print('--- priorité d\'allumage des chaudières ---') # pour les tests
        print(PRIORITE) # pour les tests
        SILO = self.siloChaudiere # Silo d'appartenance des chaudières
        print('--- silo d\'appartenance des chaudières ---') # pour les tests
        print(SILO) # pour les tests
        P_NOM = self.pNomChaudiere # Puissance nominale des chaudières
        print('--- puissance nominale des chaudières ---') # pour les tests
        print(P_NOM) # pour les tests
        RENDEMENT = self.rendementChaudiere # Rendement des chaudières
        print('--- rendement des chaudières ---') # pour les tests
        print(RENDEMENT) # pour les tests
        P_MIN = self.pMinChaudiere # Puissance minimale des chaudières
        print('--- puissance minimale des chaudières ---') # pour les tests
        print(P_MIN) # pour les tests
        CHARGE = self.chargeChaudiere # Charge des chaudières
        # print('--- charge des chaudières ---') # pour les tests
        # print(CHARGE) # pour les tests
        # --------- Définition de la plage d’étude ---------
        DATE_DEBUT = df_tableauEntree['DATE'][0]
        print('--- date début ---') # pour les tests
        print(DATE_DEBUT) # pour les tests
        DATE_FIN = df_tableauEntree['DATE'][len(df_tableauEntree)-1]
        print('--- date fin ---') # pour les tests
        print(DATE_FIN) # pour les tests
        NB_HEURES = math.floor((DATE_FIN-DATE_DEBUT).total_seconds() / 3600) + 1
        print('--- nombre d\'heures ---') # pour les tests
        print(NB_HEURES) # pour les tests
        # --------- Paramètres intermédiaires ---------
        NB_CHAUDIERE_TOTAL = sum(NB_CHAUDIERE) # Nombre de chaudières biomasse total
        print('--- nombre de chaudières total ---') # pour les tests
        print(NB_CHAUDIERE_TOTAL) # pour les tests
        NB_ALLUME = NB_CHAUDIERE_TOTAL # Nombre de chaudières biomasse qui doivent être allumées pour répondre à la demande réseau (pour le cas d'un pilotage de type maximum de chaudières)
        print('--- nombre de chaudières allumées ---') # pour les tests
        print(NB_ALLUME) # pour les tests
        CH_NUM = np.zeros((NB_CHAUDIERE_TOTAL), int)
        CPT = -1 # Compteur
        # Complément du tableau de données d'entrées
        P_BIOMASSE_CH = np.zeros([NB_HEURES, NB_CHAUDIERE_TOTAL]) # Puissance à fournir pour chaque chaudière biomasse
        P_DISPO_CH = np.zeros([NB_HEURES, NB_CHAUDIERE_TOTAL]) # Puissance disponible pour chaque chaudière biomasse
        P_BIOMASSE = np.zeros(NB_HEURES) # Puissance totale restant à fournir pour toutes les chaudières biomasse
        P_DISPO = np.zeros(NB_HEURES) # Puissance totale disponible pour toutes les chaudières biomasse

        # --------- Données de sorties ---------
        # Initialisation du tableau de sortie
        columns_tableauSortie = ['DATE']
        for i in range(NB_SILO):
            columns_tableauSortie += ['BESOIN_BIOMASSE_SILO'+str(i+1)]
        df_tableauSortie = pd.DataFrame(columns=columns_tableauSortie)
        # Remplissage de la colonne DATE
        df_tableauSortie['DATE'] = df_tableauEntree['DATE']

        # --------- CALCUL ---------

        # /// Calcul de la puissance à fournir par l'ensemble de chaudières biomasse ///
        # print('--- Calcul de la puissance à fournir par l\'ensemble de chaudières biomasse ---') # pour les tests
        P_BIOMASSE = DEMANDE - P_BASE
        P_BIOMASSE[P_BIOMASSE < 0] = 0
        # print(P_BIOMASSE) # pour les tests
        # /// Calcul de la puissance disponible pour chaque chaudière biomasse ///
        # print('--- Calcul de la puissance disponible pour chaque chaudière biomasse ---') # pour les tests
        for ch in range(NB_CHAUDIERE_TOTAL):
            P_DISPO_CH[:, ch] = P_NOM[ch] * CHARGE[:, ch] / 100
            for i in range(NB_HEURES):
                if P_DISPO_CH[i, ch] < P_MIN[CH_NUM[ch]]:
                    P_DISPO_CH[i, ch] = 0
        # print(P_DISPO_CH) # pour les tests
        # /// Reclassement des chaudières biomasse par ordre de priorité ///
        print('--- Reclassement des chaudières biomasse par ordre de priorité ---') # pour les tests
        for ch in range(NB_CHAUDIERE_TOTAL):
            CH_NUM[PRIORITE[ch]-1] = ch
        print(CH_NUM) # pour les tests
        # /// Calcul de la puissance à fournir pour chaque chaudière biomasse ///
        print('--- Calcul de la puissance à fournir pour chaque chaudière biomasse ---') # pour les tests

        for i in range(NB_HEURES):
            if PILOTAGE == 1: # Pilotage de type minimum de chaudières
                for ch in range(NB_CHAUDIERE_TOTAL):
                    if P_BIOMASSE[i] > 0:
                        if P_BIOMASSE[i] > P_DISPO_CH[i, CH_NUM[ch]]:
                            P_BIOMASSE_CH[i, CH_NUM[ch]] = P_DISPO_CH[i, CH_NUM[ch]]
                            P_BIOMASSE[i] -= P_BIOMASSE_CH[i, CH_NUM[ch]]
                        else:
                            if P_BIOMASSE[i] < P_MIN[CH_NUM[ch]]:
                                P_BIOMASSE_CH[i, CH_NUM[ch]] = 0
                            else:
                                P_BIOMASSE_CH[i, CH_NUM[ch]] = P_BIOMASSE[i]
                                P_BIOMASSE[i] -= P_BIOMASSE_CH[i, CH_NUM[ch]]
                    else:
                        P_BIOMASSE_CH[i, CH_NUM[ch]] = 0

            elif PILOTAGE == 2: # Pilotage de type maximum de chaudières
                CPT = 0
                # On allume toutes les chaudières possibles
                NB_ALLUME = NB_CHAUDIERE_TOTAL
                for ch in range(NB_CHAUDIERE_TOTAL):
                    if P_DISPO_CH[i, CH_NUM[ch]] == 0:
                        NB_ALLUME -= 1       
                # On calcule la puissance disponible totale
                for ch in range(NB_CHAUDIERE_TOTAL):
                    P_DISPO[i] += P_DISPO_CH[i, CH_NUM[ch]]
                # EN COURS
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
                        elif P < P_MIN[CH_NUM[ch]]:
                            NB_ALLUME -= 1
                            P_BIOMASSE_CH[i, :] = 0
                            P_DISPO[i] -= P_DISPO_CH[i, CH_NUM[ch]]
                            CPT = max(0,CPT-1)
                            break
                        elif P > P_DISPO_CH[i, CH_NUM[ch]]:
                            P_BIOMASSE_CH[i, CH_NUM[ch]] = P_DISPO_CH[i, CH_NUM[ch]]
                            CPT += 1
                        else:
                            P_BIOMASSE_CH[i, CH_NUM[ch]] = P_DISPO_CH[i, CH_NUM[ch]] * P_BIOMASSE[i] / P_DISPO[i]
                            CPT += 1

        # print('pbiomasse') # pour les tests
        # print(P_BIOMASSE_CH) # pour les tests
        # print('Rendement') # pour les tests
        # print(RENDEMENT) # pour les tests

        # /// Calcul du volume de bois nécessaire par site ou silo ///
        print('--- Calcul du volume de bois nécessaire par site ou silo ---') # pour les tests
        for silo in range(NB_SILO):
            # Initialisation
            df_tableauSortie['BESOIN_BIOMASSE_SILO'+str(silo+1)] = 0.0
            # Ajout des besoins par chaudière
            for ch in range(NB_CHAUDIERE_TOTAL):
                if SILO[ch]-1 == silo:
                    for i in range(NB_HEURES):
                        df_tableauSortie.loc[i,'BESOIN_BIOMASSE_SILO'+str(silo+1)] += P_BIOMASSE_CH[i, ch] / (RENDEMENT[ch]/100) / PCI[silo] / DENSITE[silo] # JLE à verifier
        
        # --------- Données de sorties ---------
        previsionBesoinBiomasse = df_tableauSortie
        # display(previsionBesoinBiomasse)
        
        with open(str(self.authentification)+'_biomasse.pickle', 'wb') as BDD:
            print('--- Sauvegarde de la prévision demande de biomasse ---') # pour les tests
            pickle.dump(previsionBesoinBiomasse, BDD)
        print('---------- Fin calcul du fonctionnement des chaudières ----------') # pour les tests
        return previsionBesoinBiomasse


    def CalculPlanningAppro(self):
        global silo, NB_SILO, df_tableauEntree, df_tableauSortie # pour les tests
        print('---------- Début calcul du planning d\'approvisionnement ----------') # pour les tests

        # --------- Données d’entrées ---------
        HEURE_MATIN = 9
        HEURE_APRESMIDI = 14
        # Tableau du besoin de biomasse nécessaire aux chaudières pour couvrir la demande du réseau (prédite)
        df_tableauEntree = self.FonctionnementChaudiere()

        # Caractéristiques de la chaufferie
        NB_SILO = self.nbSilo # Nombre de silo répondant à la même demande réseau
        print('--- nombre de silo ---') # pour les tests
        print(NB_SILO) # pour les tests
        # Contraintes sur le planning (une ligne = un silo)
        NB_CAMIONS_MIN_1 = self.nbCamionsMin[0] # Nombre de livraisons minimum qu'il est possible de recevoir dans la matinée
        print('--- nombre de livraisons minimum matin ---') # pour les tests
        print(NB_CAMIONS_MIN_1) # pour les tests
        NB_CAMIONS_MIN_2 = self.nbCamionsMin[1] # Nombre de livraisons minimum qu'il est possible de recevoir dans l'après-midi
        print('--- nombre de livraisons minimum midi ---') # pour les tests
        print(NB_CAMIONS_MIN_2) # pour les tests
        NB_CAMIONS_MAX_1 = self.nbCamionsMax[0] # Nombre de livraisons maximum qu'il est possible de recevoir dans la matinée
        print('--- nombre de livraisons maximum matin ---') # pour les tests
        print(NB_CAMIONS_MAX_1) # pour les tests
        NB_CAMIONS_MAX_2 = self.nbCamionsMax[1] # Nombre de livraisons maximum qu'il est possible de recevoir dans l'après-midi
        print('--- nombre de livraison maximum midi ---') # pour les tests
        print(NB_CAMIONS_MAX_2) # pour les tests
        VOLUME_CAMIONS = self.volumeCamion # Volume des camions livrés
        print('--- volume des camions livrés ---') # pour les tests
        print(VOLUME_CAMIONS) # pour les tests
        # Contraintes sur le stockage de bois (une ligne = un silo)
        NIVEAU_MIN_1 = self.niveauMinSilo[0] # Seuil de remplissage minimum à respecter dans la matinée
        NIVEAU_MIN_2 = self.niveauMinSilo[1] # Seuil de remplissage minimum à respecter dans l'après-midi
        NIVEAU_MAX_1 = self.niveauMaxSilo[0] # Seuil de remplissage maximum à respecter dans la matinée
        NIVEAU_MAX_2 = self.niveauMaxSilo[1] # Seuil de remplissage maximum à respecter dans l'après-midi

        # === CHGT JLE POUR DEMO
        VOLUME_STOCK = []
        #for niveau, niveauMax in zip(self.niveauSilo, self.niveauMaxSilo):
        #    VOLUME_STOCK.append(niveau  * niveauMax / 100)
        VOLUME_STOCK = self.volumeMaxSilo #*obj_remplissage
        print('--- volume de stockage disponible ---') # pour les tests
        print(VOLUME_STOCK) # pour les tests
        print('--- niveau de stockage ---') # pour les tests
        print(self.niveauSilo) # pour les tests
        print('--- niveau max du stockage ---') # pour les tests
        print(self.niveauMaxSilo) # pour les tests
        # Niveau actuel du stock
        # NIVEAU_ACTUEL_INITIAL = self.niveauSilo
        NIVEAU_ACTUEL_INITIAL = []
        for niveau, volumeMaxSilo in zip(self.niveauSilo, self.volumeMaxSilo):
            NIVEAU_ACTUEL_INITIAL.append(niveau  / volumeMaxSilo * 100)
        print('--- niveau actuel de stockage ---') # pour les tests
        print(NIVEAU_ACTUEL_INITIAL) # pour les tests
        # === CHGT JLE POUR DEMO

        # --------- Définition de la plage d’étude ---------
        DATE_DEBUT = df_tableauEntree['DATE'][0]
        DATE_FIN = df_tableauEntree['DATE'][len(df_tableauEntree)-1]
        NB_HEURES = math.floor((DATE_FIN-DATE_DEBUT).total_seconds() / 3600) + 1
        NB_JOURS = math.floor(NB_HEURES/24)

        # --------- Paramètres intermédiaires ---------
        # Complément du tableau de données d'entrées (pas de temps horaire)
        df_tableauEntree['JOUR'] = -9999
        for h in range(NB_HEURES):
            df_tableauEntree.loc[h,'JOUR'] = df_tableauEntree.loc[h,'DATE'].day - df_tableauEntree.loc[0,'DATE'].day
        df_tableauEntree['HEURE'] = -9999
        for h in range(NB_HEURES):
            df_tableauEntree.loc[h,'HEURE'] = df_tableauEntree.loc[h,'DATE'].hour
        for silo in range(NB_SILO):
            # Sur les contraintes de livraison
            df_tableauEntree['NB_CAMIONS_MIN'+str(silo+1)] = np.nan # Nombre de livraisons minimum qu’il faut encore recevoir jusqu’à la fin de la demi-journée
            df_tableauEntree['NB_CAMIONS_MAX'+str(silo+1)] = np.nan # Nombre de livraisons maximum qu’il est encore possible de recevoir sur la demi-journée
            df_tableauEntree['VOLUME_CAMION'+str(silo+1)] = np.nan # Quantité maximale de bois qui peut encore être livrée sur la demi-journée
            # Sur les contraintes sur le stockage de bois
            df_tableauEntree['NIVEAU_MIN'+str(silo+1)] = np.nan # Seuil limite basse de remplissage du stockage
            df_tableauEntree['VOLUME_MIN'+str(silo+1)] = np.nan # Volume minimum de remplissage du stockage
            df_tableauEntree['NIVEAU_MAX'+str(silo+1)] = np.nan # Seuil limite haute de remplissage du stockage
            df_tableauEntree['VOLUME_MAX'+str(silo+1)] = np.nan # Volume maximum de remplissage du stockage
            df_tableauEntree['NIVEAU_ACTUEL'+str(silo+1)] = np.nan # Niveau du stock
            df_tableauEntree['VOLUME_ACTUEL'+str(silo+1)] = np.nan # Volume du stock
            # Sur les livraisons
            df_tableauEntree['NB_CAMIONS'+str(silo+1)] = np.nan # Nombre de camions nécessaires

        # --------- Données de sorties ---------
        # Initialisation du tableau de sorties
        columns_tableauSortie = ['DATE']
        for silo in range(NB_SILO):
            columns_tableauSortie += ['NB_CAMIONS_1_SILO'+str(silo+1)]
            columns_tableauSortie += ['NB_CAMIONS_2_SILO'+str(silo+1)]
        index_tableauSortie = range(NB_JOURS)
        df_tableauSortie = pd.DataFrame(index=index_tableauSortie, columns=columns_tableauSortie)
        # Remplissage de la colonne DATE
        for j in range(NB_JOURS):
            df_tableauSortie.loc[j,'DATE'] = (DATE_DEBUT+ timedelta(j)).strftime('%Y-%m-%d')
        # === CHGT JLE POUR DEMO
        # Initialisation du tableau de sorties 2
        columns_tableauSortie2 = ['DATE']
        for silo in range(NB_SILO):
            columns_tableauSortie2 += ['VOLUME_ACTUEL'+str(silo+1)]
        index_tableauSortie2 = range(NB_JOURS)
        df_tableauSortie2 = pd.DataFrame(index=index_tableauSortie2, columns=columns_tableauSortie2)
        # Remplissage de la colonne DATE
        for j in range(NB_HEURES):
            df_tableauSortie2.loc[j,'DATE'] = df_tableauEntree.loc[j,'DATE']
        # === CHGT JLE POUR DEMO

        # --------- CALCUL ---------

        # /// Calcul heure par heure du nombre de camions nécessaire par site ou silo ///
        print('--- Calcul heure par heure du nombre de camions nécessaire par site ou silo ---') # pour les tests

        for silo in range(NB_SILO):

            print('- Calcul pour le silo ' + str(silo+1) + '/' + str(NB_SILO)) # pour les tests

            # == Initialisation des premières lignes des demi-journées dans le tableau de données d’entrées ==
            for j in range(NB_JOURS):
                for h in range(NB_HEURES):
                    if df_tableauEntree['JOUR'][h] == j:
                        if df_tableauEntree['HEURE'][h] == HEURE_MATIN:
                            df_tableauEntree.loc[h,'NB_CAMIONS_MIN'+str(silo+1)] = NB_CAMIONS_MIN_1[silo][j]
                            df_tableauEntree.loc[h,'NB_CAMIONS_MAX'+str(silo+1)] = NB_CAMIONS_MAX_1[silo][j]
                            df_tableauEntree.loc[h,'VOLUME_CAMION'+str(silo+1)] = VOLUME_CAMIONS[silo]
                            df_tableauEntree.loc[h,'NIVEAU_MIN'+str(silo+1)] = NIVEAU_MIN_1[silo][j]
                            df_tableauEntree.loc[h,'VOLUME_MIN'+str(silo+1)] = NIVEAU_MIN_1[silo][j]/100 * VOLUME_STOCK[silo]
                            df_tableauEntree.loc[h,'NIVEAU_MAX'+str(silo+1)] = NIVEAU_MAX_1[silo][j]
                            df_tableauEntree.loc[h,'VOLUME_MAX'+str(silo+1)] = NIVEAU_MAX_1[silo][j]/100 * VOLUME_STOCK[silo]
                        elif df_tableauEntree['HEURE'][h] == HEURE_APRESMIDI:
                            df_tableauEntree.loc[h,'NB_CAMIONS_MIN'+str(silo+1)] = NB_CAMIONS_MIN_2[silo][j]
                            df_tableauEntree.loc[h,'NB_CAMIONS_MAX'+str(silo+1)] = NB_CAMIONS_MAX_2[silo][j]
                            df_tableauEntree.loc[h,'VOLUME_CAMION'+str(silo+1)] = VOLUME_CAMIONS[silo]
                            df_tableauEntree.loc[h,'NIVEAU_MIN'+str(silo+1)] = NIVEAU_MIN_2[silo][j]
                            df_tableauEntree.loc[h,'VOLUME_MIN'+str(silo+1)] = NIVEAU_MIN_2[silo][j]/100 * VOLUME_STOCK[silo]
                            df_tableauEntree.loc[h,'NIVEAU_MAX'+str(silo+1)] = NIVEAU_MAX_2[silo][j]
                            df_tableauEntree.loc[h,'VOLUME_MAX'+str(silo+1)] = NIVEAU_MAX_2[silo][j]/100 * VOLUME_STOCK[silo]   

            # == Initialisation de la toute première ligne dans le tableau de données d’entrées ==
            for j in range(NB_JOURS):
                if df_tableauEntree['JOUR'][0] == j:                
                    if df_tableauEntree['HEURE'][0] != HEURE_MATIN and df_tableauEntree['HEURE'][0] != HEURE_APRESMIDI:
                        if df_tableauEntree['HEURE'][0] > HEURE_MATIN and df_tableauEntree['HEURE'][0] < HEURE_APRESMIDI:
                            df_tableauEntree.loc[0,'NB_CAMIONS_MIN'+str(silo+1)] = NB_CAMIONS_MIN_1[silo][j]
                            df_tableauEntree.loc[0,'NB_CAMIONS_MAX'+str(silo+1)] = NB_CAMIONS_MAX_1[silo][j]
                            df_tableauEntree.loc[0,'VOLUME_CAMION'+str(silo+1)] = VOLUME_CAMIONS[silo]
                            df_tableauEntree.loc[0,'NIVEAU_MIN'+str(silo+1)] = NIVEAU_MIN_1[silo][j]
                            df_tableauEntree.loc[0,'VOLUME_MIN'+str(silo+1)] = NIVEAU_MIN_1[silo][j]/100 * VOLUME_STOCK[silo]
                            df_tableauEntree.loc[0,'NIVEAU_MAX'+str(silo+1)] = NIVEAU_MAX_1[silo][j]
                            df_tableauEntree.loc[0,'VOLUME_MAX'+str(silo+1)] = NIVEAU_MAX_1[silo][j]/100 * VOLUME_STOCK[silo]
                        elif df_tableauEntree['HEURE'][0] < HEURE_MATIN or df_tableauEntree['HEURE'][0] > HEURE_APRESMIDI:
                            df_tableauEntree.loc[0,'NB_CAMIONS_MIN'+str(silo+1)] = NB_CAMIONS_MIN_2[silo][j]
                            df_tableauEntree.loc[0,'NB_CAMIONS_MAX'+str(silo+1)] = NB_CAMIONS_MAX_2[silo][j]
                            df_tableauEntree.loc[0,'VOLUME_CAMION'+str(silo+1)] = VOLUME_CAMIONS[silo]
                            df_tableauEntree.loc[0,'NIVEAU_MIN'+str(silo+1)] = NIVEAU_MIN_2[silo][j]
                            df_tableauEntree.loc[0,'VOLUME_MIN'+str(silo+1)] = NIVEAU_MIN_2[silo][j]/100 * VOLUME_STOCK[silo]
                            df_tableauEntree.loc[0,'NIVEAU_MAX'+str(silo+1)] = NIVEAU_MAX_2[silo][j]
                            df_tableauEntree.loc[0,'VOLUME_MAX'+str(silo+1)] = NIVEAU_MAX_2[silo][j]/100 * VOLUME_STOCK[silo]
            df_tableauEntree.loc[0,'NIVEAU_ACTUEL'+str(silo+1)] = NIVEAU_ACTUEL_INITIAL[silo]
            df_tableauEntree.loc[0,'VOLUME_ACTUEL'+str(silo+1)] = NIVEAU_ACTUEL_INITIAL[silo]/100 * VOLUME_STOCK[silo]

            # == Calcul horaire ==
            for h in range(NB_HEURES):

                # Test si on a les données sur la ligne d'étude
                CPT = 0
                if np.isnan(df_tableauEntree['NIVEAU_MAX'+str(silo+1)][h]):
                    CPT += 1
                if np.isnan(df_tableauEntree['NIVEAU_MIN'+str(silo+1)][h]):
                    CPT += 1
                if np.isnan(df_tableauEntree['NIVEAU_ACTUEL'+str(silo+1)][h]):
                    CPT += 1

                # Nombre de camions
                if CPT == 0:
                    if df_tableauEntree['HEURE'][h] >= HEURE_MATIN and df_tableauEntree['HEURE'][h] < (HEURE_APRESMIDI + 4):
                        if df_tableauEntree['NIVEAU_ACTUEL'+str(silo+1)][h] < df_tableauEntree['NIVEAU_MAX'+str(silo+1)][h]:
                            if df_tableauEntree['NIVEAU_ACTUEL'+str(silo+1)][h] >= df_tableauEntree['NIVEAU_MIN'+str(silo+1)][h]:
                                df_tableauEntree.loc[h,'NB_CAMIONS'+str(silo+1)] = math.floor((df_tableauEntree['VOLUME_MAX'+str(silo+1)][h] - df_tableauEntree['VOLUME_ACTUEL'+str(silo+1)][h])/df_tableauEntree['VOLUME_CAMION'+str(silo+1)][h])
                            else:  
                                df_tableauEntree.loc[h,'NB_CAMIONS'+str(silo+1)] = math.floor((df_tableauEntree['VOLUME_MIN'+str(silo+1)][h] - df_tableauEntree['VOLUME_ACTUEL'+str(silo+1)][h])/df_tableauEntree['VOLUME_CAMION'+str(silo+1)][h])
                        else:
                            df_tableauEntree.loc[h,'NB_CAMIONS'+str(silo+1)] = 0
                    else:
                        df_tableauEntree.loc[h,'NB_CAMIONS'+str(silo+1)] = 0

                    # === CHGT JLE POUR DEMO    
                    #while df_tableauEntree.loc[h,'NB_CAMIONS'+str(silo+1)] < df_tableauEntree['NB_CAMIONS_MIN'+str(silo+1)][h]:
                    #    a = df_tableauEntree['VOLUME_ACTUEL'+str(silo+1)][h] - df_tableauEntree['BESOIN_BIOMASSE_SILO'+str(silo+1)][h] + df_tableauEntree['NB_CAMIONS'+str(silo+1)][h] * df_tableauEntree['VOLUME_CAMION'+str(silo+1)][h] / VOLUME_STOCK[silo]
                    #    if a < df_tableauEntree['NIVEAU_MAX'+str(silo+1)][h] :
                    #        df_tableauEntree.loc[h,'NB_CAMIONS'+str(silo+1)] += 1
                    #    else:
                    #        #JLE à compléter : message d'alerte
                    #        break
                       
                    #while df_tableauEntree.loc[h,'NB_CAMIONS'+str(silo+1)] > df_tableauEntree['NB_CAMIONS_MAX'+str(silo+1)][h]:
                    #    a = (df_tableauEntree['VOLUME_ACTUEL'+str(silo+1)][h] - df_tableauEntree['BESOIN_BIOMASSE_SILO'+str(silo+1)][h] + df_tableauEntree['NB_CAMIONS'+str(silo+1)][h] * df_tableauEntree['VOLUME_CAMION'+str(silo+1)][h])/ VOLUME_STOCK[silo]
                    #    if a > df_tableauEntree['NIVEAU_MIN'+str(silo+1)][h]:
                    #        df_tableauEntree.loc[h,'NB_CAMIONS'+str(silo+1)] -= 1
                    #    else:
                    #        #JLE à compléter : message d'alerte : il faut plus de camions que le nombre max qui peut être commandé pour assurer le niveau min du stock
                    #        break
                    # === CHGT JLE POUR DEMO   

                # Calcul des contraintes sur le pas de temps suivant
                if h != NB_HEURES-1:
                    if np.isnan(df_tableauEntree['NB_CAMIONS_MIN'+str(silo+1)][h+1]):
                        df_tableauEntree.loc[h+1,'NB_CAMIONS_MIN'+str(silo+1)] = max(0, df_tableauEntree['NB_CAMIONS_MIN'+str(silo+1)][h] - df_tableauEntree['NB_CAMIONS'+str(silo+1)][h])
                    if np.isnan(df_tableauEntree['NB_CAMIONS_MAX'+str(silo+1)][h+1]):
                        df_tableauEntree.loc[h+1,'NB_CAMIONS_MAX'+str(silo+1)] = max(0, df_tableauEntree['NB_CAMIONS_MAX'+str(silo+1)][h] - df_tableauEntree['NB_CAMIONS'+str(silo+1)][h])
                    if np.isnan(df_tableauEntree['VOLUME_CAMION'+str(silo+1)][h+1]):
                        df_tableauEntree.loc[h+1,'VOLUME_CAMION'+str(silo+1)] = df_tableauEntree['VOLUME_CAMION'+str(silo+1)][h]
                    if np.isnan(df_tableauEntree['NIVEAU_MIN'+str(silo+1)][h+1]):
                        df_tableauEntree.loc[h+1,'NIVEAU_MIN'+str(silo+1)] = df_tableauEntree['NIVEAU_MIN'+str(silo+1)][h]
                    if np.isnan(df_tableauEntree['VOLUME_MIN'+str(silo+1)][h+1]):
                        df_tableauEntree.loc[h+1,'VOLUME_MIN'+str(silo+1)] = df_tableauEntree['NIVEAU_MIN'+str(silo+1)][h+1] / 100 * VOLUME_STOCK[silo]
                    if np.isnan(df_tableauEntree['NIVEAU_MAX'+str(silo+1)][h+1]):
                        df_tableauEntree.loc[h+1,'NIVEAU_MAX'+str(silo+1)] = df_tableauEntree['NIVEAU_MAX'+str(silo+1)][h]
                    if np.isnan(df_tableauEntree['VOLUME_MAX'+str(silo+1)][h+1]):
                        df_tableauEntree.loc[h+1,'VOLUME_MAX'+str(silo+1)] = df_tableauEntree['NIVEAU_MAX'+str(silo+1)][h+1] / 100 * VOLUME_STOCK[silo]
                    if np.isnan(df_tableauEntree['NIVEAU_ACTUEL'+str(silo+1)][h+1]):
                        df_tableauEntree.loc[h+1,'NIVEAU_ACTUEL'+str(silo+1)] = 100 * max(0, df_tableauEntree['VOLUME_ACTUEL'+str(silo+1)][h] - df_tableauEntree['BESOIN_BIOMASSE_SILO'+str(silo+1)][h] + df_tableauEntree['NB_CAMIONS'+str(silo+1)][h] * df_tableauEntree['VOLUME_CAMION'+str(silo+1)][h]) / VOLUME_STOCK[silo]
                    if np.isnan(df_tableauEntree['VOLUME_ACTUEL'+str(silo+1)][h+1]):
                        df_tableauEntree.loc[h+1,'VOLUME_ACTUEL'+str(silo+1)] = df_tableauEntree['NIVEAU_ACTUEL'+str(silo+1)][h+1] / 100 * VOLUME_STOCK[silo]

        # /// Calcul du nombre total de camions nécessaire par site ou silo ///
        print('--- Calcul du nombre total de camions nécessaire par site ou silo ---') # pour les tests
        for silo in range(NB_SILO):
            for j in range(NB_JOURS):
                df_tableauSortie.loc[j,'NB_CAMIONS_1_SILO'+str(silo+1)] = 0
                df_tableauSortie.loc[j,'NB_CAMIONS_2_SILO'+str(silo+1)] = 0
                for h in range(NB_HEURES):
                    df_tableauSortie2.loc[h,'VOLUME_ACTUEL'+str(silo+1)] = 0
                    df_tableauSortie2.loc[h,'VOLUME_ACTUEL'+str(silo+1)] = df_tableauEntree.loc[h,'VOLUME_ACTUEL'+str(silo+1)]
                    if df_tableauEntree['JOUR'][h] == j:
                        if df_tableauEntree['HEURE'][h] >= HEURE_MATIN and df_tableauEntree['HEURE'][h] < HEURE_APRESMIDI:
                            df_tableauSortie.loc[j,'NB_CAMIONS_1_SILO'+str(silo+1)] += df_tableauEntree['NB_CAMIONS'+str(silo+1)][h]
                        elif df_tableauEntree['HEURE'][h] >= HEURE_APRESMIDI and df_tableauEntree['HEURE'][h] <= HEURE_APRESMIDI + 4:
                            df_tableauSortie.loc[j,'NB_CAMIONS_2_SILO'+str(silo+1)] += df_tableauEntree['NB_CAMIONS'+str(silo+1)][h]

        # --------- Données de sorties ---------
        previsionStockBiomasse = df_tableauSortie

        with open(str(self.authentification)+'_livraison.pickle', 'wb') as BDD:
            print('--- Sauvegarde du planning de livraison ---') # pour les tests
            pickle.dump(previsionStockBiomasse, BDD)
        with open(str(self.authentification)+'_stockAveclivraison.pickle', 'wb') as BDD:
            print('--- Sauvegarde de la prévision de l''évolution stock de biomasse ---') # pour les tests
            pickle.dump(df_tableauSortie2, BDD)
            print(df_tableauSortie2)
        print('---------- Fin calcul du planning d\'approvisionnement ----------') # pour les tests
        # display(previsionStockBiomasse)
        return previsionStockBiomasse
    