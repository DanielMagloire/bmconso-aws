/* eslint-disable */

/* State module for global information, shared across the app. If a page needs to store specific information, use a module for the given page. */

// Mutations and Actions
import mutations from './mutations';
import actions from './actions';

const user = {
  namespaced: true,
  state: {
    plannings: [],
    planning_index: 0,
  },
  getters: {
    planning(state) {
      return state.boilers[state.planning_index];
    },
  },
  mutations,
  actions,
};

export default user;
