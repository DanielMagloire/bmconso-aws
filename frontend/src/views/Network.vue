<template>
  <div class="view-network">
    <v-alert
      dense
      :type="type"
      dismissible
      transition="slide-y-transition"
      :value="value"
      border="left"
      elevation="1"
      tile
      v-on:input="reset()"
      colored-border
    >
      {{ alert }}
    </v-alert>
    <div class="main-container">
      <v-card class="input-wrapper transparent elevation-0 rounded-0">
        <v-form class="search-wrapper">
          <v-text-field
            persistent-placeholder
            :loading="loading"
            label="Numéro d'installation Cofely Vision"
            type="number"
            v-model="number"
            counter
            maxlength="10"
            :rules="rules"
          />
          <v-btn :disabled="!isValid" outlined color="primary" v-on:click="getSensorOptions()" class="search-btn">Rechercher</v-btn>
        </v-form>
        <div class="options-wrapper">
          <v-select persistent-placeholder v-model="option" :items="options" label="Compteur"></v-select>
          <v-select persistent-placeholder class="_unit-select" v-model="unit" :items="units" label="Unité du compteur"></v-select>
          <v-btn outlined color="primary" v-on:click="addSensor()" class="add-btn">Ajouter</v-btn>
        </div>
      </v-card>
      <v-divider vertical></v-divider>
      <div class="table-wrapper">
        <v-data-table
          :hide-default-footer="true"
          :headers="headers"
          :items="this.sensors"
          sort-by="id"
          loading-text="Loading... Please wait"
          class="transparent sensor-table rounded-0"
        >
          <template v-slot:top>
            <v-toolbar flat class="transparent grey lighten-2 elevation-1">
              <v-toolbar-title class="tool-title text-uppercase light-blue--text">Liste des compteurs</v-toolbar-title>
            </v-toolbar>
          </template>

          <template v-slot:[`item.supprimer`]="{ item }" align="center">
            <div class="del-btn">
              <v-icon small @click="removeSensor(item)">mdi-delete</v-icon>
            </div>
          </template>
        </v-data-table>
      </div>
    </div>
    <div class="button-container">
      <v-btn depressed color="primary" @click="goToLocation()">Précédent</v-btn>
      <v-btn depressed color="primary" @click="goToHeatingPlant()">Suivant</v-btn>
    </div>
  </div>
</template>

<script>
/* eslint-disable */

import { mapState } from 'vuex';
import store from '../store/index';

export default {
  store: store,
  data() {
    return {
      type: 'info',
      alert: '',
      value: false,
      rules: [(v) => !!v || '', (v) => (v && v.length <= 10) || ''],
      number: 3491000900,
      loading: false,
      unit: null,
      units: ['W', 'Wh', 'kW', 'kWh', 'MW', 'MWh', 'GW', 'GWh'],
      option: null,
      options: [],
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
        { text: 'Actions', value: 'supprimer', sortable: false },
      ],
    };
  },
  created() {
    this.setupCheckBoxes();
    if (this.config.num !== undefined) {
      this.setupNetworkView();
    }
  },

  methods: {
    reset() {
      this.value = false;
      // store.commit('SET_ERROR', false)
    },
    // when created
    setupCheckBoxes() {
      store.commit('CHECK_METEO', true);
      store.commit('CHECK_NETWORK', false);
      store.commit('CHECK_BOILER', false);
    },
    setupNetworkView() {
      if (this.config.compl !== 1) {
        const payload = {
          commit: 1,
          dispatch: {
            user: this.user.id,
            config: this.config.id,
          },
        };
        this.updateConfig(payload);
      }
      if (this.sensors.length === 0) {
        this.getSensorList();
      }
    },
    async getSensorOptions() {
      if (!this.loading) this.loading = true;
      const options = await store.dispatch('getSensorOptions', this.number);
      this.options = options;
      this.option = options[0];
      this.unit = 'W';
      if (this.loading) this.loading = false;
    },
    getSensorList() {
      store.dispatch('getSensorList', this.config.id);
    },
    async updateConfig(payload) {
      store.commit('SET_COMPL', payload.commit);
      await store.dispatch('updateConfig', payload.dispatch);
    },

    // dispatches
    setSensorInum(payload) {
      this.danger = '';
      this.warning = '';
      store.dispatch('getSensorOptions', payload);
    },
    updateSensor(index) {
      let sensor = this.sensors[index];
      payload = {
        config: config.id,
        sensor: sensor.id,
        state: sensor,
      };
      store.dispatch('updateSensor', payload);
    },
    //buttons commands
    addSensor() {
      this.danger = '';
      this.warning = '';
      const sensor = {
        config_id: this.config.id,
        num: this.number,
        name: this.option,
        unit: this.unit,
      };
      store.dispatch('addSensor', sensor);
    },
    removeSensor(sensor) {
      console.log(sensor);
      store.dispatch('remSensor', sensor);
    },

    //buttons commands
    goToLocation() {
      this.$router.push('/configuration/station-meteo');
    },
    goToHeatingPlant() {
      if (this.sensors.length === 0) {
        this.alert = 'Liste des capteurs vide !';
        this.type = 'warning';
        this.value = true;
      } else {
        const payload = {
          commit: 2,
          dispatch: {
            user: this.user.id,
            config: this.config.id,
          },
        };
        this.updateConfig(payload);
        this.$router.push('/configuration/donnees-chaufferie');
      }
    },
  },

  computed: {
    ...mapState(['sensors', 'user', 'error', 'config']),
    isValid() {
      if (this.number !== null) {
        if (this.number.length === 10) {
          return true;
        }
      }
      return false;
    },
  },
  watch: {
    value(val) {
      if (!val) return;
      setTimeout(() => (this.value = false), 5000);
    },
    error(val) {
      if (val === true) {
        this.loading = false;
        this.alert = "Numéro d'installation invalide.";
        this.type = 'error';
        this.value = true;
      }
    },
    config(current) {
      if (current.num !== undefined) {
        this.setupNetworkView();
      }
    },
    loading(val) {
      if (!val) return;
      setTimeout(() => (this.loading = false), 10000);
    },
  },
};
</script>

<style scoped>
.main-container {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
  width: 100%;
}

.input-wrapper {
  flex-direction: column;
  margin: 2em;
  width: 18em;
  padding-top: 1em;
  padding-left: 2em;
  padding-right: 2em;
  padding-bottom: 2em;
  height: calc(100% - 97px);
}

.options-wrapper,
.search-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.table-wrapper {
  overflow: auto;
  display: flex;
  justify-content: center;
  flex-grow: 1;
  background-color: white;
  height: 100%;
}

.sensor-table {
  margin: 2em;
  max-width: 58em;
  height: calc(100% - 97px);
  width: 100%;
}

.search-btn,
.add-btn {
  font-weight: bold;
  margin-bottom: 1.5em;
}

.search-btn {
  margin-top: 1.5em;
}

.view-network {
  flex-direction: column;
}
.del-btn {
  padding-left: 1em;
}

.tool-title {
  padding: 1em;
  letter-spacing: 0.1em;
}

.v-alert {
  z-index: 100;
  position: absolute;
  min-width: 50%;
  top: 4em;
  left: 3em;
  letter-spacing: 0.03em;
}
</style>
