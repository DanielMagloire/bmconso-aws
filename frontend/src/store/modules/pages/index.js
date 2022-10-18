// Mutations and Actions
import mutations from './mutations';

const pages = {
  namespaced: true,
  state: {
    meteo: {
      cheked: true,
      select: {
        filled: true,
      },
      input: {
        filled: true,
      },
    },
    network: {
      checked: false,
    },
    room: {
      checked: false,
    },
  },
  getters: {
    meteo: (state) => state.meteo,
    network: (state) => state.network,
    room: (state) => state.room,
  },
  mutations,
};

export default pages;
