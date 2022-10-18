/* eslint-disable */
import Vue from 'vue';
import axios from 'axios';

const client = axios.create({
  baseURL: process.env.BASE_URL_INT,
  json: true,
});

client.interceptors.request.use(
  async (config) => {
    const conf = config;
    conf.headers.Authorization = await Vue.prototype.$auth.getIdToken();
    // eslint-disable-next-line
    return conf;
  },
  (error) => Promise.reject(error)
);

export default client;
