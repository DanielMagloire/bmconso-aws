/* eslint-disable */
export default {
  CHG_SILO(state, silo_index) {
    state.silo_index = silo_index;
    state.boiler_index = 0;
  },

  CHG_PCI(state, pci) {
    state.silos[state.silo_index].wood_pci = pci;
  },
  CHG_DENS(state, density) {
    state.silos[state.silo_index].wood_density = density;
  },
  CHG_CAP(state, capacity) {
    state.silos[state.silo_index].capacity = capacity;
  },
  CHG_UPLIMIT(state, threshold) {
    state.silos[state.silo_index].threshold_high = threshold;
  },
  CHG_LOWLIMIT(state, threshold) {
    state.silos[state.silo_index].threshold_low = threshold;
  },

  INC_BOILER_COUNT(state, index) {
    state.silos[index].boiler_count++;
  },
  DEC_BOILER_COUNT(state, index) {
    state.silos[index].boiler_count--;
  },

  ADD_SILO(state, silo) {
    state.silos.push(silo);
  },

  SET_SILO_LIST(state, silos) {
    state.silos = silos;
  },

  REM_SILO(state, index) {
    state.silos.splice(index, 1);
  },
};
