/* eslint-disable */
import http from '@/services/api/internal/client';

export default {
  updateSensor(_, sensor) {
    console.log(sensor);
    http
      .put(`/sensor?id=${sensor.id}`, sensor)
      .then((response) => {
        console.log('sensor updated');
        console.log(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  },

  getSensorOptions(_, payload) {
    return new Promise((resolve, reject) => {
      http
        .get(`/sensors/cofely_vision?number=${payload}`, {
          timeout: 100000,
        })
        .then((response) => {
          resolve(response.data);
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  },

  getSensorList({ commit }, id) {
    http
      .get(`users/${id}/sensors`)
      .then((response) => {
        let sensors = response.data;
        if (sensors.length > 0) {
          for (const sensor of sensors) {
            commit('ADD_SENSOR', sensor);
          }
        }
      })
      .catch((error) => {
        console.log(error);
      });
  },

  addSensor({ commit, dispatch, state }, sensor) {
    http
      .post(`users/${sensor.user_id}/sensors`, sensor)
      .then((response) => {
        console.log(response.data);
        commit('ADD_SENSOR', sensor);
      })
      .catch((error) => {
        console.log(error);
      });
  },

  remSensor({ commit }, sensor) {
    http
      .delete(`users/${sensor.user_id}/sensors/${sensor.id}`)
      .then((response) => {
        console.log(response.data);
        commit('REM_SENSOR', sensor.id);
      })
      .catch((error) => {
        console.log(error);
      });
  },
};
