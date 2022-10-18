<template>
  <v-app id="container" v-bind:class="{ hidden: hidden }">
    <c-toolbar></c-toolbar>
    <v-main>
      <v-container text-xs-center v-if="!authenticated">
        <v-layout align-center justify-center row wrap>
          <v-flex xs6>
            <v-alert :value="true" color="error" icon="warning" outline>
              {{ generateMessage('boilerplate.disconnected_message') }}
            </v-alert>
          </v-flex>
        </v-layout>
      </v-container>
      <router-view v-if="authenticated" />
    </v-main>
    <v-fab-transition>
      <v-btn v-scroll="onScroll" v-show="fab" color="red" small fixed bottom right fab @click="toTop">
        <v-icon>keyboard_arrow_up</v-icon>
      </v-btn>
    </v-fab-transition>
  </v-app>
</template>

<script>
/* eslint-disable */
import CToolbar from '@/components/boilerplate/NavBar';
import { mapGetters, mapState } from 'vuex';

export default {
  components: {
    CToolbar,
  },
  data() {
    return {
      fab: false,
      hidden: true,
      compl: 0,
    };
  },
  async created() {
    console.log('--- IN DEFAULT ---');
    try {
      const user = await this.$auth.getUser();
      this.$store.dispatch('global/setUser', user);
    } catch (error) {
      try {
        this.$router.replace({
          name: 'error',
          params: {
            errorCode: error.code ? error.code : JSON.parse(error.xhr.response).error,
            errorMessage: error.message ? error.message : JSON.parse(error.xhr.response).error_description,
          },
        });
      } catch (err) {
        this.$router.replace({
          name: 'error',
          params: {
            errorCode: 'Authentification error',
            errorMessage: 'Authentification error',
          },
        });
      }
    }
  },
  computed: {
    ...mapGetters({ authenticated: 'boilerplate/authenticated' }),
    ...mapGetters({
      client: 'global/user',
      indexSiloFromId: 'indexSiloFromId',
    }),
    ...mapState(['user', 'config', 'location', 'plant', 'silos']),
  },
  watch: {
    client(auth, not) {
      if (not !== auth && auth.sub !== null) {
        this.init(auth);
      }
    },
  },
  methods: {
    onScroll(e) {
      if (typeof window === 'undefined') {
        return;
      }
      const top = window.pageYOffset || e.target.scrollTop || 0;
      this.fab = top > 20;
    },
    toTop() {
      this.$vuetify.goTo(0);
    },

    async init(client) {
      console.log('getting user list');
      const users = await this.$store.dispatch('getUserList');
      let user = users.find((el) => el.sub === client.sub);
      if (user === undefined) {
        console.log('unknown user');
        const payload = {
          sub: client.sub,
          name: client.name,
        };
        user = await this.$store.dispatch('addUser', payload);
        console.log('welcome to the familly ' + client.given_name);
      } else {
        console.log('welcome back ' + client.given_name);
        this.$store.commit('SET_USER', user);
      }
      this.setConfig(user);
      this.redirectUser(user);
    },
    async setPageApp(id) {
      await this.$store.dispatch('getLocation', id);
      await this.$store.dispatch('getHeatingPlant', id);
      await this.$store.dispatch('getSiloList', id);
      await this.$store.dispatch('getPlanningList', id);
      await this.$store.dispatch('getBoilerList', id);
    },
    async setConfig(user) {
      console.log('getting configurations list');
      const configs = await this.$store.dispatch('getConfigList', user.id);
      if (configs.length === 0) {
        console.log('no configuration in list');
      } else {
        this.$store.commit('SET_CONFIG_LIST', configs);
        let config = {};
        if (user.role === 'Administrateur') {
          config = configs[0];
        } else if (user.role === 'Utilisateur') {
          config = configs.find((el) => el.user_id === user.id);
          if (config === undefined) {
            console.log('user has no configuration');
          }
        }
        if (config !== undefined) {
          await this.setPageApp(config.id);
          console.log('configuration data retrieved');
          this.$store.commit('SET_CONFIG', config);
          this.compl = config.compl;
        }
      }
    },
    async redirectUser(user) {
      const current_route = this.$router.currentRoute.path;
      if (user.role === 'Administrateur') {
        const isProfil = typeof current_route === 'string' ? current_route.includes('profil') : false;
        if (!isProfil) {
          console.log('redirecting admin user to profil page');
          this.$router.push('/profil');
        }
      } else if (user.role === 'Utilisateur') {
        const isMeteo = typeof current_route === 'string' ? current_route.includes('station-meteo') : false;
        const isNetwork = typeof current_route === 'string' ? current_route.includes('demande-reseau') : false;
        const isBoiler = typeof current_route === 'string' ? current_route.includes('donnees-chaufferie') : false;
        const isPrevisions = typeof current_route === 'string' ? current_route.includes('previsions') : false;
        switch (this.compl) {
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
          default:
            if (!isMeteo) {
              console.log('redirecting to meteo');
              this.$router.push('/configuration/station-meteo');
            }
            break;
        }
      }
      this.hidden = false;
    },
  },
};
</script>

<style scoped>
.hidden {
  display: none;
}
</style>
