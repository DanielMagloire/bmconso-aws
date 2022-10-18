/* eslint-disable */
/* State module for global information, shared across the app. If a page needs to store specific information, use a module for the given page. */

// Mutations and Actions
import mutations from './mutations';
import actions from './actions';

const global = {
  namespaced: true,
  state: {
    constraints: [],
  },
  getters: {
    indexConstraintToAdd: (state) => (silo_id) => {
      let index = state.constraints.length > 0 ? state.constraints.filter((constraint) => constraint.silo_id <= silo_id).length : 0;
      return index;
    },
    constraintFromId: (state) => (id) => {
      return state.constraints.find((constraint) => constraint.id === id);
    },
  },
  mutations,
  actions,
};

export default global;
