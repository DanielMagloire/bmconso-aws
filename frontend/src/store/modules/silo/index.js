/* eslint-disable */
/* State module for global information, shared across the app. If a page needs to store specific information, use a module for the given page. */

// Mutations and Actions
import mutations from './mutations';
import actions from './actions';

const user = {
  namespaced: true,
  state: {
    silo_index: 0,
    silos: [],
  },
  getters: {
    silo(state) {
      return state.silos[state.silo_index];
    },
    // watched for update
    boilerCountList(state) {
      return state.silos.map(({ id, boiler_count }) => ({ id, boiler_count }));
    },
    // for action purposes
    indexSiloFromId: (state) => (id) => {
      return state.silos.findIndex((silo) => silo.id === id);
    },
    siloFromId: (state) => (id) => {
      return state.silos.find((silo) => silo.id === id);
    },
    silos: (state) => state.silos,
  },
  mutations,
  actions,
};

export default user;
