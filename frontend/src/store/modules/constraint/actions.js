/* eslint-disable */
import http from '@/services/api/internal/client';

export default {
  async getConstraintList({ commit }) {
    return new Promise((resole, reject) => {
      http
        .get(`/constraints?room_id=${localStorage.auth_key}`)
        .then((response) => {
          console.log(response.data);
          commit('SET_CONSTRAINT_LIST', response.data);
          resole(response.data);
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  },
  async addConstraint({ commit, getters }, silo_id) {
    return new Promise((resolve, reject) => {
      http
        .post(`/constraint/add?silo_id=${silo_id}`)
        .then((response) => {
          console.log(response.data);
          commit('ADD_CONSTRAINT', { index: getters.indexConstraintToAdd(silo_id), data: response.data });
          resolve(response.data);
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  },
  async updateConstraint({ getters }, id) {
    return new Promise((resolve, reject) => {
      let constraint = getters.constraintFromId(id);
      http
        .put(`constraint?id=${id}`, constraint)
        .then((response) => {
          console.log(response.data);
          resolve(response.data);
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  },
  async remConstraint({ commit }, id) {
    return new Promise((resolve, reject) => {
      http
        .delete(`/constraint/delete?id=${id}`)
        .then((response) => {
          console.log(response.data);
          commit('REM_CONSTRAINT', id);
          resolve(response.data);
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  },
};
