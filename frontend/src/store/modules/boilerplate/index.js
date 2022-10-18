import mutations from './mutations';
import actions from './actions';

const boilerplate = {
  namespaced: true,
  state: {
    authenticated: true,
  },
  getters: {
    authenticated: (state) => state.authenticated,
  },
  mutations,
  actions,
};

export default boilerplate;
