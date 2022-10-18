/* State module for global information, shared across the app. If a page needs to store specific information, use a module for the given page. */

// Mutations and Actions
import mutations from './mutations';
import actions from './actions';

const location = {
  namespaced: true,
  state: {
    snapshots: [],
    snapshot: {},
  },
  getters: {
    indexSnapshotFromIdSilo: (state) => (id) => {
      return state.snapshots.findIndex((snap) => snap.id === id);
    },
  },
  mutations,
  actions,
};

export default location;
