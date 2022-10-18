<template>
  <div class="view-meteo">
    <div class="main-container">
      <div class="card-container">
        <v-select
          v-model="select"
          :hint="`H: ${select.id_histo} - P: ${select.id_prev}`"
          :items="locationList"
          item-text="station"
          item-value="nom"
          label="Localisation du site"
          return-object
          v-on:change="updateLocation(select)"
        />
        <v-text-field
          persistent-placeholder
          label="Numéro de configuration"
          type="number"
          :hint="hint"
          v-model="value"
          counter
          maxlength="10"
          :rules="rules"
          @focus="$event.target.select()"
        />
      </div>
    </div>
    <div class="button-container">
      <v-dialog v-model="dialog" max-width="375">
        <v-card>
          <v-card-title class="text-h5 info--text">
            Erreur 404 !
          </v-card-title>
          <v-card-text>Numéro de configuration absent ou incorrect. Commencer une nouvelle configuration ?</v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="black" text @click="dialog = false">
              réessayer
            </v-btn>
            <v-btn color="black" text @click="startNewConfig()">
              oui
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-btn depressed color="primary" v-on:click="goToNetwork()">Suivant</v-btn>
    </div>
  </div>
</template>

<script>
/* eslint-disable */

import store from '../store/index';
import { mapGetters, mapState } from 'vuex';

let stations = require('../data/station-list');
export default {
  store: store,

  data() {
    return {
      locationList: stations,
      isDisabledNext: false,
      danger: '',
      warning: '',
      validation: 'is-invalid',
      select: {
        station: 'Abbeville (80)',
        id_histo: 7005,
        id_prev: 29592,
        nom: 'abbeville',
      },
      value: null,
      hint: null,
      rules: [(v) => !!v || '', (v) => (v && v.length <= 10) || ''],
      dialog: false,
    };
  },
  methods: {
    async startNewConfig() {
      const otherload = {
        name: `USR${this.user.id}`,
        user: this.user.id,
        role: this.user.role,
      };
      const config = await this.$store.dispatch('addConfig', otherload);
      this.$store.commit('SET_CONFIG', config);
      await this.$store.dispatch('addLocation', config.id);
      await this.$store.dispatch('addHeatingPlant', config.id);
      this.$store.commit('RESET_SILO_LIST');
      this.$store.commit('RESET_PLANNING_LIST');
      const silo = await this.$store.dispatch('addSilo', config.id);
      this.$store.commit('INC_SILO_COUNT');
      this.$store.dispatch('updateHeatingPlant', config.id);
      const payload = {
        silo: silo.id,
        plant: config.id,
      };
      this.$store.commit('RESET_BOILER_LIST');
      await this.$store.dispatch('addBoiler', payload);
      this.$store.commit('INC_BOILER_COUNT', this.indexSiloFromId(silo.id));
      this.$store.commit('INC_BOILER_TOTAL');
      this.$store.dispatch('updateSilo', payload);
      this.$store.dispatch('updateHeatingPlant', config.id);
      await this.$store.dispatch('addDefaultPlanning', silo.id);
      this.dialog = false;
    },
    setupCheckBoxes() {
      store.commit('CHECK_METEO', false);
      store.commit('CHECK_NETWORK', false);
      store.commit('CHECK_BOILER', false);
    },

    async updateConfig(payload) {
      store.commit('SET_COMPL', payload.commit);
      await store.dispatch('updateConfig', payload.dispatch);
    },
    async setupMeteoView() {
      if (this.location.station !== undefined) {
        this.select = this.location;
      }
      if (this.config.num !== undefined) {
        this.value = this.config.num;
        if (this.config.compl !== 0) {
          const payload = {
            commit: 0,
            dispatch: {
              user: this.user.id,
              config: this.config.id,
            },
          };
          this.updateConfig(payload);
        }
      }
    },
    updateLocation(value) {
      store.commit('SET_LOCATION', value);
      store.dispatch('updateLocation', this.config.id);
    },
    async goToNetwork() {
      let config = this.configs.find((el) => el.num === this.value);
      if (config === undefined) {
        this.dialog = true;
      } else {
        config.user_id = this.user.id;
        this.$store.commit('SET_CONFIG', config);
        console.log(this.config);
        const payload = {
          commit: 1,
          dispatch: {
            user: this.user.id,
            config: this.config.id,
          },
        };
        this.updateConfig(payload);
        this.$router.push('/configuration/demande-reseau');
      }
    },
  },
  created() {
    console.log('--- IN METEO ---');
    this.setupCheckBoxes();
    if (this.config.compl !== undefined) {
      this.setupMeteoView();
    }
  },
  computed: {
    store() {
      return this.$store.state;
    },
    ...mapState(['user', 'location', 'config', 'configs']),
    ...mapGetters({
      client: 'global/user',
      indexSiloFromId: 'indexSiloFromId',
    }),
  },
  watch: {
    config(current) {
      if (current.compl !== undefined) {
        this.setupMeteoView();
      }
    },
    // location(newinput, oldinput) {
    //   if (oldinput !== newinput) {
    //     this.input = newinput;
    //   }
    // },
  },
};
</script>

<style scoped>
.main-container {
  background-color: white;
}
.card-container {
  padding: 20px 50px 50px;
  border-radius: 0px;
  max-width: 400px;
}

.v-input {
  width: 20em;
  margin: 2em;
}
</style>
