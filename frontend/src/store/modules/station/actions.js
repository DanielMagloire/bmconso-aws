/* eslint-disable */
import http from '@/services/api/internal/client';

export default {
  // LOCATION related
  async addLocation({ commit }, id) {
    return new Promise((resolve, reject) => {
      http
        .post(`/locations?id=${id}`)
        .then((response) => {
          commit('SET_LOCATION', response.data);
          resolve(response.data);
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  },

  async getLocationList() {
    return new Promise((resolve, reject) => {
      http
        .get(`/locations`)
        .then((response) => {
          resolve(response.data);
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  },

  async getLocation({ commit }, id) {
    return new Promise((resolve, reject) => {
      http
        .get(`/users/${id}/location`)
        .then((response) => {
          commit('SET_LOCATION', response.data);
          resolve(response.data);
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  },

  async updateLocation({ state }, id) {
    http
      .put(`users/${id}/location`, state.location)
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  },

  async remLocation(_, id) {
    http
      .delete(`/location/delete?id=${id}`)
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  },

  // SENSORS related
};
