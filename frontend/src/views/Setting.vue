<template>
  <div class="view-setup">
    <nav-setup />
    <v-alert
      dense
      type="info"
      dismissible
      transition="slide-y-transition"
      :value="value"
      border="left"
      elevation="1"
      tile
      v-on:input="reset()"
    >
      L'onglet Prévisions est inaccessible avant la fin de la configuration.
    </v-alert>
    <router-view />
  </div>
</template>

<script>
/* eslint-disable */

import NavSetup from '../navigation/SetupNavbar.vue';
import { mapState } from 'vuex';

export default {
  components: {
    NavSetup,
  },
  data() {
    return {
      value: false,
    };
  },
  beforeRouteLeave(to, from, next) {
    console.log(to.name);
    console.log(this.config);
    if ((to.name === 'Historique' || to.name === 'Previsions') && (this.config.compl === undefined || this.config.compl < 2)) {
      this.value = true;
      next(false);
    } else {
      next();
    }
  },
  methods: {
    reset() {
      this.value = false;
    },
    redirectUser() {
      const current_route = this.$router.currentRoute.path;
      const isMeteo = typeof current_route === 'string' ? current_route.includes('station-meteo') : false;
      const isNetwork = typeof current_route === 'string' ? current_route.includes('demande-reseau') : false;
      const isBoiler = typeof current_route === 'string' ? current_route.includes('donnees-chaufferie') : false;
      const isPrevisions = typeof current_route === 'string' ? current_route.includes('previsions') : false;
      if (this.config.compl !== undefined) {
        switch (this.config.compl) {
          case 0:
            if (!isMeteo) {
              console.log('redirecting to meteo');
              this.$router.push('/configuration/station-meteo');
            }
            break;
          case 1:
            if (!isNetwork) {
              console.log('redirecting to network');
              this.$router.push('/configuration/demande-reseau');
            }
            break;
          case 2:
            if (!isBoiler) {
              console.log('redirecting to boiler');
              this.$router.push('/configuration/donnees-chaufferie');
            }
            break;
          case 3:
            if (!isPrevisions) {
              console.log('redirecting to previsions');
              this.$router.push('/previsions');
            }
            break;
        }
      } else {
        if (!isMeteo) {
          console.log('redirecting to meteo');
          this.$router.push('/configuration/station-meteo');
        }
      }
    },
  },
  created() {
    console.log('--- IN CONFIG ---');
  },
  computed: {
    ...mapState(['config']),
  },
  watch: {
    value(val) {
      if (!val) return;
      setTimeout(() => (this.value = false), 5000);
    },
  },
};
</script>

<style scoped>
.v-alert {
  z-index: 100;
  position: absolute;
  min-width: 50%;
  top: 4em;
  left: 3em;
  letter-spacing: 0.03em;
}
</style>
