/* eslint-disable */
import http from '@/services/api/internal/client';

export default {
  async addBoilerRoom({ commit }, id) {
    return new Promise((resolve, reject) => {
      http
        .post(`/rooms?id=${id}`)
        .then((response) => {
          commit('SET_ROOM', response.data);
          resolve(response.data);
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  },

  async getBoilerRoom({ commit }, id) {
    return new Promise((resolve, reject) => {
      http
        .get(`/users/${id}/room`)
        .then((response) => {
          commit('SET_ROOM', response.data);
          resolve(response.data);
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  },

  async updateBoilerRoom({ state }, id) {
    http
      .put(`/users/${id}/room`, state.room)
      .then((response) => {
        console.log('boiler room');
        console.log(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  },
};
