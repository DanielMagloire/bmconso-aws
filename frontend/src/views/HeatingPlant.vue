<template>
  <div class="view-boiler">
    <v-alert
      dense
      type="warning"
      dismissible
      transition="slide-y-transition"
      :value="value"
      border="left"
      elevation="1"
      tile
      v-on:input="reset()"
      colored-border
    >
      {{ alert }}
    </v-alert>
    <div class="main-container">
      <v-row
        class="
          order-wrapper 
          flex-nowrap 
          no-gutters"
      >
        <v-col class="order-nav pt-1">
          <div class="nav-title block-order">config.</div>
          <div class="nav-title sub-title block-order">générale</div>
        </v-col>
        <v-col class="order-body">
          <v-col cols="6" class="pa-0">
            <v-row no-gutters class=" d-flex justify-space-around">
              <v-col cols="6" class="pa-0">
                <fieldset class="cogeneration" :class="{ 'is-coge': isCoge, 'no-coge': !isCoge }">
                  <legend>
                    <v-row>
                      <v-col class="coge-legend pr-0 pl-1 pt-1" cols="7">
                        Cogénération
                      </v-col>
                      <v-col class="pa-0 pl-2" cols="1">
                        <div class="button r" id="button-1">
                          <input type="checkbox" class="checkbox" v-model="isCoge" @click="updateIsCoge()" />
                          <div class="knobs"></div>
                          <div class="layer"></div>
                        </div>
                      </v-col>
                    </v-row>
                  </legend>

                  <v-row no-gutters class="pl-2 pr-4 pt-7">
                    <label for="power-coge" class="order-label power-coge">Puissance</label>
                  </v-row>
                  <v-row no-gutters class="pl-2 pr-4">
                    <input
                      @focus="$event.target.select()"
                      type="number"
                      :value="this.plant.power_coge"
                      @input="changeOtherOutput($event.target.value)"
                      style="padding-right:45px; text-align:right;"
                      :disabled="!isCoge"
                      :class="{ unavailable: !isCoge }"
                    />
                    <span style="margin-left:-50px" :class="{ unavailable: !isCoge }">kWh</span>
                  </v-row>
                </fieldset>
              </v-col>

              <v-col cols="6" class="pa-0">
                <fieldset class="pilotage">
                  <legend>pilotage</legend>
                  <v-row no-gutters class="pt-8">
                    <label for="piloting-type" class="order-label piloting-type">Type de pilotage</label>
                  </v-row>
                  <v-row no-gutters>
                    <select v-model="$store.state.plant.pilot_type" @change="updateHeatingPlant()">
                      <option v-for="(type, index) in pilot_types" :key="index" v-bind:value="type">{{ type }}</option>
                    </select>
                  </v-row>
                </fieldset>
              </v-col>
            </v-row>
          </v-col>

          <v-col cols="6" class="pa-0 pr-4 d-flex justify-center">
            <fieldset class="priorite">
              <legend>
                priorité d'allumage
              </legend>
              <table class="table table-responsive table-borderless">
                <thead>
                  <tr>
                    <th
                      class="silo-header"
                      v-for="(silo, index) in $store.state.silos"
                      :key="index"
                      :colspan="$store.state.silos[index].boiler_count"
                    >
                      SILO {{ index + 1 }}
                    </th>
                  </tr>
                  <tr>
                    <th class="boiler-header" v-for="index in $store.state.plant.boiler_total" :key="index">CHAUDIÈRE {{ index }}</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td v-for="(boiler, index) in orders" :key="index">
                      <select v-model="boiler.order" @change="changePriority({ id: boiler.id, order: boiler.order })">
                        <option v-for="index in $store.state.boilers.length" :key="index" v-bind:value="index"> {{ index }} </option>
                      </select>
                    </td>
                  </tr>
                </tbody>
              </table>
            </fieldset>
          </v-col>
        </v-col>
      </v-row>

      <v-row class="silo-wrapper flex-nowrap no-gutters">
        <v-col class="silo-nav flex-shrink-1 felx-grow-0">
          <div class="nav-title">SILO</div>
          <div class="btn-row silo-row" v-for="(silo, index) in this.silos" :key="silo.index">
            <button class="rem-btn" v-on:click="changeIndexSilo(index), removeSilo({ index: index, id: silo.id })">
              <v-icon small>
                mdi-delete
              </v-icon>
            </button>
            <button class="silo-btn" :class="{ active: index === silo_index }" v-on:click="changeIndexSilo(index)">{{ index + 1 }}</button>
          </div>
          <button class="add-btn silo-add" v-on:click="addSilo()">
            <v-icon small>
              mdi-plus-box-multiple
            </v-icon>
            <span>ajouter</span>
          </button>
        </v-col>

        <v-col class="silo-body flex-shrink-0 flex-grow-1 flex-wrap" v-if="this.silo !== undefined">
          <v-row no-gutters class="pa-0 ma-0">
            <v-col cols="6">
              <v-row no-gutters class="pa-0">
                <v-col cols="6" class="pa-0">
                  <fieldset class="caracteristics">
                    <legend id="second">caractéristiques</legend>
                    <div class="input-row">
                      <label for="max-cap">Volume du silo</label>
                      <input
                        :class="{ error: errCap }"
                        @focus="$event.target.select()"
                        type="number"
                        :value="this.silo.cap"
                        @input="changeCapacity($event.target.value)"
                        style="padding-right:45px; text-align:right;"
                      /><span style="margin-left:-40px;">m³</span>
                    </div>

                    <div class="input-row">
                      <label for="lower-limit">Niveau minimum du silo</label>
                      <input
                        min="0"
                        max="100"
                        :class="{ error: errLimitLow }"
                        @focus="$event.target.select()"
                        type="number"
                        :value="this.silo.limit_low"
                        @input="changeLowerLimit($event.target.value)"
                        style="padding-right:45px; text-align:right;"
                      /><span style="margin-left:-40px;">%</span>
                    </div>
                  </fieldset>
                </v-col>

                <v-col cols="6" class="pa-0">
                  <fieldset class="wood-type">
                    <legend id="first">type de bois</legend>

                    <div class="input-row">
                      <label for="PCI">PCI</label>
                      <input
                        :class="{ error: errPCI }"
                        min="0"
                        @focus="$event.target.select()"
                        type="number"
                        :value="this.silo.wood_pci"
                        @input="changePCI($event.target.value)"
                        style="padding-right:45px; text-align:right;"
                      /><span style="margin-left:-40px;">kWh/T</span>
                    </div>

                    <div class="input-row">
                      <label for="dens">Densité</label>
                      <input
                        :class="{ error: errDens }"
                        min="0"
                        @focus="$event.target.select()"
                        type="number"
                        :value="this.silo.wood_dens"
                        @input="changeDensity($event.target.value)"
                        style="padding-right:45px; text-align:right;"
                      /><span style="margin-left:-40px;">T/m³</span>
                    </div>
                  </fieldset>
                </v-col>
              </v-row>
            </v-col>

            <v-col cols="6">
              <v-row no-gutters class="pa-0 ma-0 pr-4">
                <v-col cols="12" class="pa-0">
                  <fieldset class="planning" v-if="this.planning !== undefined">
                    <legend id="fourth">planning par défaut</legend>
                    <div class="input-row">
                      <label for="deliveries">Nombre de camions par demi-journée</label>
                      <v-range-slider
                        v-model="range"
                        :max="max"
                        :min="min"
                        hide-details
                        class="align-center mt-1"
                        @change="changeDelivery()"
                      >
                        <template v-slot:prepend>
                          <v-text-field
                            outlined
                            dense
                            :value="range[0]"
                            class="rounded-0"
                            hide-details
                            single-line
                            type="number"
                            style="width: 50px; height: 35px;"
                            @change="$set(range, 0, $event)"
                          ></v-text-field>
                        </template>
                        <template v-slot:append>
                          <v-text-field
                            outlined
                            dense
                            :value="range[1]"
                            class="rounded-0"
                            hide-details
                            single-line
                            type="number"
                            style="width: 50px; height: 35px;"
                            @change="$set(range, 1, $event)"
                          ></v-text-field>
                        </template>
                      </v-range-slider>
                    </div>

                    <div class="input-row" id="medium-cap">
                      <label for="med-cap">Volume moyen (par camion)</label>
                      <input
                        min="0"
                        :class="{ error: errAv }"
                        @focus="$event.target.select()"
                        type="number"
                        :value="this.planning.av"
                        @input="changeMediumDelivery($event.target.value)"
                        style="padding-right:50px; text-align:right;"
                      /><span style="margin-left:-45px;">m³</span>
                    </div>
                  </fieldset>
                </v-col>
              </v-row>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
      <v-row class="boiler-wrapper flex-nowrap no-gutters">
        <v-col class="boiler-nav">
          <div class="nav-title">chaudière</div>
          <div class="btn-row boiler-row" v-for="(boiler, index) in this.boilerList" :key="boiler.index">
            <button class="rem-btn" v-on:click="removeBoiler({ silo_id: boiler.silo_id, id: boiler.id })">
              <v-icon small>
                mdi-delete
              </v-icon>
            </button>
            <button class="boiler-btn" :class="{ active: index === boiler_index }" v-on:click="changeBoilerIndex(index)">
              {{ indexBeforeBoiler + index + 1 }}
            </button>
          </div>
          <button class="add-btn boiler-add" v-on:click="addBoiler()">
            <v-icon small>
              mdi-plus-box
            </v-icon>
            <span>ajouter</span>
          </button>
        </v-col>

        <v-col class="boiler-body" v-if="this.boiler">
          <v-row no-gutters class="pa-0 ma-0">
            <v-col cols="3" class="pa-0">
              <div class="input-row">
                <label for="nominal-power">Puissance nominale</label>
                <input
                  min="0"
                  :class="{ error: errNom }"
                  @focus="$event.target.select()"
                  type="number"
                  :value="this.boiler.power_nom"
                  @input="changeNominalPower($event.target.value)"
                /><span style="margin-left:-40px;">kW</span>
              </div>
            </v-col>
            <v-col cols="3" class="pa-0">
              <div class="input-row">
                <label for="min-power">Puissance minimale</label>
                <input
                  min="0"
                  @focus="$event.target.select()"
                  type="number"
                  :value="this.boiler.power_min"
                  @input="changeMinimalPower($event.target.value)"
                /><span style="margin-left:-40px;">kW</span>
              </div>
            </v-col>
            <v-col cols="3" class="pa-0">
              <div class="input-row">
                <label for="output">Rendement</label>
                <input
                  min="0"
                  :class="{ error: errOut }"
                  @focus="$event.target.select()"
                  type="number"
                  :value="this.boiler.output"
                  @input="changeProductivity($event.target.value)"
                /><span style="margin-left:-40px;">%</span>
              </div>
            </v-col>
            <v-col cols="3" class="pa-0">
              <div class="input-row">
                <label for="load">Charge</label>
                <input
                  min="0"
                  :class="{ error: errLoad }"
                  @focus="$event.target.select()"
                  type="number"
                  :value="this.boiler.load"
                  @input="changeLoad($event.target.value)"
                />
                <span style="margin-left:-40px;">%</span>
              </div>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </div>

    <div class="button-container">
      <v-btn color="primary" @click="returnToNetwork()">Précédent</v-btn>
      <v-btn color="primary" @click="endConfiguration(), pushPrevivisions()">Terminer</v-btn>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import store from '../store/index';
import { mapState, mapGetters } from 'vuex';

export default {
  store: store,

  data() {
    return {
      errCap: false,
      errLimitLow: false,
      errLimitHigh: false,

      errPCI: false,
      errDens: false,

      errAv: false,
      errDropMin: false,

      errOut: false,
      errNom: false,
      errLoad: false,

      isCoge: true,

      units: ['m³', 'T'],
      pilot_types: ['Minimum de chaudières', 'Maximum de chaudières'],
      orders: [],
      min: 0,
      max: 30,
      range: [10, 20],
      value: false,
      alert: '',
    };
  },
  beforeRouteLeave(to, _, next) {
    console.log(to);
    if (!to.path.includes('configuration') && this.config.compl === 2) {
      this.endConfiguration();
    }
    next();
  },
  async created() {
    console.log('--- IN HEATING PLANT ---');
    this.setupCheckBoxes();
    if (this.config.num !== undefined) {
      if (this.config.compl !== 2) {
        const payload = {
          commit: 2,
          dispatch: {
            user: this.user.id,
            config: this.config.id,
          },
        };
        this.updateConfig(payload);
      }
      if (this.plant.is_coge !== undefined) {
        this.isCoge = this.plant.is_coge;
      }
      if (this.orders !== this.orderList) {
        console.log('--- setting order list ---');
        this.orders = this.orderList;
      }
      if (this.planning !== undefined) {
        if (this.planning.drop_min !== this.range[0]) this.range[0] = this.planning.drop_min;
        if (this.planning.drop_max !== this.range[1]) this.range[1] = this.planning.drop_max;
      }
    }
  },
  methods: {
    updateIsCoge() {
      store.commit('CHG_IS_COGE', this.isCoge);
      this.updateHeatingPlant();
    },
    reset() {
      this.value = false;
    },
    // initialisation methods
    setupCheckBoxes() {
      store.commit('CHECK_METEO', true);
      store.commit('CHECK_NETWORK', true);
      store.commit('CHECK_BOILER', false);
    },
    async updateConfig(payload) {
      store.commit('SET_COMPL', payload.commit);
      await store.dispatch('updateConfig', payload.dispatch);
    },
    async setupHeatingPlant() {
      if (this.plant && Object.keys(this.plant).length === 0 && Object.getPrototypeOf(this.plant) === Object.prototype) {
        console.log('still waiting...');
      } else {
        this.orders = this.orderList;
      }
    },

    // navigation methods
    changeIndexSilo(index) {
      store.commit('CHG_SILO', index);
    },
    changeBoilerIndex(index) {
      store.commit('CHG_BOILER', index);
    },

    // addition methods
    async addSilo() {
      if (this.plant.silo_count < 3) {
        console.log('adding silo');
        let silo = await store.dispatch('addSilo', this.plant.config_id);
        const payload = {
          plant: this.plant.config_id,
          silo: silo.id,
        };
        await store.dispatch('addBoiler', payload);
        await store.dispatch('addDefaultPlanning', silo.id);
        store.commit('INC_SILO_COUNT');
        store.commit('INC_BOILER_COUNT', this.silos.length - 1);
        store.commit('INC_BOILER_TOTAL');
        this.changeIndexSilo(this.plant.silo_count - 1);
        this.changeBoilerIndex(0);
      } else {
        this.alert = 'Maximum de silos atteint.';
        this.value = true;
      }
    },
    async addBoiler() {
      if (this.boilerList.length < 3) {
        const payload = {
          plant: this.plant.config_id,
          silo: this.silo.id,
        };
        await store.dispatch('addBoiler', payload);
        console.log('adding boiler to silo ' + this.indexSilo);
        store.commit('INC_BOILER_COUNT', this.indexSilo);
        store.commit('INC_BOILER_TOTAL');
        store.commit('CHG_BOILER', this.boilerList.length - 1);
      } else {
        this.alert = `Maximum de chaudière atteint pour silo ${this.silo_index + 1}.`;
        this.value = true;
      }
    },

    // removal methods
    async removeSilo(silo) {
      if (this.silos.length === 1) {
        this.alert = 'Minimum de silo atteint.';
        this.value = true;
      } else {
        const payload = {
          user: this.user.id,
          silo: this.silo.id,
        };
        console.log(payload);
        await store.dispatch('remSilo', payload);
        let index = this.indexFirstBoiler(silo.id);
        let boiler_list = this.boilerListSelected(silo.id);
        store.commit('DEC_SILO_COUNT');
        store.commit('CHG_BOILER_TOTAL', this.boilers.length - boiler_list.length);
        store.commit('REM_BOILER_LIST', { index, length: boiler_list.length });
        store.commit('REM_PLANNING', silo.id);
        store.commit('REM_SILO', silo.id);
        store.commit('CHG_SILO', 0);
      }
    },
    async removeBoiler(boiler) {
      if (this.silo.boiler_count === 1) {
        this.alert = `Minimum de chaudière atteint pour le silo ${this.silo_index + 1}.`;
        this.value = true;
      } else {
        const payload = {
          plant: this.plant.config_id,
          silo: this.silo.id,
          id: boiler.id,
        };
        await store.dispatch('remBoiler', payload);
        store.commit('CHG_BOILER', 0);
        store.commit('DEC_BOILER_TOTAL');
        store.commit('DEC_BOILER_COUNT', this.silo_index);
        store.commit('REM_BOILER', this.indexBoilerFromId(boiler.id));
      }
    },
    // silos options
    changePCI(pci) {
      this.errPCI = false;
      var parsed_pci = parseInt(pci);
      if (parsed_pci === 0) {
        this.errPCI = true;
      } else {
        store.commit('CHG_PCI', parsed_pci);
        this.updateSilo();
      }
    },
    changeDensity(dens) {
      this.errDens = false;
      var parsed_dens = parseFloat(dens);

      store.commit('CHG_DENS', parsed_dens);
      this.updateSilo();
    },

    changeCapacity(cap) {
      this.errCap = false;
      var parsed_cap = parseInt(cap);
      if (parsed_cap === 0) {
        this.errCap = true;
      } else {
        store.commit('CHG_CAP', parsed_cap);
        this.updateSilo();
      }
    },
    changeUpperLimit(limit_high) {
      if (limit_high === '') {
        limit_high = '0';
      }
      this.errLimitHigh = false;
      const limit_low = store.state.silos[store.state.silo_index].limit_low;
      var parsed_uphold = parseInt(limit_high);
      if (limit_low <= parsed_uphold && parsed_uphold <= 100) {
        store.commit('CHG_UPLIMIT', parsed_uphold);
        this.updateSilo();
      } else {
        this.errLimitHigh = true;
      }
    },
    changeLowerLimit(limit_low) {
      if (limit_low === '') {
        limit_low = '0';
      }
      this.errLimitLow = false;
      var parsed_lowhold = parseInt(limit_low);
      const limit_high = store.state.silos[store.state.silo_index].limit_high;
      if (parsed_lowhold <= limit_high && 0 <= parsed_lowhold) {
        store.commit('CHG_LOWLIMIT', parsed_lowhold);
        this.updateSilo();
      } else {
        this.errLimitLow = true;
      }
    },

    changeOtherOutput(other_power_output) {
      var parsed_opout = parseInt(other_power_output);
      store.commit('CHG_OTHEROUT', parsed_opout);
      this.updateHeatingPlant();
    },
    // PLANNING
    changeDelivery() {
      if (this.planning.drop_min !== this.range[0]) this.changeMinimumDelivery(this.range[0]);
      if (this.planning.drop_max !== this.range[1]) this.changeMaximumDelivery(this.range[1]);
    },
    changeMinimumDelivery(drop_min) {
      if (drop_min === '') {
        drop_min = '0';
      }
      this.errDropMin = false;
      const drop_max = store.state.plannings[store.state.silo_index].drop_max;
      var parsed_delimin = parseInt(drop_min);
      if (drop_min <= drop_max) {
        store.commit('CHG_DELIMIN', parsed_delimin);
        this.updateDefaultPlanning();
      } else {
        this.errDropMin = true;
      }
    },
    changeMaximumDelivery(max_delivery) {
      var parsed_delimax = parseInt(max_delivery);
      store.commit('CHG_DELIMAX', parsed_delimax);
      this.updateDefaultPlanning();
    },
    changeMediumDelivery(medium_delivery) {
      this.errAv = false;
      var parsed_delimed = parseInt(medium_delivery);
      if (parsed_delimed === 0) {
        this.errAv = true;
      } else {
        store.commit('CHG_DELIMED', parsed_delimed);
        this.updateDefaultPlanning();
      }
    },

    // boiler options
    changeNominalPower(power) {
      this.errNom = false;
      var parsed_pow = parseInt(power);
      if (parsed_pow === 0) {
        this.errNom = true;
      } else {
        store.commit('CHG_POW', { index: this.boilers.indexOf(this.boiler), value: parsed_pow });
        this.updateBoiler(this.boiler.id);
      }
    },
    changeProductivity(output) {
      this.errOut = false;
      var parsed_output = parseInt(output);
      if (parsed_output === 0) {
        this.errOut = true;
      } else {
        store.commit('CHG_OUT', { index: this.boilers.indexOf(this.boiler), value: parsed_output });
        this.updateBoiler(this.boiler.id);
      }
    },
    changeMinimalPower(power_min) {
      var parsed_powmin = parseInt(power_min);
      store.commit('CHG_POWMIN', { index: this.boilers.indexOf(this.boiler), value: parsed_powmin });
      this.updateBoiler(this.boiler.id);
    },
    changeLoad(load) {
      this.errLoad = false;
      var parsed_load = parseInt(load);
      if (parsed_load === 0) {
        this.errLoad = true;
      } else {
        store.commit('CHG_LOAD', { index: this.boilers.indexOf(this.boiler), value: parsed_load });
        this.updateBoiler(this.boiler.id);
      }
    },
    async changePriority(given) {
      const boiler_index = this.indexBoilerFromId(given.id);
      given.index = boiler_index;
      store.commit('CHG_BOILER_ORDER', given);
      let to_change = this.boilers.find((boiler) => boiler.id !== given.id && boiler.order === given.order);
      console.log('changing order boiler: ' + given.id);
      for (let count = 1; count <= this.boilers.length; count++) {
        if (this.boilers.some((boiler) => boiler.order === count) === false) {
          const boiler_index = this.indexBoilerFromId(to_change.id);
          const details = {
            index: boiler_index,
            order: count,
          };
          store.commit('CHG_BOILER_ORDER', details);
          // to_change.order = count;
          const payload = {
            plant: this.plant.config_id,
            silo: this.silo.id,
            boiler: to_change.id,
          };
          await store.dispatch('updateBoiler', payload);
          break;
        }
      }
      const payload = {
        plant: this.plant.config_id,
        silo: this.silo.id,
        boiler: given.id,
      };
      console.log('updating boiler: ' + given.id);
      console.log(payload);
      await store.dispatch('updateBoiler', payload);
      this.orders = this.orderList;
    },
    // DISPATCHS
    updateHeatingPlant() {
      store.dispatch('updateHeatingPlant', this.plant.config_id);
    },
    updateSilo() {
      store.dispatch('updateSilo', this.silo.id);
    },
    updateBoiler(id) {
      const payload = {
        plant: this.plant.config_id,
        silo: this.silo.id,
        boiler: id,
      };
      console.log(payload);
      store.dispatch('updateBoiler', payload);
    },
    updateDefaultPlanning() {
      const payload = {
        plant: this.user.id,
        silo: this.silo.id,
        state: this.planning,
      };
      store.dispatch('updateDefaultPlanning', payload);
    },

    // navigation button methods
    returnToNetwork() {
      this.$router.push('/configuration/demande-reseau');
    },
    async endConfiguration() {
      const payload = {
        commit: 3,
        dispatch: {
          user: this.user.id,
          config: this.config.id,
        },
      };

      this.updateConfig(payload);
      this.changeIndexSilo(0);
    },
    pushPrevivisions() {
      this.$router.push('/previsions');
    },
    setSiloPayload() {
      this.payload_silo = {
        user: this.user.id,
        silo: this.silo.id,
        sate: this.silo,
      };
    },
  },
  computed: {
    isErr() {
      return (
        this.errCap ||
        this.errLimitLow ||
        this.errLimitHigh ||
        this.errPCI ||
        this.errDens ||
        this.errAv ||
        this.errDropMin ||
        this.errNom ||
        this.errOut ||
        this.errLoad
      );
    },
    ...mapState(['silos', 'boilers', 'plannings', 'silo_index', 'boiler_index', 'plant', 'user', 'config']),
    ...mapState({
      // silo index dependent
      silo: (state) => state.silos[state.silo_index],
      planning: (state) => state.plannings[state.silo_index],
      // only for watch purpuses
      silo_count: (state) => state.plant.silo_count,
      boiler_total: (state) => state.plant.boiler_total,
    }),
    ...mapGetters([
      'boilerCountList',
      'orderList',
      'boilerList',
      'boilerListSelected',
      'indexFirstBoiler',
      'boiler',
      'indexBoilerFromId',
      'boilerFromId',
      'indexSiloFromId',
    ]),
    indexBeforeBoiler() {
      return this.indexFirstBoiler(this.silo.id);
    },
    indexSilo() {
      return this.indexSiloFromId(this.silo.id);
    },
  },
  watch: {
    planning(next, prev) {
      console.log(prev);
      if (prev === undefined) {
        console.log(next);
        this.range[0] = this.planning.drop_min;
        this.range[1] = this.planning.drop_max;
      }
    },
    value(val) {
      if (!val) return;
      setTimeout(() => (this.value = false), 5000);
    },
    plant(plant) {
      if (plant.is_coge !== undefined) {
        this.isCoge = plant.is_coge;
      }
    },
    orderList(new_arr, old_arr) {
      if (old_arr.length === 0) {
        this.orders = new_arr;
      }
      if (old_arr !== undefined && new_arr !== undefined) {
        // if there is at least one object less
        if (new_arr.length < old_arr.length) {
          console.log(new_arr);
          console.log(old_arr);
          // only one object in the new array
          if (new_arr.length === 1) {
            new_arr[0].order = 1;
            console.log('updating order boiler: ' + new_arr[0].id);
            store.commit('CHG_PRIORITY', new_arr[0]);
            const payload = {
              plant: this.user.id,
              silo: new_arr[0].silo_id,
              boiler: new_arr[0].id,
            };
            store.dispatch('updateBoiler', payload);
          }
          // more than one object in the new array
          if (new_arr.length > 1) {
            new_arr.sort((a, b) => {
              return a.order - b.order;
            });
            if (new_arr[0].order !== 1) {
              new_arr[0].order = 1;
            }
            let one = 0;
            for (let two = 1; two < new_arr.length; one++, two++) {
              new_arr[two].order = new_arr[one].order + 1;
            }
            for (let present of new_arr) {
              let past = old_arr.find((other) => other.id === present.id);
              if (past.order !== present.order) {
                console.log('updating boiler order');
                store.commit('CHG_PRIORITY', present);
                const payload = {
                  plant: this.user.id,
                  silo: present.silo_id,
                  boiler: present.id,
                };
                console.log(payload);
                store.dispatch('updateBoiler', payload);
              }
            }
          }
        }
      }
      this.orders = this.orderList;
    },
    boilerCountList(newCounts, oldCounts) {
      if (newCounts.length === oldCounts.length) {
        for (var i = 0; i < newCounts.length; i++) {
          if (newCounts[i].boiler_count !== oldCounts[i].boiler_count && newCounts[i].boiler_count > 0) {
            console.log(`boiler count went from ${oldCounts[i].boiler_count} to ${newCounts[i].boiler_count}`);
            console.log(`updating silo ${i}`);
            const payload = {
              plant: this.plant.config_id,
              silo: newCounts[i].id,
            };
            store.dispatch('updateSilo', payload);
          }
        }
      }
    },
    // state related watchers
    silo_count(newState, oldState) {
      if (typeof oldState === 'undefined') {
        console.log(`silo count went from ${oldState} to ${newState}`);
      } else if (newState !== oldState) {
        console.log(`silo count went from ${oldState} to ${newState}`);
        console.log('updating heating plant');
        store.dispatch('updateHeatingPlant', this.plant.config_id);
      }
    },
    boiler_total(newState, oldState) {
      if (newState !== oldState && typeof oldState !== 'undefined') {
        console.log(`boiler total went from ${oldState} to ${newState}`);
        console.log('updating heating plant');
        store.dispatch('updateHeatingPlant', this.plant.config_id);
      }
    },
  },
};
</script>

<style scoped>
@import 'https://cdnjs.cloudflare.com/ajax/libs/simple-line-icons/2.3.2/css/simple-line-icons.min.css';

.view-boiler * {
  transition: 0.4s;
}

.view-boiler fieldset legend * {
  transition: 0.1s !important;
}

input,
select {
  border: 1px solid rgba(0, 0, 0, 0.2);
  box-shadow: 0px 2px 1px 1px rgba(0, 0, 0, 0.1) inset;
  outline: none;
}

button {
  outline: none;
}
/************* navbar *****************/

.nav-title {
  height: 40px;
  line-height: 40px;
  padding-left: 15px;
  font-weight: bold;
  font-size: large;
  color: #949494;
  text-transform: uppercase;
}

.sub-title {
  line-height: 30px !important;
}

.block-silo {
  height: 54.5%;
}

.block-boiler {
  height: 30%;
}

.block-order {
  height: 15.5%;
}
/************************ navbar buttons */

.silo-nav {
  border-right: solid 5px #00aaff;
}

.boiler-nav {
  border-right: solid 5px #6ed;
}

.order-nav {
  border-right: 5px solid gray;
}

.silo-nav,
.boiler-nav,
.order-nav {
  max-width: 10em;
}

.btn-row {
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
}

.rem-btn:hover {
  opacity: 0.5;
}

.silo-row .rem-btn:hover {
  background-color: #00aaff;
}

.boiler-row .rem-btn:hover {
  background-color: #6ed;
}

.btn-row button {
  height: 40px;
  font-weight: bolder;
  letter-spacing: 1px;
}

.silo-btn.active,
.silo-btn.active:hover {
  color: white;
  background-color: #00aaff;
  border: none;
}

.silo-btn:hover {
  color: #00aaff;
}

.boiler-btn:hover {
  color: #6ed;
}

.boiler-btn.active {
  background-color: #6ed;
  border: none;
}

.add-btn {
  display: flex;
  align-items: center;
  color: rgb(50, 50, 50);
  height: 40px;
  font-size: 19px;
  font-weight: bold;
  border: none;
  margin-top: 5px;
  margin-bottom: 5px;
  font-family: monospace;
  align-self: center;
  width: 120px;
  margin-left: 15px;
  box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.1);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  padding-left: 16px;
}
.add-btn:focus {
  border: none;
}
.add-btn span {
  padding-left: 14px;
  color: #949494;
}
.silo-add:hover {
  background-color: #00aaff;
  opacity: 0.5;
}
.boiler-add:hover {
  background-color: #6ed;
  opacity: 0.5;
}
.silo-btn,
.boiler-btn {
  width: 90px;
  border: none;
  color: #949494;
  box-shadow: none;
}
.boiler-btn.active {
  background-color: #6ed;
  color: white;
}
.rem-btn {
  width: 50px;
  border: none;
  border-right: 1px solid lightgray;
  margin-left: 15px;
  font-size: xx-large;
  font-family: monospace;
}

/********* specificities *********/

.data {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: calc(100% - 153px);
}

/******************* column options */

.fieldset-row {
  display: flex;
  width: 100%;
  justify-content: space-evenly;
  flex-wrap: wrap;
}

fieldset.priorite {
  width: 100% !important;
}

fieldset,
fieldset:hover {
  width: 250px;
  padding-left: 15px;
  padding-right: 15px;
  border: solid 1px #949494;
  padding-bottom: 15px;
  height: 15em;
}

fieldset.planning {
  width: 100%;
  border: 1px solid #00aaff;
  box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.1);
  padding-left: 1.5em;
  padding-right: 1.5em;
}

fieldset.is-coge {
  border: 1px solid #03a9f4;
}

fieldset.is-coge legend {
  color: #00aaff;
}
fieldset.no-coge {
  border: 1px solid #f44336;
}

fieldset.no-coge legend {
  color: #949494;
}

fieldset.cogeneration,
fieldset.pilotage,
fieldset.priorite {
  height: 10em;
}

.planning legend {
  color: #00aaff;
}

#medium-cap {
  width: 250px;
}

legend,
legend:hover {
  text-transform: uppercase;
  display: block;
  font-size: 0.9em;
  padding-left: 1em;
  padding-right: 1em;
  font-weight: bold;
  float: none;
  width: auto;
}

.view-boiler label {
  font-size: 0.9em;
  margin-top: 10px;
  margin-bottom: 5px;
}

label[for='PCI'],
label[for='upper-limit'],
label[for='other-output'],
label[for='deliveries'] {
  margin-top: 0px;
}
.boiler-container label {
  margin-top: 0px;
}

.view-boiler input,
.view-boiler select {
  width: calc(250px - 35px);
  height: 40px;
  font-weight: 500;
}

.view-boiler input {
  padding-left: 10px;
}
.view-boiler select {
  padding-left: 5px;
}

.view-boiler .other input {
  width: 215px;
}

.boiler-body {
  display: flex;
  width: 100%;
  justify-content: space-evenly;
  flex-wrap: wrap;
}

.boiler-body .input-row {
  padding-left: 15px;
  padding-right: 15px;
  width: 250px;
}

span.unavailable {
  background: none;
}

.unavailable {
  background-color: rgb(232, 232, 232);
  color: #949494;
}

/************** order ****************** */

.view-boiler table {
  height: 100%;
}

.silo-header {
  font-size: 0.9em;
}

.boiler-header {
  padding-top: 5px;
  font-size: 0.6em !important;
  text-transform: uppercase;
  letter-spacing: 0.09em;
  font-weight: 100;
}

.table select {
  padding-left: 8px;
  max-width: 50px;
  box-shadow: none;
}

.view-boiler .buttons {
  display: flex;
  width: 100%;
  justify-content: space-around;
  align-content: center;
  position: absolute;
  bottom: 0vh;
  padding: 5vh;
}

.view-boiler .main-container button i.icon {
  padding-left: 10px;
}

.view-boiler .main-container button:disabled {
  cursor: not-allowed;
  pointer-events: all !important;
  background: #949494;
}

.view-boiler span {
  font-size: 0.7em;
}

/* trying a litlle bit of order for change */

.view-boiler .main-container {
  overflow: auto;
  width: 100%;
  justify-content: start;
}

.silo-wrapper,
.boiler-wrapper,
.order-wrapper {
  display: flex;
  width: 100%;
}

.silo-body,
.boiler-body,
.order-body {
  background-color: white;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  width: 100%;
  padding: 1em 0 0 1em !important;
  border-bottom: solid 1px lightgray;
}

.silo-body > *,
.boiler-body > * {
  margin: 0 1em 1em 0;
}

.v-alert {
  z-index: 100;
  position: absolute;
  min-width: 50%;
  top: 5em;
  left: 13.5em;
  letter-spacing: 0.03em;
}

select {
  transition: 0s !important;
  background-image: linear-gradient(45deg, transparent 50%, gray 50%), linear-gradient(135deg, gray 50%, transparent 50%),
    linear-gradient(to right, #ccc, #ccc);
  background-position: calc(100% - 12px) calc(1em + 2px), calc(100% - 7px) calc(1em + 2px), calc(100% - 1.5em) 0.5em;
  background-size: 5px 5px, 5px 5px, 1px 1.5em;
  background-repeat: no-repeat;
}

select:focus {
  background-image: linear-gradient(45deg, gray 50%, transparent 50%), linear-gradient(135deg, transparent 50%, gray 50%),
    linear-gradient(to right, #ccc, #ccc);
  background-position: calc(100% - 7px) 1em, calc(100% - 12px) 1em, calc(100% - 1.5em) 0.5em;
  background-size: 5px 5px, 5px 5px, 1px 1.5em;
  background-repeat: no-repeat;
  outline: 0;
}

.order-label {
  padding-left: 0px;
  font-size: 0.6em !important;
  text-transform: uppercase;
  letter-spacing: 0.09em;
  padding-bottom: 1.1em;
}

.order-label.piloting-type,
.order-label.power-coge {
  padding-top: 2px;
}

span {
  width: 0px;
  line-height: 40px;
}

.presence-coge {
  font-weight: bold;
  text-transform: uppercase;
  font-size: 14px;
  padding-top: 1em;
}
.error {
  background-color: white !important;
  border: solid red 2px;
  outline: none;
}

.knobs,
.layer {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
}

.button {
  position: relative;
  top: -10%;
  width: 74px;
  height: 36px;
  overflow: hidden;
}

.button.r,
.button.r .layer {
  border-radius: 100px;
}

.checkbox {
  position: relative;
  width: 100%;
  height: 100%;
  padding: 0;
  margin: 0;
  opacity: 0;
  cursor: pointer;
  z-index: 3;
}

.knobs {
  z-index: 2;
}

.layer {
  width: 100%;
  background-color: #fcebeb;
  transition: 0.3s ease all;
  z-index: 1;
}

/* Button 1 */
#button-1 .knobs:before {
  content: 'NON';
  position: absolute;
  top: 4px;
  left: 4px;
  width: 27px;
  height: 27px;
  color: #fff;
  font-size: 10px;
  font-weight: bold;
  text-align: center;
  line-height: 1;
  padding: 9px 4px 9px 3px;
  background-color: #f44336;
  border-radius: 50%;
  transition: 0.3s cubic-bezier(0.18, 0.89, 0.35, 1.15) all;
}

#button-1 .checkbox:checked + .knobs:before {
  content: 'OUI';
  left: 42px;
  background-color: #03a9f4;
}

#button-1 .checkbox:checked ~ .layer {
  background-color: #ebf7fc;
}

#button-1 .knobs,
#button-1 .knobs:before,
#button-1 .layer {
  transition: 0.3s ease all;
}
</style>
