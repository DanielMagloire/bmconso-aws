export default {
  SET_CHECKBOXES: (state, payload) => {
    state.meteo.cheked = payload.meteo;
    state.network.checked = payload.network;
    state.room.checked = payload.room;
  },
};
