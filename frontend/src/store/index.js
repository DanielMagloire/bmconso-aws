/* eslint-disable */
import Vue from 'vue';
import Vuex from 'vuex';
import boilerplate from './modules/boilerplate';
import global from './modules/global';
import http from '@/services/api/internal/client';
import Qs from 'qs';

Vue.use(Vuex);

const store = new Vuex.Store({
  strict: true,
  modules: {
    boilerplate,
    global,
  },

  state: {
    error: false,
    error_message: '',
    loading: false,
    // CHECKBOXES related states
    meteo_status: false,
    network_status: false,
    boiler_status: false,
    // SENSORS related state
    sensors: [],
    sensor_options: [],
    sensor_statuses: [],
    // SILOS related states
    silo_index: 0,
    silos: [],
    plannings: [],
    // BOILERS related states
    boiler_index: 0,
    boilers: [],
    // USER related states
    users: [],
    user: {},
    // CONFIG related states
    configs: [],
    config: {},
    // LOCATION related states
    locations: [],
    location: {},
    plants: [],
    plant: {},
    // CONSTRAINT related state
    rules: [],
    loads: [],

    //PREVISION related state
    snapshots: [],
    appros: [],
    woods: [],
    meteos: [],
    demands: [],

    // HISTORICS
    hist_humi: [],
    hist_heat: [],
    hist_temp: [],
  },
  mutations: {
    // USER related mutations
    SET_USER_LIST(state, users) {
      state.users = users;
    },
    SET_USER(state, user) {
      state.user = user;
    },
    SET_AUTH(state, sub) {
      state.user.sub = sub;
    },
    SET_ROLE(state, role) {
      state.user.role = role;
    },
    ADD_USER(state, user) {
      state.users.push(user.sub);
    },
    REM_USER(state, user) {
      let index = state.users.indexOf(user);
      state.users.splice(index, 1);
    },

    // CONFIG related mutations
    SET_CONFIG_LIST(state, configs) {
      state.configs = configs;
    },
    SET_COMPL(state, compl) {
      state.config.compl = compl;
    },
    SET_CONFIG(state, config) {
      state.config = config;
    },
    ADD_CONFIG(state, config) {
      state.configs.push(config);
    },
    REM_CONFIG(state, index) {
      state.configs.splice(index, 1);
    },
    // LOCATION related mutations
    SET_LOCATION_LIST(state, locations) {
      state.locations = locations;
    },
    SET_LOCATION(state, location) {
      state.location = location;
    },

    // HEATING PLANT related muitations
    SET_PLANT_LIST(state, plants) {
      state.plants = plants;
    },
    SET_PLANT(state, plant) {
      state.plant = plant;
    },
    SET_ID_USER(state, id) {
      state.plant.sub = id;
    },
    CHG_BOILER_TOTAL(state, total) {
      state.plant.boiler_total = total;
    },

    INC_BOILER_TOTAL(state) {
      state.plant.boiler_total++;
    },
    CHG_IS_COGE(state, is_coge) {
      state.plant.is_coge = is_coge;
    },
    //  ROOM NAVIGATION
    CHG_SILO(state, silo_index) {
      state.silo_index = silo_index;
      state.boiler_index = 0;
    },
    CHG_BOILER(state, boiler_index) {
      state.boiler_index = boiler_index;
    },

    // SILO UPDATE
    CHG_PCI(state, pci) {
      state.silos[state.silo_index].wood_pci = pci;
    },
    CHG_DENS(state, dens) {
      state.silos[state.silo_index].wood_dens = dens;
    },
    CHG_CAP(state, cap) {
      state.silos[state.silo_index].cap = cap;
    },
    CHG_UPLIMIT(state, limit) {
      state.silos[state.silo_index].limit_high = limit;
    },
    CHG_LOWLIMIT(state, limit) {
      state.silos[state.silo_index].limit_low = limit;
    },
    CHG_OTHEROUT(state, output) {
      state.plant.power_coge = output;
    },

    // PLANNING related mutations
    CHG_DELIMIN(state, deliveries) {
      state.plannings[state.silo_index].drop_min = deliveries;
    },
    CHG_DELIMAX(state, deliveries) {
      state.plannings[state.silo_index].drop_max = deliveries;
    },
    CHG_DELIMED(state, delivery) {
      state.plannings[state.silo_index].av = delivery;
    },

    // BOILER related mutations
    CHG_POW(state, power) {
      state.boilers[power.index].power_nom = power.value;
    },
    CHG_OUT(state, output) {
      state.boilers[output.index].output = output.value;
    },
    CHG_POWMIN(state, power_min) {
      state.boilers[power_min.index].power_min = power_min.value;
    },
    CHG_LOAD(state, load) {
      state.boilers[load.index].load = load.value;
    },
    CHG_PRIORITY(state, given) {
      state.boilers.find((boiler) => boiler.id === given.id).order = given.order;
    },

    // SILO related mutations
    ADD_SILO(state, silo) {
      state.silos.push(silo);
    },

    SET_SILO_LIST(state, silos) {
      state.silos = silos;
    },
    INC_SILO_COUNT(state) {
      state.plant.silo_count++;
    },

    DEC_SILO_COUNT(state) {
      state.plant.silo_count--;
    },

    REM_SILO(state, id) {
      const index = state.silos.findIndex((silo) => silo.id === id);
      state.silos.splice(index, 1);
    },

    // BOILERS related mutations
    ADD_BOILER(state, boiler) {
      state.boilers.splice(boiler.index, 0, boiler.data);
    },
    SET_BOILER_LIST(state, boilers) {
      state.boilers = boilers;
    },
    REM_BOILER(state, index) {
      state.boilers.splice(index, 1);
    },
    REM_BOILER_LIST(state, list) {
      state.boilers.splice(list.index, list.length);
    },
    INC_BOILER_COUNT(state, index) {
      state.silos[index].boiler_count++;
    },
    DEC_BOILER_COUNT(state, index) {
      state.silos[index].boiler_count--;
    },
    DEC_BOILER_TOTAL(state) {
      state.plant.boiler_total--;
    },
    CHG_BOILER_ORDER(state, boiler) {
      state.boilers[boiler.index].order = boiler.order;
    },

    // PLANNING related mutations
    SET_PLANNING_LIST(state, plannings) {
      state.plannings = plannings;
    },
    SET_PLANNING(state, planning) {
      state.plannings.splice(planning.index, 0, planning.data);
    },
    ADD_PLANNING(state, planning) {
      state.plannings.push(planning);
    },
    REM_PLANNING(state, id) {
      const index = state.plannings.findIndex((planning) => planning.silo_id === id);
      state.plannings.splice(index, 1);
    },
    // LATEST related vues
    SET_SNAPSHOT_LIST(state, snapshots) {
      state.snapshots = snapshots;
    },
    SET_SNAPSHOT(state, latest) {
      state.snapshots.splice(latest.index, 0, latest.data);
    },
    REM_SNAPSHOT(state) {
      let silo = state.silos[state.silo_index];
      delete silo.latest;
    },
    UPD_SNAPSHOT(state, snapshot) {
      state.snapshots.splice(state.silo_index, 1, snapshot);
    },
    PUT_LEVEL(state, parsed_value) {
      state.snapshots[state.silo_index].level = parsed_value;
    },
    PUT_LEVEL_UNIT(state, value) {
      state.snapshots[state.silo_index].level_unit = value;
    },
    PUT_GOAL(state, parsed_value) {
      state.snapshots[state.silo_index].goal = parsed_value;
    },
    // SENSORS related mutations
    ADD_SENSOR(state, sensor) {
      state.sensors.push(sensor);
    },
    REM_SENSOR(state, index) {
      state.sensors.splice(index, 1);
    },
    REM_SENSOR_OPTS(state, index) {
      state.sensor_options.splice(index, 1);
    },
    REM_SENSOR_STATUS(state, index) {
      state.sensor_statuses.splice(index, 1);
    },
    SET_SENSOR_IDX(state, index) {
      state.sensor_idx = index;
    },
    SET_SENSOR_INUM(state, payload) {
      state.sensors[payload.index].instl_num = payload.instl_num;
    },
    SET_SENSOR_NAME(state, payload) {
      state.sensors[payload.index].name = payload.name;
    },
    SET_SENSOR_OPTS(state, burden) {
      let array = [];
      for (let option of burden.options) {
        array.push(option);
      }
      state.sensor_options.splice(burden.index, 1, array);
    },
    SET_SENSOR_STATUS(state, cargo) {
      state.sensor_statuses.splice(cargo.index, 1, cargo.value);
    },

    // CONSTRAINT related mutations
    SET_CONSTRAINT_LIST(state, list) {
      state.rules = list;
    },
    ADD_CONSTRAINT(state, rule) {
      state.rules.push(rule);
    },
    PUT_CONSTRAINT(state, data) {
      let rule_index = state.rules.findIndex((rule) => rule.id === data.id);
      Object.assign(state.rules[rule_index], data);
    },
    REM_CONSTRAINT(state, id) {
      let index = state.rules.findIndex((rule) => rule.id === id);
      state.rules.splice(index, 1);
    },

    // LOAD related mutations
    SET_LOAD_LIST(state, list) {
      state.loads = list;
    },
    ADD_LOAD(state, payload) {
      state.loads.push(payload);
    },
    PUT_LOAD(state, payload) {
      state.loads[payload.index].value = payload.value;
    },
    REM_LOAD(state, index) {
      state.loads.splice(index, 1);
    },

    // CONSTRAINT related values
    PUT_INDEX(state, rule) {
      state.rules[rule.found_index].index = rule.given_index;
    },
    PUT_MIN(state, payload) {
      state.rules[payload.index].drop_min = payload.value;
    },
    PUT_MAX(state, payload) {
      state.rules[payload.index].drop_max = payload.value;
    },
    PUT_START(state, payload) {
      state.rules[payload.index].date_start = payload.value;
    },
    PUT_END(state, payload) {
      state.rules[payload.index].date_end = payload.value;
    },

    // PREVISIONS related vues
    ADD_APPRO(state, payload) {
      state.appros[payload.silo][payload.date] = payload.planning;
    },
    ADD_WOOD(state, stock) {
      state.woods.push(stock);
    },
    RESET_WOOD(state) {
      state.woods = [];
    },
    ADD_METEO(state, demand) {
      state.meteos.push(demand);
    },
    ADD_DEMAND(state, prevision) {
      state.demands.push(prevision);
    },

    SET_APPRO(state, plannings) {
      state.appros = plannings;
    },
    SET_WOOD(state, stock) {
      state.woods = stock;
    },
    SET_METEO(state, demand) {
      state.meteos = demand;
    },
    SET_DEMAND(state, prevision) {
      state.demands = prevision;
    },

    // HISTORICS
    SET_HUMI_HIST(state, hist_humi) {
      state.hist_humi = hist_humi;
    },
    SET_PLANT_HIST(state, hist_heat) {
      state.hist_heat = hist_heat;
    },
    SET_TEMP_HIST(state, hist_temp) {
      state.hist_temp = hist_temp;
    },

    // change chekboxes status
    CHECK_METEO(state, meteo_status) {
      state.meteo_status = meteo_status;
    },
    CHECK_NETWORK(state, network_status) {
      state.network_status = network_status;
    },
    CHECK_BOILER(state, boiler_status) {
      state.boiler_status = boiler_status;
    },

    SET_ERROR_MESSAGE(state, error) {
      state.error_message = error;
    },
    SET_ERROR(state, error) {
      state.error = error;
    },

    RESET_SILO_LIST(state) {
      state.silos = [];
    },
    RESET_BOILER_LIST(state) {
      state.boilers = [];
    },
    RESET_PLANNING_LIST(state) {
      state.plannings = [];
      state.snapshots = [];
    },
  },
  actions: {
    // USER related actions
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

    async addUser({ commit }, payload) {
      return new Promise((resolve, reject) => {
        let user = {
          sub: payload.sub,
          name: payload.name,
        };
        http
          .post('/users', user)
          .then((response) => {
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

    async remUser({ commit }, sub) {
      console.log('removing user');
      const id = state.users.find((el) => el.sub === sub).id;
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

    // CONFIGURATION related mutations
    async getConfigList() {
      return new Promise((resolve, reject) => {
        http
          .get(`/configurations`)
          .then((response) => {
            // console.log(response.data);
            resolve(response.data);
          })
          .catch((error) => {
            console.log(error);
            reject(error);
          });
      });
    },
    async addConfig({ commit }, params) {
      console.log(params);
      return new Promise((resolve, reject) => {
        http
          .post(`/configurations`, {
            params: params,
            // paramsSerializer: function (params) {
            //   return Qs.stringify(params, {arrayFormat: 'brackets'})
            // },
            // headers: {
            //   "Content-Type": "application/x-www-form-urlencoded",
            //   Accept: "application/json",
            // },
            // transformRequest: [
            //   function(params) {
            //     return Qs.stringify(params);
            //   },
            // ],
          })
          .then((response) => {
            commit('ADD_CONFIG', response.data);
            resolve(response.data);
          })
          .catch((error) => {
            console.log(error);
            reject(error);
          });
      });
    },

    async updateConfig({ state }, payload) {
      http
        .put(`/users/${payload.user}/configurations/${payload.config}`, state.config)
        .then((response) => {
          console.log(response.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },

    async remConfig(_, payload) {
      return new Promise((resolve, reject) => {
        http
          .delete(`/users/${payload.user}/configurations/${payload.config}`)
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

    // LOCATION related actions
    async addLocation({ commit }, id) {
      return new Promise((resolve, reject) => {
        http
          .post(`configurations/${id}/locations`)
          .then((response) => {
            console.log('location :');
            console.log(response.data);
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
          .get(`/configurations/${id}/locations/${id}`)
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
        .put(`configurations/${id}/locations/${id}`, state.location)
        .then((response) => {
          console.log(response.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },

    async remLocation(_, id) {
      http
        .delete(`configurations/${id}/locations/${id}`)
        .then((response) => {
          console.log(response.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },

    // SENSOR related actions
    updateSensor(_, payload) {
      http
        .put(`/configurations/${payload.config}/sensors/${payload.sensor}`, payload.state)
        .then((response) => {
          console.log('sensor updated');
          console.log(response.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },

    getSensorOptions({ commit }, payload) {
      return new Promise((resolve, reject) => {
        http
          .get(`/sensors/cofely_vision?number=${payload}`, {
            timeout: 100000,
          })
          .then((response) => {
            resolve(response.data);
          })
          .catch((error) => {
            if (error.response) {
              commit('SET_ERROR', true);
            }
            reject(error);
          });
      });
    },

    getSensorList({ commit }, id) {
      http
        .get(`configurations/${id}/sensors`)
        .then((response) => {
          let sensors = response.data;
          if (sensors.length > 0) {
            for (const sensor of sensors) {
              commit('ADD_SENSOR', sensor);
            }
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },

    addSensor({ commit, dispatch, state }, sensor) {
      http
        .post(`configurations/${sensor.config_id}/sensors`, sensor)
        .then((response) => {
          console.log(response.data);
          commit('ADD_SENSOR', response.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },

    async remSensor({ commit, getters }, sensor) {
      console.log(sensor);
      http
        .delete(`configurations/${sensor.config_id}/sensors/${sensor.id}`)
        .then((response) => {
          const index = getters.indexSensorFromId(sensor.id);
          commit('REM_SENSOR', index);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    // HEATING PLANT related actions
    async getHeatingPlantList() {
      return new Promise((resolve, reject) => {
        http
          .get(`/heatingsplants`)
          .then((response) => {
            resolve(response.data);
          })
          .catch((error) => {
            console.log(error);
            reject(error);
          });
      });
    },

    async addHeatingPlant({ commit }, id) {
      return new Promise((resolve, reject) => {
        http
          .post(`/configurations/${id}/heatingplants`)
          .then((response) => {
            console.log('user :');
            console.log(response.data);
            commit('SET_PLANT', response.data);
            resolve(response.data);
          })
          .catch((error) => {
            console.log(error);
            reject(error);
          });
      });
    },

    async getHeatingPlant({ commit }, id) {
      return new Promise((resolve, reject) => {
        http
          .get(`/configurations/${id}/heatingplants/${id}`)
          .then((response) => {
            commit('SET_PLANT', response.data);
            resolve(response.data);
          })
          .catch((error) => {
            console.log(error);
            reject(error);
          });
      });
    },

    async updateHeatingPlant({ state }, id) {
      http
        .put(`/configurations/${id}/heatingplants/${id}`, state.plant)
        // .then((response) => {
        //   console.log(response.data);
        // })
        .catch((error) => {
          console.log(error);
        });
    },
    // SILOS related actions
    async getSiloList({ commit }, id) {
      return new Promise((resolve, reject) => {
        http
          .get(`heatingplants/${id}/silos`)
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
          .post(`/heatingplants/${id}/silos`)
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
      if (payload === undefined || typeof payload === 'number') {
        payload = {
          plant: getters.idUser,
          silo: getters.silo.id,
        };
      }
      return new Promise((resolve, reject) => {
        http
          .put(`/heatingplants/${payload.plant}/silos/${payload.silo}`, getters.siloFromId(payload.silo))
          .then((response) => {
            resolve(response.data);
          })
          .catch((error) => {
            console.log(error);
            reject(error);
          });
      });
    },

    async remSilo(_, payload) {
      return new Promise((resolve, reject) => {
        http
          .delete(`/heatingplants/${payload.user}/silos/${payload.silo}`)
          .then((response) => {
            resolve(response.data);
          })
          .catch((error) => {
            console.log(error);
            reject(error);
          });
      });
    },
    // BOILERS related actions
    async getBoilerList({ commit }, id) {
      return new Promise((resolve, reject) => {
        http
          .get(`/heatingplants/${id}/boilers`)
          .then((response) => {
            commit('SET_BOILER_LIST', response.data);
            resolve(response.data);
          })
          .catch((error) => {
            console.log(error);
            reject(error);
          });
      });
    },

    async updateBoiler({ getters }, payload) {
      return new Promise((resolve, reject) => {
        http
          .put(`/heatingplants/${payload.plant}/silos/${payload.silo}/boilers/${payload.boiler}`, getters.boilerFromId(payload.boiler))
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
          order: state.boilers.length + 1,
        };
        http
          .post(`/heatingplants/${payload.plant}/silos/${payload.silo}/boilers`, boiler)
          .then((response) => {
            commit('ADD_BOILER', { index: getters.indexBoilerToAdd(payload.silo), data: response.data });
            resolve(response.data);
          })
          .catch((error) => {
            console.log(error);
            reject(error);
          });
      });
    },

    async remBoiler(_, payload) {
      return new Promise((resolve, reject) => {
        http
          .delete(`/heatingplants/${payload.plant_id}/silos/${payload.silo_id}/boilers/${payload.id}`)
          .then((response) => {
            resolve(response.data);
          })
          .catch((error) => {
            console.log(error);
            reject(error);
          });
      });
    },
    // PLANNING related actions
    async getPlanningList({ commit }, id) {
      return new Promise((resolve, reject) => {
        http
          .get(`/heatingplants/${id}/plannings`)
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
          .post(`/silos/${silo_id}/plannings`)
          .then((response) => {
            console.log('planning :');
            console.log(response.data);
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

    async updateDefaultPlanning(_, payload) {
      return new Promise((resolve, reject) => {
        http
          .put(`/heatingplants/${payload.plant}/silos/${payload.silo}/plannings/${payload.silo}`, payload.state)
          .then((response) => {})
          .catch((error) => {
            console.log(error);
          });
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

    // SNAPSHOT related actions
    async getSnapshotList({ commit }, plant_id) {
      return new Promise((resolve, reject) => {
        http
          .get(`/heatingplants/${plant_id}/snapshots`)
          .then((response) => {
            commit('SET_SNAPSHOT_LIST', response.data);
            resolve(response.data);
          })
          .catch((error) => {
            reject(error);
          });
      });
    },
    async addSnapshot({ commit }, payload) {
      return new Promise((resolve, reject) => {
        http
          .post(`/silos/${payload.silo_id}/snapshots`)
          .then((response) => {
            console.log('snapshot :');
            console.log(response.data);
            commit('SET_SNAPSHOT', { index: payload.index, data: response.data });
            resolve(response.data);
          })
          .catch((error) => {
            console.log(error);
            reject(error);
          });
      });
    },

    async getSnapshot({ commit }, snap) {
      return new Promise((resolve, reject) => {
        http
          .get(`/heatingplants/${snap.plant_id}/silos/${snap.silo_id}/snapshots/${snap.silo_id}`)
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

    async updateSnapshot({ commit }, snap) {
      http
        .put(`/heatingplants/${snap.plant_id}/silos/${snap.silo_id}/snapshots/${snap.silo_id}`, snap.state)
        .then((response) => {
          console.log(response.data);
          commit('UPD_SNAPSHOT', response.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },

    async remSnapshot({ commit }, snap) {
      return new Promise((resolve, reject) => {
        http
          .delete(`/heatingplants/${snap.plant_id}/silos/${snap.silo_id}/snapshots/${snap.silo_id}`, snap.state)
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

    // CONSTRAINTS related actions
    async getConstraintList({ commit }, id) {
      return new Promise((resole, reject) => {
        http
          .get(`/heatingplants/${id}/rules`)
          .then((response) => {
            commit('SET_CONSTRAINT_LIST', response.data);
            resole(response.data);
          })
          .catch((error) => {
            console.log(error);
            reject(error);
          });
      });
    },
    async addConstraint({ commit }, load) {
      return new Promise((resolve, reject) => {
        http
          .post(`/silos/${load.silo}/rules`, load.state)
          .then((response) => {
            commit('ADD_CONSTRAINT', response.data);
            resolve(response.data);
          })
          .catch((error) => {
            console.log(error);
            reject(error);
          });
      });
    },
    async updateConstraint({ commit }, load) {
      return new Promise((resolve, reject) => {
        http
          .put(`/heatingplants/${load.plant}/silos/${load.silo}/rules/${load.id}`, load.state)
          .then((response) => {
            console.log(response.data);
            commit('PUT_CONSTRAINT', response.data);

            resolve(response.data);
          })
          .catch((error) => {
            console.log(error);
            reject(error);
          });
      });
    },
    async remConstraint({ commit }, load) {
      return new Promise((resolve, reject) => {
        http
          .delete(`/heatingplants/${load.plant}/silos/${load.silo}/rules/${load.id}`)
          .then((response) => {
            console.log(response.data);
            commit('REM_CONSTRAINT', load.id);
            resolve(response.data);
          })
          .catch((error) => {
            console.log(error);
            reject(error);
          });
      });
    },

    // PREVISIONS related actions
    async getPrevisions(_, payload) {
      return new Promise((resolve, reject) => {
        let params = {};
        if (payload.show === true) {
          params.show = payload.show;
        }
        http
          .get(`/users/${payload.user}/previsions/${payload.config}`, {
            params: params,
          })
          .then((response) => {
            console.log("--- DONNEES D'ENTREE ---");
            console.log(response.data);
            resolve(response.data);
          })
          .catch((error) => {
            console.log(error);
            reject(error);
          });
      });
    },
    async getStockBiomasse(_, payload) {
      return new Promise((resolve, reject) => {
        let params = {};
        if (payload.refresh === true) {
          params.refresh = payload.refresh;
        }
        http
          .get(`/users/${payload.user}/biomass_stock/${payload.config}`, {
            timeout: 3600000,
            params: params,
          })
          .then((response) => {
            // console.log('--- PLANNING ---');
            // console.log(response.data);
            // commit('ADD_APPRO', array)
            resolve(response.data);
          })
          .catch((error) => {
            console.log(error);
            reject(error);
          });
      });
    },
    async getBesoinBiomasse({ commit }, payload) {
      return new Promise((resolve, reject) => {
        let params = {};
        if (payload.refresh === true) {
          params.refresh = payload.refresh;
        }
        http
          .get(`/users/${payload.user}/biomass_need/${payload.config}`, {
            timeout: 100000,
            params: params,
          })
          .then((response) => {
            // console.log('--- BIOMASSE ---')
            // console.log(response.data);
            // const length = response.data.length / 2
            // const array = Array(length).fill({})
            // commit('ADD_WOOD', response.data)
            resolve(response.data);
          })
          .catch((error) => {
            console.log(error);
            reject(error);
          });
      });
    },
    async getPrevisionDemande({ commit }, payload) {
      return new Promise((resolve, reject) => {
        let params = {};
        if (payload.refresh === true) {
          params.refresh = payload.refresh;
        }
        http
          .get(`/users/${payload.user}/demand_prevision/${payload.config}`, {
            timeout: 100000,
            params: params,
          })
          .then((response) => {
            // console.log('--- DEMANDE ---')
            // console.log(response.data);
            // const length = response.data.length / 2
            // const array = Array(length).fill({})
            // commit('ADD_DEMAND', array)
            resolve(response.data);
          })
          .catch((error) => {
            console.log(error);
            reject(error);
          });
      });
    },

    async getPrevisionMeteo({ commit }, payload) {
      return new Promise((resolve, reject) => {
        let params = {};
        if (payload.refresh === true) {
          params.refresh = payload.refresh;
        }
        http
          .get(`/users/${payload.user}/weather_prevision/${payload.config}`, {
            timeout: 100000,
            params: params,
          })
          .then((response) => {
            // console.log('--- METEO ---')
            // console.log(response.data);
            // const length = response.data.length / 2
            // const array = Array(length).fill({})
            // commit('ADD_METEO', array)
            resolve(response.data);
          })
          .catch((error) => {
            console.log(error);
            reject(error);
          });
      });
    },
    async getHistorics(_, payload) {
      return new Promise((resolve, reject) => {
        http
          .get(`/users/${payload.user}/historics/${payload.config}`)
          .then((response) => {
            // console.log('--- METEO ---')
            // console.log(response.data);
            // const length = response.data.length / 2
            // const array = Array(length).fill({})
            // commit('ADD_METEO', array)
            resolve(response.data);
          })
          .catch((error) => {
            console.log(error);
            reject(error);
          });
      });
    },
  },
  getters: {
    indexSensorFromId: (state) => (id) => {
      return state.sensors.findIndex((sensor) => sensor.id === id);
    },
    indexRuleFromId: (state) => (id) => {
      const index = state.rules.findIndex((rule) => rule.id === id);
      return index;
    },
    ruleList(state) {
      let rules = [];
      if (state.rules.length > 0) {
        let silo_id = state.silos[state.silo_index].id;
        return state.rules.filter((rule) => rule.silo_id === silo_id);
      }
      return rules;
    },
    indexSnapshotFromIdSilo: (state) => (id) => {
      return state.snapshots.findIndex((snap) => snap.id === id);
    },
    indexFirstBoiler: (state) => (silo_id) => {
      return state.boilers.findIndex((boiler) => boiler.silo_id === silo_id);
    },
    lastIndexBoiler: (state) => (silo_id) => {
      return state.boilers.reverse().findIndex((boiler) => (boiler.silo_id = silo_id));
    },
    boilerList(state) {
      let boilers = [];
      if (state.boilers.length > 0) {
        let silo_id = state.silos[state.silo_index].id;
        return state.boilers.filter((boiler) => boiler.silo_id === silo_id);
      }
      return boilers;
    },
    boiler(state, getters) {
      return getters.boilerList[state.boiler_index];
    },
    silo(state) {
      return state.silos[state.silo_index];
    },
    boilerListSelected: (state) => (id) => {
      return state.boilers.filter((boiler) => boiler.silo_id === id);
    },
    indexBoilerList(state, getters) {
      let index_list = [];
      for (let boiler of getters.boilerList) {
        index_list.push(state.boilers.findIndex(boiler));
        console.log(index_list);
      }
      return index_list;
    },
    // watched for update
    boilerCountList(state) {
      return state.silos.map(({ id, boiler_count }) => ({ id, boiler_count }));
    },
    // for action purposes
    indexSiloFromId: (state) => (id) => {
      return state.silos.findIndex((silo) => silo.id === id);
    },
    siloFromId: (state) => (id) => {
      return state.silos.find((silo) => silo.id === id);
    },
    indexBoilerToAdd: (state) => (silo_id) => {
      let index = state.boilers.length > 0 ? state.boilers.filter((boiler) => boiler.silo_id <= silo_id).length : 0;
      return index;
    },
    indexConstraintToAdd: (state) => (silo_id) => {
      let index = state.rules.length > 0 ? state.rules.filter((rule) => rule.silo_id <= silo_id).length : 0;
      return index;
    },
    boilerFromId: (state) => (id) => {
      return state.boilers.find((boiler) => boiler.id === id);
    },
    indexBoilerFromId: (state) => (id) => {
      return state.boilers.findIndex((boiler) => boiler.id === id);
    },
    orderList(state) {
      return state.boilers.map(({ id, order, silo_id }) => ({ id, order, silo_id }));
    },
    ruleFromId: (state) => (id) => {
      return state.rules.find((rule) => rule.id === id);
    },
    loadList: (state) => (id) => {
      return state.loads.filter((load) => load.rule_id === id);
    },
    loadListFromSilo(state, getters) {
      const boilers = getters.boilerList;
      const boilers_mapped = boilers.map((boiler) => boiler.id);
      let loads = [];
      for (const id of boilers_mapped) {
        for (const load of state.loads) {
          if (load.boiler_id === id) {
            loads.push(load);
          }
        }
      }
      return loads;
    },
    idUser(state) {
      return state.user.id;
    },
    error(state) {
      return state.error;
    },
    loading(state) {
      return state.loading;
    },
    indexLoadFromId: (state) => (id) => {
      return state.loads.findIndex((load) => load.id === id);
    },
  },
});

export default store;
