/* eslint-disable */
import http from '@/services/api/internal/client';

export default {
  async getBoilerList({ commit }, payload) {
    return new Promise((resolve, reject) => {
      http
        .get(`/rooms/${payload.room_id}/silos/${payload.silo_id}/boilers`)
        .then((response) => {
          console.log(response.data);
          commit('SET_BOILER_LIST', response.data);
          resolve(response.data);
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  },

  async updateBoiler({ getters }, id) {
    return new Promise((resolve, reject) => {
      http
        .put(`/boiler?id=${id}`, getters.boilerFromId(id))
        .then((response) => {
          resolve(response.data);
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  },

  async addBoiler({ commit, getters, state }, payload) {
    return new Promise((resolve, reject) => {
      let boiler = {
        priority: state.boilers.length + 1,
      };
      http
        .post(`/rooms/${payload.room_id}/silos/${payload.silo_id}/boilers`, boiler)
        .then((response) => {
          commit('ADD_BOILER', { index: getters.indexBoilerToAdd(payload.silo_id), data: response.data });
          resolve(response.data);
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  },

  async remBoiler(_, id) {
    return new Promise((resolve, reject) => {
      http
        .delete(`/boiler/delete?id=${id}`)
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
