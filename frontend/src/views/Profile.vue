<template>
  <div class="view-profil" v-if="this.client !== null">
    <v-row no-gutters class="pa-5 fill-height">
      <v-col cols="3">
        <!--  données utilisateur -->
        <v-card class="pl-1 pt-4 pa-5 mb-5">
          <v-row no-gutters>
            <v-col cols="6">
              <v-card-title> {{ client.given_name }} {{ client.family_name }}</v-card-title>
              <v-card-subtitle>{{ client.preferred_username }}</v-card-subtitle>
            </v-col>
            <v-col cols="6" class="py-2">
              <v-card outlined class="fill-height">
                <v-row no-gutters>
                  <v-col cols="auto" class="pa-4">
                    <v-icon x-large color="primary" v-if="this.user.role === 'Utilisateur'">
                      mdi-account
                    </v-icon>
                    <v-icon x-large color="teal" v-if="this.user.role === 'Administrateur'">
                      mdi-account-supervisor
                    </v-icon>
                  </v-col>
                  <v-col cols="auto">
                    <v-divider vertical></v-divider>
                  </v-col>
                  <v-col class="role-col" @click="chgRole()">
                    <v-card-title
                      v-if="this.user.role === 'Administrateur'"
                      class="icon-label font-weight-bold text-h4 teal--text justify-center"
                      >ADM</v-card-title
                    >
                    <v-card-title
                      v-if="this.user.role === 'Utilisateur'"
                      class="icon-label font-weight-bold text-h4 primary--text justify-center"
                      >USR</v-card-title
                    >
                  </v-col>
                </v-row>
              </v-card>
            </v-col>
          </v-row>
          <v-row no-gutters class="pt-2">
            <v-col class="pl-5">
              Dernière connexion :
            </v-col>
            <v-col>
              {{ auth_time }}
            </v-col>
          </v-row>
          <v-row no-gutters class="pb-2">
            <v-col class="pl-5">
              Date d'expiration :
            </v-col>
            <v-col>
              {{ exp_time }}
            </v-col>
          </v-row>
          <v-row no-gutters>
            <v-col class="pl-5">
              E-mail :
            </v-col>
            <v-col>
              {{ client.email }}
            </v-col>
          </v-row>
        </v-card>
        <!-- barre de recherche -->
        <v-row no-gutters class="mb-5">
          <v-col cols="10">
            <v-text-field
              outlined
              class="elevation-2 mt-1"
              v-model="research"
              prefix="NOM :"
              type="text"
              hide-details
              single-line
              @keyup.enter="searchAddConfig()"
              style="text-transform:uppercase"
            />
          </v-col>
          <v-col v-if="this.user.role === 'Utilisateur'" class="search-col" cols="2">
            <v-btn large outlined elevation="2" :color="color" @click="searchConfig()" height="4.3em" style="min-width: 0">
              <v-icon>mdi-magnify-plus</v-icon>
            </v-btn>
          </v-col>
          <v-col v-if="this.user.role === 'Administrateur'" class="search-col" cols="2">
            <v-btn large outlined elevation="2" color="success" @click="addConfig()" style="min-width: 0" height="4.3em">
              <v-icon>mdi-plus-thick</v-icon>
            </v-btn>
          </v-col>
        </v-row>

        <!-- liste des configurations -->
        <v-list elevation="3">
          <v-subheader class="text-uppercase">
            <v-row class="pb-5">
              <v-col cols="10">
                liste des configurations
              </v-col>
              <!-- <v-btn icon>
                <v-icon 
                  color="success"
                  @click="addConfig()"
                >mdi-plus-thick</v-icon>
              </v-btn> -->
            </v-row>
          </v-subheader>
          <v-list-item-group v-model="model" mandatory color="primary">
            <v-list-item v-for="(item, index) in configs" :key="index">
              <v-list-item-icon>
                <v-progress-circular :rotate="360" :width="5" :value="getValue(item.compl)" color="teal"> </v-progress-circular>
              </v-list-item-icon>
              <v-list-item-content class=" justify-space-between">
                <v-list-item-title>
                  <v-row no-gutters>
                    <v-col cols="5" class="d-flex align-center"> <span class="label-config">ID :</span> {{ item.num }} </v-col>
                    <v-col cols="5" class="d-flex align-center"> <span class="label-config">NOM :</span> {{ item.name }} </v-col>
                    <v-col cols="1">
                      <v-btn icon color="red" @click="removeConfig(index)">
                        <v-icon>
                          mdi-delete-outline
                        </v-icon>
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-col>
      <v-col cols="9" class="px-5">
        <v-card flat class="mb-15" v-if="this.user.role === 'Utilisateur'">
          <v-row>
            <v-col cols="auto">
              <v-card-title>Station météo</v-card-title>
            </v-col>
            <v-col>
              <v-text-field :value="this.location.station"></v-text-field>
            </v-col>
          </v-row>
          <v-card-text>
            <v-data-table
              :hide-default-footer="true"
              :headers="headers"
              :items="this.sensors"
              sort-by="id"
              loading-text="Loading... Please wait"
            >
              <template v-slot:top>
                <v-toolbar flat>
                  <v-toolbar-title>Liste des compteurs</v-toolbar-title>
                </v-toolbar>
              </template>
            </v-data-table>

            <v-card flat tile class="mt-9">
              <v-row>
                <v-card-title>
                  Configuration générale
                </v-card-title>
              </v-row>
              <v-row class="pl-4">
                <v-col>
                  <v-text-field label="Nombre de silos" :value="this.plant.silo_count"></v-text-field>
                  <v-text-field label="Nombre de chaudières" :value="this.plant.boiler_total"></v-text-field>
                </v-col>
                <v-col>
                  <v-text-field label="Presence d'une cogénération" :value="this.yesOrNo()"></v-text-field>
                  <v-text-field
                    hint="Si cogénération"
                    label="Puissance de la cogénération"
                    suffix="kWh"
                    :value="this.plant.power_coge"
                  ></v-text-field>
                </v-col>
                <v-col>
                  <v-text-field label="Type de pilotage" :value="this.plant.pilot_type"></v-text-field>
                </v-col>
              </v-row>
              <v-row v-for="(silo, index) in this.siloList" :key="index">
                <v-card tile flat class="silo-card my-5 px-5 pb-9">
                  <v-card-title class="pt-5">Silo {{ silo.id }}</v-card-title>
                  <v-row class="mb-6">
                    <v-col cols="6">
                      <v-row class="pl-4">
                        <v-col>
                          <v-text-field label="Densité du bois" suffix="T/m³" :value="silo.wood_dens"></v-text-field>
                          <v-text-field label="PCI du bois" suffix="kWh/T" :value="silo.wood_pci"></v-text-field>
                        </v-col>
                        <v-col>
                          <v-text-field label="Volume du silo" :value="silo.cap" suffix="m³"></v-text-field>
                          <v-text-field label="Objectif de remplissage" suffix="m³" :value="silo.limit_high"></v-text-field>
                        </v-col>
                        <v-col>
                          <v-text-field label="Niveau minimum" suffix="%" :value="silo.limit_low"></v-text-field>
                        </v-col>
                      </v-row>
                    </v-col>
                    <v-col cols="6">
                      <v-card tile flat class="plan-card">
                        <v-card-title class="pb-4 pt-11">
                          Planning par défaut
                        </v-card-title>
                        <v-row class="px-4">
                          <v-col class="pr-4">
                            <v-text-field label="Maximun par demie-journée" suffix="camions" :value="silo.planning.drop_max"></v-text-field>
                            <v-text-field label="Minimun par demie-journée" suffix="camions" :value="silo.planning.drop_min"></v-text-field>
                          </v-col>
                          <v-col>
                            <v-text-field label="Volume moyen par camion" suffix="m³" :value="silo.planning.av"></v-text-field>
                          </v-col>
                        </v-row>
                      </v-card>
                    </v-col>
                  </v-row>

                  <v-card tile flat class="boiler-card pb-5">
                    <v-row>
                      <v-col cols="6" v-for="(boiler, secdex) in silo.boilers" :key="secdex">
                        <v-card flat class="pr-5">
                          <v-card-title> Chaudière {{ boiler.id }} </v-card-title>
                          <v-row class="pl-4">
                            <v-col>
                              <v-text-field label="Charge" suffix="%" :value="boiler.load"></v-text-field>
                            </v-col>
                            <v-col>
                              <v-text-field label="Rendement" suffix="%" :value="boiler.output"></v-text-field>
                            </v-col>
                          </v-row>
                          <v-row class="pl-4">
                            <v-col>
                              <v-text-field label="Puissance minimale" suffix="kW" :value="boiler.load"></v-text-field>
                            </v-col>
                            <v-col>
                              <v-text-field label="Puissance nominale" suffix="kW" :value="boiler.output"></v-text-field>
                            </v-col>
                          </v-row>
                        </v-card>
                      </v-col>
                    </v-row>
                  </v-card>
                </v-card>
              </v-row>
            </v-card>
          </v-card-text>
        </v-card>
        <v-card v-if="this.user.role === 'Administrateur'" height="100%" class="pa-5">
          <v-card-title class="text-h5 font-weight-regular justify-space-between">
            <span class="titre">{{ currentTitle }}</span>
            <v-avatar color="primary lighten-2" class="white--text" size="24" v-text="step" />
          </v-card-title>

          <v-window v-model="step">
            <v-window-item :value="1">
              <v-card-text class="pa-5">
                <v-select
                  :menu-props="{ bottom: true, offsetY: true }"
                  v-model="select"
                  :hint="`H: ${select.id_histo} - P: ${select.id_prev}`"
                  :items="locations"
                  item-text="station"
                  item-value="nom"
                  label="Localisation du site"
                  return-object
                  @change="updateLocation(select)"
                />
              </v-card-text>
            </v-window-item>

            <v-window-item :value="2">
              <v-card-text>
                <v-card outlined elevation="0" class="input-wrapper pa-5 mb-10">
                  <v-text-field persistent-placeholder label="Numéro d'installation Cofely Vision" type="number" counter maxlength="10" />
                  <v-btn outlined color="primary" v-on:click="getSensorOptions()" class="search-btn mb-5">Rechercher</v-btn>
                  <v-select persistent-placeholder label="Compteur"></v-select>
                  <v-select persistent-placeholder class="_unit-select" label="Unité du compteur"></v-select>
                  <v-btn outlined color="primary" v-on:click="addSensor()" class="add-btn">Ajouter</v-btn>
                </v-card>

                <v-data-table
                  :hide-default-footer="true"
                  sort-by="id"
                  loading-text="Loading... Please wait"
                  class="transparent sensor-table rounded-0"
                >
                  <template v-slot:top>
                    <v-toolbar flat outlined class="rounded-1">
                      <v-toolbar-title class="pl-5 text-uppercase light-blue--text">Liste des compteurs</v-toolbar-title>
                    </v-toolbar>
                  </template>

                  <template v-slot:[`item.supprimer`]="{ item }" align="center">
                    <div class="del-btn">
                      <v-icon small @click="removeSensor(item)">mdi-delete</v-icon>
                    </div>
                  </template>
                </v-data-table>
              </v-card-text>
            </v-window-item>

            <v-window-item :value="3">
              <v-card-text>
                <v-card-title>Configuration générale</v-card-title>
                <v-row class="px-9">
                  <v-col>
                    <v-select :menu-props="{ bottom: true, offsetY: true }" :items="this.coge_items" label="Présence cogénération" />
                  </v-col>
                  <v-col>
                    <v-text-field suffix="kWh" label="Puissance cogénération" />
                  </v-col>
                  <v-col>
                    <v-select :menu-props="{ bottom: true, offsetY: true }" label="Type de pilotage" :items="this.type_items" />
                  </v-col>
                  <card>
                    <v-card-title>
                      Priorité d'allumage
                    </v-card-title>
                    <table class="table table-responsive order-table">
                      <thead>
                        <tr>
                          <th v-for="(silo, index) in $store.state.silos" :key="index" :colspan="$store.state.silos[index].boiler_count">
                            Silo {{ index + 1 }}
                          </th>
                        </tr>
                        <tr>
                          <th v-for="index in $store.state.plant.boiler_total" :key="index">Chaudière {{ index }}</th>
                        </tr>
                      </thead>
                      <tbody>
                        <!-- <tr v-if="this.orders">
                          <td v-for="(boiler, index) in orders" :key="index">
                            <select v-model="boiler.order" @change="changePriority({ id: boiler.id, order: boiler.order })">
                              <option v-for="index in $store.state.boilers.length" :key="index" v-bind:value="index"> {{ index }} </option>
                            </select>
                          </td>
                        </tr> -->
                      </tbody>
                    </table>
                  </card>
                </v-row>

                <v-row>
                  <v-row class="pl-4">
                    <v-col>
                      <v-text-field label="Densité du bois" suffix="T/m³"></v-text-field>
                      <v-text-field label="PCI du bois" suffix="kWh/T"></v-text-field>
                    </v-col>
                    <v-col>
                      <v-text-field label="Volume du silo" suffix="m³"></v-text-field>
                      <v-text-field label="Objectif de remplissage" suffix="m³"></v-text-field>
                    </v-col>
                    <v-col>
                      <v-text-field label="Niveau minimum" suffix="%"></v-text-field>
                    </v-col>
                  </v-row>
                  <v-card tile flat class="plan-card">
                    <v-card-title class="pb-4 pt-11">
                      Planning par défaut
                    </v-card-title>
                    <v-row class="px-4">
                      <v-col>
                        <v-text-field label="Maximun par demie-journée" suffix="camions"></v-text-field>
                      </v-col>
                      <v-col>
                        <v-text-field label="Minimun par demie-journée" suffix="camions"></v-text-field>
                      </v-col>
                      <v-col>
                        <v-text-field label="Volume moyen par camion" suffix="m³"></v-text-field>
                      </v-col>
                    </v-row>
                  </v-card>
                </v-row>
                <v-row>
                  <v-row class="pl-4">
                    <v-col>
                      <v-text-field label="Charge" suffix="%"></v-text-field>
                    </v-col>
                    <v-col>
                      <v-text-field label="Rendement" suffix="%"></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row class="pl-4">
                    <v-col>
                      <v-text-field label="Puissance minimale" suffix="kW"></v-text-field>
                    </v-col>
                    <v-col>
                      <v-text-field label="Puissance nominale" suffix="kW"></v-text-field>
                    </v-col>
                  </v-row>
                </v-row>
              </v-card-text>
            </v-window-item>
          </v-window>

          <v-divider></v-divider>

          <v-card-actions>
            <v-btn :disabled="step === 1" text @click="step--">
              précédent
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn :disabled="step === 3" color="primary" depressed @click="step++">
              suivant
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
/* eslint-disable */
import { mapGetters, mapState } from 'vuex';
import store from '../store/index';
let stations = require('../data/station-list');
export default {
  store: store,
  name: 'Profile',
  data() {
    return {
      // search bar related data
      icon: 'mdi-magnify',
      text: 'chercher',
      color: 'primary',
      research: '',

      // user related data
      claims: [],
      auth_time: null,
      exp_time: null,
      verified: null,

      // navigation related data
      model: 0,
      step: 1,

      // meteo view related data
      locations: stations,
      select: {
        station: 'Abbeville (80)',
        id_histo: 7005,
        id_prev: 29592,
        nom: 'abbeville',
      },

      // network view related data
      headers: [
        {
          text: "Numéro d'installation",
          value: 'num',
        },
        {
          text: 'Compteur',
          value: 'name',
        },
        {
          text: 'Unité',
          value: 'unit',
        },
      ],
      number: 3491000900,
      // heating plant related views
      coge_items: ['oui', 'non'],
      type_items: ['Minimum de chaudières', 'Maximum de chaudières'],
      siloList: [],
    };
  },
  methods: {
    chgRole() {
      if (this.user.role === 'Administrateur') store.commit('SET_ROLE', 'Utilisateur');
      else if (this.user.role === 'Utilisateur') store.commit('SET_ROLE', 'Administrateur');
      store.dispatch('updateUser', this.user.id);
    },
    parseDateTime(datetime) {
      if (!datetime) return null;
      const [date, time] = datetime.split(' ');
      const [hour, min, _] = time.split(':');
      return `${date} ${hour}:${min}`;
    },
    yesOrNo() {
      if (this.plant.is_coge === true) return 'Oui';
      if (this.plant.is_coge === false) return 'Non';
    },
    updateLocation(value) {
      this.$store.commit('SET_LOCATION', value);
      this.$store.dispatch('updateLocation', this.config.id);
    },
    async removeConfig(index) {
      const user = this.user.id;
      const config = this.configs[index].id;
      await this.$store.dispatch('remConfig', { user, config });
      this.$store.commit('REM_CONFIG', index);
    },
    searchConfig() {
      if (this.research.length !== 10) {
        this.icon = 'mdi-alert';
        this.text = 'mauvais format';
        this.color = 'error';
      } else {
        const index = this.configs.findIndex((el) => el.num === this.research);
        if (index === -1) {
          this.text = 'introuvable';
          this.icon = 'mdi-information-outline';
          this.color = 'info';
        } else {
          this.model = index;
        }
      }
      console.log(index);
    },
    getValue(compl) {
      switch (compl) {
        case 0:
          return 0;
        case 1:
          return 33;
        case 2:
          return 66;
        case 3:
          return 100;
        default:
          return 0;
      }
    },
    async addConfig() {
      let otherload = {
        name: this.research,
        user: this.user.id,
        role: this.user.role,
      };
      const config = await this.$store.dispatch('addConfig', otherload);
      await this.$store.dispatch('addLocation', config.id);
      await this.$store.dispatch('addHeatingPlant', config.id);
      const silo = await this.$store.dispatch('addSilo', config.id);
      this.$store.commit('INC_SILO_COUNT');
      this.$store.dispatch('updateHeatingPlant', config.id);
      const payload = {
        silo: silo.id,
        plant: config.id,
      };
      await this.$store.dispatch('addBoiler', payload);
      this.$store.commit('INC_BOILER_COUNT', this.indexSiloFromId(silo.id));
      this.$store.commit('INC_BOILER_TOTAL');
      this.$store.dispatch('updateSilo', payload);
      this.$store.dispatch('updateHeatingPlant', config.id);
      await this.$store.dispatch('addDefaultPlanning', silo.id);
    },
    async initClient(client) {
      this.auth_time = new Date(client.auth_time * 1000).toLocaleString('fr');
      this.exp_time = new Date(client.exp * 1000).toLocaleString('fr');
      this.verified = client.email_verified === true ? 'Oui' : 'Non';
      this.claims = await Object.entries(await this.$auth.getUser()).map((entry) => ({ claim: entry[0], value: entry[1] }));
    },
    async initView() {
      if (this.config !== undefined) {
        if (this.user.role === 'Utilisateur') {
          if (this.config.compl > 0) this.initMeteo();
          if (this.config.compl > 1) this.initNetwork();
          if (this.config.compl > 2) this.initPlant();
        }
        if (this.config.compl + 1 !== this.step) {
          this.step = this.config.compl + 1;
        } else {
          switch (this.config.compl) {
            case 0:
              this.initMeteo();
            case 1:
              this.initNetwork();
            case 2:
              this.initPlant();
          }
        }
      }
    },
    async initMeteo() {
      console.log('initializing meteo');
      const location = await this.$store.dispatch('getLocation', this.config.id);
      this.select = location;
    },
    async initNetwork() {
      console.log('initializing network');
      if (this.sensors.length === 0) store.dispatch('getSensorList', this.config.id);
    },
    async initPlant() {
      console.log('initializing heating plant');
      // pass
    },
    fillSiloList() {
      if (this.boilers.length > 0) {
        let silos = this.silos;
        for (let i = 0; i < silos.length; i++) {
          silos[i].planning = this.plannings[i];
          silos[i].boilers = this.boilerListSelected(silos[i].id);
        }
        this.siloList = silos;
      }
    },
    takeAStep(step) {
      console.log(step);
    },
    resetConfig() {
      store.commit('RESET_ALL');
    },
    async setPageApp(id) {
      await this.$store.dispatch('getLocation', id);
      await this.$store.dispatch('getHeatingPlant', id);
      await this.$store.dispatch('getSiloList', id);
      await this.$store.dispatch('getPlanningList', id);
      await this.$store.dispatch('getBoilerList', id);
    },
  },
  created() {
    console.log('--- IN PROFIL ---');
    if (this.client !== null) {
      this.initClient(this.client);
      this.initView();
    }
    this.fillSiloList();
  },
  computed: {
    store() {
      return this.$store.state;
    },
    config() {
      return this.store.configs[this.model];
    },
    currentTitle() {
      switch (this.step) {
        case 1:
          return 'Station météo';
        case 2:
          return 'Demande réseau';
        case 3:
          return 'Données de chaufferie';
      }
    },
    ...mapState(['user', 'configs', 'location', 'sensors', 'plant', 'silos', 'boilers', 'plannings']),
    ...mapGetters({
      client: 'global/user',
      indexSiloFromId: 'indexSiloFromId',
      boilerListSelected: 'boilerListSelected',
    }),
  },
  watch: {
    config() {
      // console.log(this.config);
      // takeAStep(this.config.compl);
    },
    step() {
      if (this.config.compl + 1 !== this.step) {
        store.commit('SET_COMPL', this.step - 1);
        const payload = {
          user: this.user.id,
          config: this.config.id,
        };
        store.dispatch('updateConfig', payload);
      }
      console.log(this.step);
      switch (this.step) {
        case 1:
          this.initMeteo();
          return 'Station météo';
        case 2:
          this.initNetwork();
          return 'Demande réseau';
        case 3:
          this.initPlant();
          return 'Données de chaufferie';
      }
    },
    research() {
      this.icon = 'mdi-magnify';
      this.text = 'chercher';
      this.color = 'primary';
    },
    client(auth, not) {
      if (not !== auth && auth.sub !== null) {
        this.initClient(auth);
        this.initView();
      }
    },
    boilers(next, prev) {
      if (prev.length === 0 && next.length > 0) {
        this.fillSiloList();
      }
    },
  },
};
</script>

<style scoped>
.search-toolbar {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.search-col {
  display: flex;
  justify-content: flex-end;
}

.icon-label {
  letter-spacing: 0.1em !important;
}
.label-config {
  font-weight: bold;
  margin-right: 1em;
}

.titre {
  letter-spacing: 0.05em;
  color: rgb(50, 50, 50);
}

.view-profil {
  height: calc(100vh - 56px);
}

.plant-card,
.plan-card,
.silo-card {
  border-top: lightgrey solid 1px;
}

.boiler-card {
  border: lightgrey solid 1px;
}

.plan-subtitle {
  margin-bottom: 11em !important;
}

.role-col:hover {
  cursor: pointer;
}
</style>
