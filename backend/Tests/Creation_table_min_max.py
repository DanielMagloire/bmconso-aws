# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 08:13:44 2022

@author: SN5694
"""
NB_JOURS=11
NB_SILO=2
NB_CAMIONS_MIN_1=[]
NB_CAMIONS_MIN_2=[]
NB_CAMIONS_MAX_1=[]
NB_CAMIONS_MAX_2=[]
Niveaux_MIN_1=[]
Niveaux_MIN_2=[]
Niveaux_MAX_1=[]
Niveaux_MAX_2=[]
VOLUME_CAMIONS = 90

for silo in range(NB_SILO):
    NB_CAMIONS_MIN_1.append([])
    NB_CAMIONS_MIN_2.append([])
    NB_CAMIONS_MAX_1.append([])
    NB_CAMIONS_MAX_2.append([])
    Niveaux_MIN_1.append([])
    Niveaux_MIN_2.append([])
    Niveaux_MAX_1.append([])
    Niveaux_MAX_2.append([])
    for j in range(NB_JOURS):
        NB_CAMIONS_MIN_1[silo].append(1)
        NB_CAMIONS_MIN_2[silo].append(1)
        NB_CAMIONS_MAX_1[silo].append(30)
        NB_CAMIONS_MAX_2[silo].append(30)
        Niveaux_MIN_1[silo].append(1000)
        Niveaux_MIN_2[silo].append(1000)
        Niveaux_MAX_1[silo].append(10000)
        Niveaux_MAX_2[silo].append(10000)
nbCamionsMin=[]
nbCamionsMax=[]
NiveauxMin=[]
NiveauxMax=[]

nbCamionsMin.append(NB_CAMIONS_MIN_1)
nbCamionsMin.append(NB_CAMIONS_MIN_2)

nbCamionsMax.append(NB_CAMIONS_MAX_1)
nbCamionsMax.append(NB_CAMIONS_MAX_2)

NiveauxMin.append(Niveaux_MIN_1)
NiveauxMin.append(Niveaux_MIN_2)
       
NiveauxMax.append(Niveaux_MAX_1)
NiveauxMax.append(Niveaux_MAX_2)