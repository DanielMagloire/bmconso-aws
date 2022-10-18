/* eslint-disable */

import '@mdi/font/css/materialdesignicons.css';
import Vue from 'vue';
import Vuetify from 'vuetify';
import 'vuetify/dist/vuetify.min.css';
import BoilerIcon from '../icons/boiler.vue';
import CogenerationIcon from '../icons/cogeneration.vue';
import DeliveryIcon from '../icons/delivery.vue';
import SiloIcon from '../icons/silo.vue';
import WoodIcon from '../icons/wood.vue';
// import colors from 'vuetify/lib/util/colors';

// Definition of the theme colors
const lightColors = {
  primary: '#008CD0' /* indigo */,
  secondary: '#005288' /* bleu  */,
  accent: '#003b70' /* deep orange */,
  error: '#F44336' /* rouge */,
  info: '#00BCD4' /* cyan */,
  success: '#4CAF50' /* vert */,
  warning: '#FF9800' /* orange */,
};

const darkColors = {
  primary: '#008CD0' /* indigo */,
  secondary: '#005288' /* bleu  */,
  accent: '#003b70' /* deep orange */,
  error: '#F44336' /* rouge */,
  info: '#00BCD4' /* cyan */,
  success: '#4CAF50' /* vert */,
  warning: '#FF9800' /* orange */,
};

Vue.use(Vuetify);

const opts = {
  icons: {
    iconfont: 'mdi', // default - only for display purposes
    values: {
      boiler: {
        component: BoilerIcon, // you can use string here if component is registered globally
        props: {
          // pass props to your component if needed
          name: 'boiler-icon',
        },
      },
      cogeneration: {
        component: CogenerationIcon, // you can use string here if component is registered globally
        props: {
          // pass props to your component if needed
          name: 'cogeneration-icon',
        },
      },
      delivery: {
        component: DeliveryIcon, // you can use string here if component is registered globally
        props: {
          // pass props to your component if needed
          name: 'delivery-icon',
        },
      },
      silo: {
        component: SiloIcon, // you can use string here if component is registered globally
        props: {
          // pass props to your component if needed
          name: 'silo-icon',
        },
      },
      wood: {
        component: WoodIcon, // you can use string here if component is registered globally
        props: {
          // pass props to your component if needed
          name: 'Wood-icon',
        },
      },
    },
  },
  // theme: colors,
  theme: {
    themes: {
      light: lightColors,
      dark: darkColors,
    },
  },
};

export default new Vuetify(opts);

/* {
  theme: {
    themes: {
      light: colors,
      dark: colors,
    }
  }
} */
