/* eslint-disable */
export default {
  ADD_SENSOR(state, sensor) {
    state.sensors.push(sensor);
  },
  REM_SENSOR(state, index) {
    state.sensors.splice(index, 1);
  },
  REM_SENSOR_OPTS(state, index) {
    state.sensor_options.splice(index, 1);
  },
  REM_SENSOR_STATUS(state, index) {
    state.sensor_statuses.splice(index, 1);
  },
  SET_SENSOR_IDX(state, index) {
    state.sensor_idx = index;
  },
  SET_SENSOR_INUM(state, payload) {
    state.sensors[payload.index].instl_num = payload.instl_num;
  },
  SET_SENSOR_NAME(state, payload) {
    state.sensors[payload.index].name = payload.name;
  },
  SET_SENSOR_OPTS(state, burden) {
    let array = [];
    for (const option of burden.options) {
      array.push(option);
    }
    state.sensor_options.splice(burden.index, 1, array);
  },
  SET_SENSOR_STATUS(state, cargo) {
    state.sensor_statuses.splice(cargo.index, 1, cargo.value);
  },
};
