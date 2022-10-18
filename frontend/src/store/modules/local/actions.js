/* eslint-disable */
import http from '@/services/api/internal/client';

export default {
  async getUserList() {
    return new Promise((resolve, reject) => {
      http
        .get('/users')
        .then((response) => {
          resolve(response.data);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },

  async getUser({ commit }, id) {
    console.log('retrieving user');
    return new Promise((resolve, reject) => {
      http
        .get(`/users/${id}`)
        .then((response) => {
          console.log(response.data);
          commit('SET_USER', response.data);
          resolve(response.data);
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  },

  async addUser({ commit }, subentication) {
    console.log('adding user');
    return new Promise((resolve, reject) => {
      let user = {
        subentication: subentication,
      };
      http
        .post('/users', user)
        .then((response) => {
          console.log(response.data);
          commit('SET_USER', response.data);
          resolve(response.data);
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  },

  async updateUser({ state }, id) {
    return new Promise((resolve, reject) => {
      http
        .put(`/users/${id}`, state.user)
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

  async remUser({ commit }, subentication) {
    console.log('removing user');
    const id = state.users.find((el) => el.subentication === subentication).id;
    http
      .delete(`/users/${id}`)
      .then((response) => {
        console.log(response.data);
        commit('REM_USER', response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  },
};
