/* eslint-disable */
export default {
  CHG_BOILER(state, boiler_index) {
    state.boiler_index = boiler_index;
  },

  CHG_POW(state, power) {
    state.boilers[power.index].power_nom = power.value;
  },
  CHG_OUT(state, output) {
    state.boilers[output.index].output = output.value;
  },
  CHG_POWMIN(state, power_min) {
    state.boilers[power_min.index].power_min = power_min.value;
  },
  CHG_LOAD(state, load) {
    state.boilers[load.index].load = load.value;
  },
  CHG_PRIORITY(state, given) {
    state.boilers.find((boiler) => boiler.id === given.id).priority = given.priority;
  },

  ADD_BOILER(state, boiler) {
    state.boilers.splice(boiler.index, 0, boiler.data);
  },
  SET_BOILER_LIST(state, boilers) {
    state.boilers = boilers;
  },
  REM_BOILER(state, index) {
    state.boilers.splice(index, 1);
  },
  REM_BOILER_LIST(state, list) {
    state.boilers.splice(list.index, list.length);
  },
  INC_BOILER_COUNT(state, index) {
    state.silos[index].boiler_count++;
  },
  DEC_BOILER_COUNT(state, index) {
    state.silos[index].boiler_count--;
  },
  DEC_BOILER_TOTAL(state) {
    state.room.boiler_total--;
  },
  CHG_BOILER_ORDER(state, details) {
    state.boilers[details.index].priority = details.value;
  },
};
