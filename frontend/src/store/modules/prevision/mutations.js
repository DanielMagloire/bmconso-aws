/* eslint-disable */
export default {
  ADD_APPRO(state, planning) {
    state.appros.push(planning);
  },
  ADD_WOOD(state, stock) {
    state.woods.push(stock);
  },
  ADD_METEO(state, demand) {
    state.meteos.push(demand);
  },
  ADD_DEMAND(state, prevision) {
    state.demands.push(prevision);
  },
};
