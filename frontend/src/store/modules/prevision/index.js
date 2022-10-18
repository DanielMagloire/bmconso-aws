/* State module for global information, shared across the app. If a page needs to store specific information, use a module for the given page. */

// Mutations and Actions
import mutations from './mutations';
import actions from './actions';

const user = {
  namespaced: true,
  state: {
    snapshots: [],
    appros: [],
    woods: [],
    meteos: [],
    demands: [],
  },
  getters: {
    user: (state) => state.user,
    users: (state) => state.users,
    auth_key: (state) => state.user.auth_key,
    compl_lvl: (state) => state.user.compl_lvl,
  },
  mutations,
  actions,
};

export default user;
