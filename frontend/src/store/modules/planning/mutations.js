/* eslint-disable */
export default {
  CHG_DELIMIN(state, deliveries) {
    state.plannings[state.silo_index].dumper_min = deliveries;
  },
  CHG_DELIMAX(state, deliveries) {
    state.plannings[state.silo_index].dumper_max = deliveries;
  },
  CHG_DELIMED(state, delivery) {
    state.plannings[state.silo_index].average = delivery;
  },

  SET_PLANNING_LIST(state, plannings) {
    state.plannings = plannings;
  },
  SET_PLANNING(state, planning) {
    state.plannings.splice(planning.index, 0, planning.data);
  },
  ADD_PLANNING(state, planning) {
    state.plannings.push(planning);
  },
  REM_PLANNING(state, index) {
    state.plannings.splice(index, 1);
  },
  // LATEST related vues
  SET_LATEST_LIST(state, latests) {
    state.latests = latests;
  },
  SET_LATEST(state, latest) {
    state.latests.splice(latest.index, 0, latest.data);
  },
  REM_LATEST(state) {
    let silo = state.silos[state.silo_index];
    delete silo.latest;
  },
  PUT_LEVEL(state, parsed_value) {
    state.latests[state.silo_index].level = parsed_value;
  },
  PUT_GOAL(state, parsed_value) {
    state.latests[state.silo_index].goal = parsed_value;
  },
};
