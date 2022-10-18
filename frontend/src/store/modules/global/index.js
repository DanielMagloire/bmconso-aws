/* State module for global information, shared across the app. If a page needs to store specific information, use a module for the given page. */

// Mutations and Actions
import mutations from './mutations';
import actions from './actions';

const global = {
  namespaced: true,
  state: {
    user: null,
  },
  getters: {
    user: (state) => state.user,
  },
  mutations,
  actions,
};

export default global;
