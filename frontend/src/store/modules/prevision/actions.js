/* eslint-disable */
import http from '@/services/api/internal/client';

export default {
  async getPrevisions() {
    return new Promise((resolve, reject) => {
      http
        .get(`/prev?user_id=${localStorage.auth_key}`)
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
  async getStockBiomasse(_, refresh) {
    return new Promise((resolve, reject) => {
      let params = {
        user_id: localStorage.auth_key,
      };
      if (refresh === true) {
        params.refresh = refresh;
      }
      http
        .get('/appro', {
          timeout: 100000,
          params: params,
        })
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
  async getBesoinBiomasse(_, refresh) {
    return new Promise((resolve, reject) => {
      let params = {
        user_id: localStorage.auth_key,
      };
      if (refresh === true) {
        params.refresh = refresh;
      }
      http
        .get('/stock', {
          timeout: 100000,
          params: params,
        })
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
  async getPrevisionDemande(_, refresh) {
    return new Promise((resolve, reject) => {
      let params = {
        user_id: localStorage.auth_key,
      };
      if (refresh === true) {
        params.refresh = refresh;
      }
      http
        .get('/demand', {
          timeout: 100000,
          params: params,
        })
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

  async getPrevisionMeteo(_, refresh) {
    return new Promise((resolve, reject) => {
      let params = {
        user_id: localStorage.auth_key,
      };
      if (refresh === true) {
        params.refresh = refresh;
      }
      http
        .get('/meteo', {
          timeout: 100000,
          params: params,
        })
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
};
