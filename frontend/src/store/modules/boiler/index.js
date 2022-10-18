/* eslint-disable */
/* State module for global information, shared across the app. If a page needs to store specific information, use a module for the given page. */

// Mutations and Actions
import mutations from './mutations';
import actions from './actions';

const global = {
  namespaced: true,
  state: {
    boiler_index: 0,
    boilers: [],
  },
  getters: {
    siloIndex(rootState) {
      return rootState.silo.silo_index;
    },
    indexFirstBoiler: (state) => (silo_id) => {
      return state.boilers.findIndex((boiler) => boiler.silo_id === silo_id);
    },
    firstBoiler: (state) => (silo_id) => {
      return state.boilers.find((boiler) => boiler.silo_id === silo_id);
    },
    lastIndexBoiler: (state) => (silo_id) => {
      return state.boilers.reverse().findIndex((boiler) => (boiler.silo_id = silo_id));
    },
    boilerList(state, getters, rootState, rootGetters) {
      let silo_id = rootGetters.silo.id;
      return state.boilers.filter((boiler) => boiler.silo_id === silo_id);
    },
    boiler(state, getters, rootState, rootGetters) {
      let boilers = getters.boilerList;
      return boilers[state.boiler_index];
    },
    boilerListSelected: (state) => (id) => {
      return state.boilers.filter((boiler) => boiler.silo_id === id);
    },
    indexBoilerList(state, getters) {
      let index_list = [];
      for (let boiler of getters.boilerList) {
        index_list.push(state.boilers.findIndex(boiler));
      }
      return index_list;
    },
    indexBoilerToAdd: (state) => (silo_id) => {
      let index = state.boilers.length > 0 ? state.boilers.filter((boiler) => boiler.silo_id <= silo_id).length : 0;
      return index;
    },
    boilerFromId: (state) => (id) => {
      return state.boilers.find((boiler) => boiler.id === id);
    },
    indexBoilerFromId: (state) => (id) => {
      return state.boilers.findIndex((boiler) => boiler.id === id);
    },
    priorityList(state) {
      return state.boilers.map(({ id, priority }) => ({ id, priority }));
    },
  },
  mutations,
  actions,
};

export default global;
