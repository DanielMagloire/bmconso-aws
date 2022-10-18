/* State module for global information, shared across the app. If a page needs to store specific information, use a module for the given page. */

// Mutations and Actions
import mutations from './mutations';
import actions from './actions';

const user = {
  namespaced: true,
  state: {
    users: [],
    user: {},
  },
  getters: {
    user: (state) => state.user,
    users: (state) => state.users,
    subentication: (state) => state.user.subentication,
    completion: (state) => state.user.completion,
  },
  mutations,
  actions,
};

export default user;
