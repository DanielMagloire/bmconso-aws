/* eslint-disable */
/* State module for global information, shared across the app. If a page needs to store specific information, use a module for the given page. */

// Mutations and Actions
import mutations from './mutations';
import actions from './actions';

const boiler = {
  namespaced: true,
  state: {
    room: {},
  },
  getters: {
    silo_count: (state) => state.room.silo_count,
    boiler_total: (state) => state.room.boiler_total,
    room: (state) => state.room,
  },
  mutations,
  actions,
};

export default boiler;
