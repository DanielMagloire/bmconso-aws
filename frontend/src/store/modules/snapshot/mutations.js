/* eslint-disable */
export default {
  SET_SNAPSHOT_LIST(state, snapshots) {
    state.snapshots = snapshots;
  },
  SET_SNAPSHOT(state, latest) {
    state.snapshots.splice(latest.index, 0, latest.data);
  },
  REM_SNAPSHOT(state) {
    let silo = state.silos[state.silo_index];
    delete silo.latest;
  },
  PUT_LEVEL(state, parsed_value) {
    state.snapshots[state.silo_index].level = parsed_value;
  },
  PUT_GOAL(state, parsed_value) {
    state.snapshots[state.silo_index].goal = parsed_value;
  },
};
