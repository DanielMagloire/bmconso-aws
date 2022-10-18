/* eslint-disable */
import http from '@/services/api/internal/client';

export default {
  async getSiloList({ commit }, id) {
    return new Promise((resolve, reject) => {
      http
        .get(`rooms/${id}/silos`)
        .then((response) => {
          commit('SET_SILO_LIST', response.data);
          resolve(response.data);
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  },

  async addSilo({ commit }, id) {
    return new Promise((resolve, reject) => {
      http
        .post(`/rooms/${id}/silos`)
        .then((response) => {
          commit('ADD_SILO', response.data);
          resolve(response.data);
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  },

  async updateSilo({ getters }, payload) {
    return new Promise((resolve, reject) => {
      http
        .put(`/rooms/${payload.room_id}/silos/${payload.silo_id}`, getters.siloFromId(payload.silo_id))
        .then((response) => {
          resolve(response.data);
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  },

  async remSilo(_, id) {
    return new Promise((resolve, reject) => {
      http
        .delete(`/silo/delete?id=${id}`)
        .then((response) => {
          resolve(response.data);
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  },
};
