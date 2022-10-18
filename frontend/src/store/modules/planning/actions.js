/* eslint-disable */
import http from '@/services/api/internal/client';

export default {
  async getPlanningList({ commit }, id) {
    return new Promise((resolve, reject) => {
      http
        .get(`/rooms/${id}/plannings`)
        .then((response) => {
          commit('SET_PLANNING_LIST', response.data);
          resolve(response.data);
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  },
  async addDefaultPlanning({ commit }, silo_id) {
    return new Promise((resolve, reject) => {
      http
        .post(`/silos/${silo_id}/planning`)
        .then((response) => {
          commit('ADD_PLANNING', response.data);
          resolve(response.data);
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  },

  async getDefaultPlanning({ commit }, planning) {
    return new Promise((resolve, reject) => {
      http
        .get(`/planning?silo_id=${planning.silo_id}`)
        .then((response) => {
          commit('SET_PLANNING', { index: planning.index, data: response.data });
          resolve(response.data);
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  },

  async updateDefaultPlanning({ state }) {
    let planning = state.plannings[state.silo_index];
    http
      .put(`/planning?silo_id=${planning.silo_id}`, planning)
      .then((response) => {})
      .catch((error) => {
        console.log(error);
      });
  },

  async remDefaultPlanning({ commit }, silo) {
    return new Promise((resolve, reject) => {
      http
        .delete(`/planning/delete?silo_id=${silo.id}`)
        .then((response) => {
          console.log(response.data);
          commit('REM_PLANNING', silo.index);
          resolve(response.data);
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  },
};
