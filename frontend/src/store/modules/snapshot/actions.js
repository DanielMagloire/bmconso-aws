/* eslint-disable */
import http from '@/services/api/internal/client';

export default {
  async getSnapshotList({ commit }, room_id) {
    return new Promise((resolve, reject) => {
      http
        .get(`/rooms/${room_id}/snapshots`)
        .then((response) => {
          commit('SET_SNAPSHOT_LIST', response.data);
          resolve(response.data);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  async addSnapshot({ commit, getters }, silo_id) {
    return new Promise((resolve, reject) => {
      http
        .post(`/silos/${silo_id}/snapshot`)
        .then((response) => {
          commit('SET_SNAPSHOT', { index: getters.indexSnapshotFromIdSilo(silo_id), data: response.data });
          resolve(response.data);
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  },

  async getSnapshot({ commit }, snapshot) {
    return new Promise((resolve, reject) => {
      http
        .get(`/snapshot?silo_id=${snapshot.silo_id}`)
        .then((response) => {
          commit('SET_SNAPSHOT', { index: snapshot.index, data: response.data });
          resolve(response.data);
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  },

  async updateSnapshot(_, snapshot) {
    http
      .put(`/snapshot?silo_id=${snapshot.silo_id}`, snapshot.state)
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  },

  async remSnapshot({ commit, state }) {
    return new Promise((resolve, reject) => {
      let silo_id = state.silos[state.silo_index].id;
      http
        .delete('/snapshot/delete', {
          params: {
            silo_id: silo_id,
          },
        })
        .then((response) => {
          commit('REM_SNAPSHOT');
          resolve(response.data);
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  },
};
