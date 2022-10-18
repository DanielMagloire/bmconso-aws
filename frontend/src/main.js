// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';

// Import vuetify core framework
// import Vuetify from 'vuetify';
import vuetify from '@/plugins/vuetify'; // path to vuetify export

// Import vuetify css file
// import 'vuetify/dist/vuetify.min.css';

// Import Material design icons
import 'material-design-icons-iconfont/dist/material-design-icons.css';

// Import bmconso dependencies
import Highcharts from 'highcharts';
import exportingInit from 'highcharts/modules/exporting';
import exportDataInit from 'highcharts/modules/export-data';
import stockInit from 'highcharts/modules/stock';
import HighchartsVue from 'highcharts-vue';
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
/* eslint-disable */

// Import router, store and App component
import App from './App';
import store from './store';
import router from './router';

exportingInit(Highcharts);
exportDataInit(Highcharts);
stockInit(Highcharts);

Vue.use(BootstrapVue);
Vue.use(IconsPlugin);
Vue.use(HighchartsVue);

const timezone = new Date().getTimezoneOffset();

Highcharts.setOptions({
  global: {
    timezoneOffset: timezone,
  },
  lang: {
    loading: 'Chargement...',
    months: ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'],
    weekdays: ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'],
    shortMonths: ['jan', 'fév', 'mar', 'avr', 'mai', 'juin', 'juil', 'aoû', 'sep', 'oct', 'nov', 'déc'],
    exportButtonTitle: 'Exporter',
    printButtonTitle: 'Imprimer',
    rangeSelectorFrom: 'Du',
    rangeSelectorTo: 'au',
    rangeSelectorZoom: 'Période',
    downloadPNG: 'Télécharger en PNG',
    downloadJPEG: 'Télécharger en JPEG',
    downloadPDF: 'Télécharger en PDF',
    downloadSVG: 'Télécharger en SVG',
    downloadCSV: 'Télécharger en CSV',
    resetZoom: 'Réinitialiser le zoom',
    resetZoomTitle: 'Réinitialiser le zoom',
    thousandsSep: ' ',
    decimalPoint: ',',
  },
  exporting: {
    buttons: {
      contextButton: {
        menuItems: ['downloadPNG', 'downloadJPEG', 'separator', 'downloadCSV'],
      },
    },
  },
});

Vue.config.productionTip = false;

/* eslint-disable no-new */
export default new Vue({
  el: '#app',
  router,
  store,
  vuetify,
  components: { App },
  template: '<App/>',
});
