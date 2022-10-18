/* eslint-disable */
export default {
  SET_ROOM(state, room) {
    state.room = room;
  },
  SET_ID_USER(state, id) {
    state.room.auth_key = id;
  },
  CHG_BOILER_TOTAL(state, total) {
    state.room.boiler_total = total;
  },

  INC_BOILER_TOTAL(state) {
    state.room.boiler_total++;
  },

  SET_SILO_LIST(state, silos) {
    state.silos = silos;
  },
  INC_SILO_COUNT(state) {
    state.room.silo_count++;
  },

  DEC_SILO_COUNT(state) {
    state.room.silo_count--;
  },

  CHG_OTHEROUT(state, output) {
    state.room.power_coge = output;
  },
  INC_SILO_COUNT(state) {
    state.room.silo_count++;
  },

  DEC_SILO_COUNT(state) {
    state.room.silo_count--;
  },
};
