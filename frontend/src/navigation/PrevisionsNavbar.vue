<template>
  <div class="nav-prev">
    <div v-for="(silo, index) in $store.state.silos" :key="silo.index" class="btn-wrapper">
      <button
        class="silo-link"
        :class="{ active: activeSiloBtn === `silo${index}` }"
        v-on:click="
          isActiveSilo(index);
          changeSelectedSilo(index);
        "
      >
        silo {{ index + 1 }}
      </button>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';
/* eslint-disable */

import store from '../store/index';

export default {
  store: store,
  data() {
    return {
      activeSiloBtn: 'silo0',
    };
  },
  methods: {
    isActiveSilo(index) {
      this.activeSiloBtn = `silo${index}`;
    },
    changeSelectedSilo(index) {
      store.commit('CHG_SILO', index);
    },
  },
  created() {
    this.isActiveSilo(this.silo_index);
    this.changeSelectedSilo(this.silo_index);
  },
  computed: {
    ...mapState(['silo_index']),
    store() {
      return this.$store.state;
    },
  },
};
</script>

<style>
.nav-prev {
  display: flex;
  justify-content: space-between;
  height: 41px;
  transform: translateY(0);
  border-bottom: solid lightgray 3px;
  background-color: #e6e6e6;
}
.nav-prev .btn-wrapper {
  width: 100%;
}

.nav-prev .silo-link {
  display: flex;
  justify-content: center;

  width: 100%;
  border: none;
  border-right: solid lightgray 1px;
  color: #949494;

  line-height: 38px;
  text-decoration: none;
  font-weight: bold;
  letter-spacing: 1px;
  font-size: 150%;
  text-transform: uppercase;

  transition: 0.2s ease color;
  outline: none;
}

.nav-prev .silo-link:hover {
  color: #0af;
}

.nav-prev .silo-link.active {
  border-bottom: solid 3px rgba(0, 170, 255, 0.8);
  background-color: none;
}
</style>
