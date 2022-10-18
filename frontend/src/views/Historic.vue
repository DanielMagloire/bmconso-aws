<template>
  <div class="view-historics">
    <v-row no-gutters class="pa-4" v-if="this.hist_humi.length > 0 && this.hist_temp.length > 0">
      <temperature-humidite />
    </v-row>
    <v-row no-gutters class="pa-4" v-if="this.hist_heat.length > 0">
      <chaleur />
    </v-row>
  </div>
</template>

<script>
/* eslint-disable */

import store from '../store/index';
import NavPrevisions from '../navigation/PrevisionsNavbar.vue';
import { mapState } from 'vuex';
import TemperatureHumidite from '../charts/TemperatureHumidite.vue';
import Chaleur from '../charts/Chaleur(HistoriqueDemande).vue';

export default {
  components: {
    NavPrevisions,
    TemperatureHumidite,
    Chaleur,
  },

  store: store,
  data() {
    return {
      loading: true,
    };
  },
  created() {
    if (this.config.compl === 3) this.setupHistorics();
  },
  methods: {
    async setupHistorics() {
      console.log('initializing historics view');
      const payload = {
        user: this.user.id,
        config: this.config.id,
      };
      let historics = await store.dispatch('getHistorics', payload);
      console.log('--- HISTORICS ---');
      let histo_entries = Object.entries(historics);
      console.log(histo_entries);
      //   let histo_filtered = meteo_entries.filter((entry) => entry[0] >= this.year_before);
      let humi_mapped = histo_entries.map((item) => [parseInt(item[0]), item[1]['humi.hist']]);
      let temp_mapped = histo_entries.map((item) => [parseInt(item[0]), item[1]['temp.hist']]);
      let heat_mapped = histo_entries.map((item) => [parseInt(item[0]), item[1]['heat.hist']]);

      store.commit('SET_HUMI_HIST', humi_mapped);
      store.commit('SET_PLANT_HIST', heat_mapped);
      store.commit('SET_TEMP_HIST', temp_mapped);
    },
  },
  computed: {
    store() {
      return this.$store.state;
    },
    ...mapState(['user', 'config', 'hist_humi', 'hist_heat', 'hist_temp']),
  },
};
</script>

<style scoped>
.weather-chart {
  height: 8px !important;
}
</style>
