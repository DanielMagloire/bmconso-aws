<template>
  <div id="app">
    <router-view />
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet" />
  </div>
</template>

<script>
import { mapState } from 'vuex';
/* eslint-disable */
export default {
  created() {
    console.log('--- IN APP ---');
  },
  computed: {
    ...mapState(['user', 'config']),
  },
  watch: {
    $route(to, from) {
      console.log('Route changed from ' + from.path + ' to ' + to.path);
      const compl = this.config.compl === undefined ? 0 : this.config.compl;
      if (to.path === '/configuration') {
        switch (compl) {
          case 1:
            console.log('redirecting to network');
            this.$router.push('/configuration/demande-reseau');
            break;
          case 2:
            console.log('redirecting to boiler');
            this.$router.push('/configuration/donnees-chaufferie');
            break;
          case 3:
            console.log('redirecting to boiler');
            this.$router.push('/configuration/donnees-chaufferie');
            break;
          default:
            console.log('redirecting to meteo');
            this.$router.push('/configuration/station-meteo');
            break;
        }
      }
    },
  },
};
</script>

<style>
html {
  overflow-y: auto;
}

* {
  transition: 0.4s;
}

.sortable-chosen * {
  cursor: grabbing !important;
}

.v-toolbar__content {
  padding: 0px !important;
}

.view-setup {
  height: calc(100vh - 56px);
  background-color: #e6e6e6;
}

.view-previsions {
  height: calc(100vh - 56px);
  width: 100%;
  overflow: hidden;
}

.view-historics {
  height: calc(100vh - 56px);
  width: 100%;
  overflow: auto;
}

.view-meteo,
.view-network,
.view-boiler {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 97px);
  width: 100%;
  justify-content: center;
  align-items: center;
}

.view-boiler .v-slider {
  margin-bottom: 0.5em;
}

.view-boiler .v-input__prepend-outer input,
.view-boiler .v-input__append-outer input {
  padding-top: 0px;
}

.view-boiler fieldset fieldset {
  height: 40px;
}

.main-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: calc(100vh - 153px);
  align-items: center;
  justify-content: center;
  background-color: white;
}

.button-container {
  display: flex;
  width: 100%;
  height: 56px;
  padding-right: 1%;
  justify-content: flex-end;
  align-items: center;
  bottom: 0vh;
  border-top: 3px solid lightgray;
}

.button-container button {
  display: block;
  padding-right: 15px;
  padding-left: 15px;
  height: 40px;
  width: 140px;
  text-align: center;
  border-radius: 3px;
  background: #00aaff;
  color: white;
  text-decoration: none;
  font-weight: 500;
  letter-spacing: 1px;
  box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.1);
  border: none;
  margin-right: 1%;
}

/* Chrome, Safari, Edge, Opera */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox */
input[type='number'] {
  -moz-appearance: textfield;
}

.week-end {
  box-shadow: 2px 2px 1px 1px rgba(200, 200, 200, 0.1) inset !important;
  background-color: rgb(156, 156, 156) !important;
  color: rgb(244, 244, 244) !important;
}

.week-end:hover {
  background-color: rgb(244, 244, 244) !important;
  color: black !important;
}

.theme--light.v-toolbar.v-sheet {
  background-color: transparent;
}
</style>
