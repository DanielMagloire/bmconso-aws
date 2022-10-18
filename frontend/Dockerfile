FROM node:lts-alpine

# installe un simple serveur http pour servir un contenu statique
RUN npm install -g http-server

# installer Node.js native addon build tool
RUN npm install -g node-gyp

# définit le dossier 'app' comme dossier de travail
WORKDIR /app

# copie 'package.json' et 'package-lock.json' (si disponible)
COPY package.json ./

# installe les dépendances du projet
RUN npm install

# copie les fichiers et dossiers du projet dans le dossier de travail (par exemple : le dossier 'app')
COPY . .

# lint all the code
# à décommenter une fois que le problème du web pack est réglé
#RUN npm run lint

# construit l'app pour la production en la minifiant
RUN npm run build

EXPOSE 8080
CMD [ "http-server", "dist" ]
