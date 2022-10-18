/* State module for global information, shared across the app. If a page needs to store specific information, use a module for the given page. */

// Mutations and Actions
import mutations from './mutations';
import actions from './actions';

const location = {
  namespaced: true,
  state: {
    location: {
      station: 'Abbeville (80)',
      id_histo: 7005,
      id_prev: 29592,
      nom: 'abbeville',
    },
    sensors: [],
  },
  getters: {
    location: (state) => state.location,
    sensors: (state) => state.sensors,
  },
  mutations,
  actions,
};

export default location;
