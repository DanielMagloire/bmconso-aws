<template>
  <div id="nav-setup">
    <router-link to="/configuration/station-meteo"
      >Station météo
      <div class="checkbox">
        <input type="checkbox" id="checkbox-site" :checked="$store.state.meteo_status" />
        <label for="checkbox"></label>
      </div>
    </router-link>
    <router-link to="/configuration/demande-reseau"
      >Demande du réseau
      <div class="checkbox">
        <input type="checkbox" id="checkbox-reseau" :checked="$store.state.network_status" />
        <label for="checkbox"></label>
      </div>
    </router-link>
    <router-link to="/configuration/donnees-chaufferie"
      >Données de chaufferie
      <div class="checkbox">
        <input type="checkbox" id="checkbox-chaufferie" :checked="$store.state.boiler_status" />
        <label for="checkbox"></label>
      </div>
    </router-link>

    <div id="indicator"></div>
  </div>
</template>

<script>
/* eslint-disable */

import store from '../store/index';
export default {
  store: store,
  computed: {
    store() {
      return this.$store.state;
    },
  },
};
</script>

<style>
#nav-setup {
  display: flex;
  justify-content: space-between;

  height: 41px;

  transform: translateY(0);
  border-bottom: solid lightgray 3px;
}

#nav-setup a {
  display: flex;
  justify-content: center;

  width: 33.33%;

  border-right: solid lightgray 1px;
  color: #949494;

  line-height: 38px;
  text-decoration: none;
  text-transform: uppercase;
  font-weight: bold;
  letter-spacing: 1px;
  font-size: 1.2vw;

  transition: 0.2s ease color;
}

#nav-setup a:hover:before,
#nav-setup a:hover:after {
  transform: scale(1);
}

#nav-setup a:nth-child(2).router-link-exact-active ~ #indicator {
  left: 33.333%;
  background: #00aaff;
}

#nav-setup a:nth-child(3).router-link-exact-active ~ #indicator {
  left: 66.666%;
  background: #00aaff;
}

#nav-setup a:nth-child(1):hover ~ #indicator {
  left: 0;
  background: linear-gradient(130deg, yellow, red);
}

#nav-setup a:nth-child(2):hover ~ #indicator {
  left: 33.333%;
  background: linear-gradient(130deg, #00e2ff, #89ff00);
}

#nav-setup a:nth-child(3):hover ~ #indicator {
  left: 66.666%;
  background: linear-gradient(130deg, purple, palevioletred);
}

#indicator {
  position: absolute;
  left: 0;
  bottom: -3px;
  width: 33.333%;
  height: 3px;
  background-color: #00aaff;
  opacity: 0.8;
  border-radius: 5px;
  transition: 0.2s ease left;
}

.checkbox {
  margin-left: 15%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.checkbox label {
  background-color: #fff;
  border: 2px solid #ccc;
  border-radius: 50%;
  cursor: pointer;
  height: 20px;
  width: 20px;
  left: -1;
  position: absolute;
  top: -1;
}

.checkbox label:after {
  border: 2px solid #fff;
  border-top: none;
  border-right: none;
  content: '';
  height: 6px;
  left: 3px;
  opacity: 0;
  position: absolute;
  top: 4px;
  transform: rotate(-45deg);
  width: 10px;
}

.checkbox input[type='checkbox'] {
  visibility: hidden;
}

.checkbox input[type='checkbox']:checked + label {
  background-color: #00aaff;
  border-color: #00aaff;
}

.checkbox input[type='checkbox']:checked + label:after {
  opacity: 1;
}
</style>
