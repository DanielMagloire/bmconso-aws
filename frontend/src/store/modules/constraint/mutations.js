/* eslint-disable */
export default {
  SET_CONSTRAINT_LIST(state, list) {
    state.constraints = list;
  },
  ADD_CONSTRAINT(state, constraint) {
    state.constraints.splice(constraint.index, 0, constraint.data);
  },
  REM_CONSTRAINT(state, id) {
    let constr_id = state.constraints.findIndex((constraint) => constraint.id === id);
    state.constraints.splice(constr_id, 1);
  },
  PUT_LOAD(state, payload) {
    state.constraints[payload.index].load = payload.value;
  },
  PUT_MIN(state, payload) {
    state.constraints[payload.index].dumper_min = payload.value;
  },
  PUT_MAX(state, payload) {
    state.constraints[payload.index].dumper_max = payload.value;
  },
  PUT_START(state, payload) {
    state.constraints[payload.index].date_start = payload.value;
  },
  PUT_END(state, payload) {
    state.constraints[payload.index].date_end = payload.value;
  },
};
