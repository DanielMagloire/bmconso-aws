<template>
  <div class="view-previsions" id="previsions">
    <nav-previsions class="nav-previsions" />
    <v-row no-gutters class="main-content">
      <v-col lg="4" xl="3" class="flex-shrink-0 flex-grow-0 card-col">
        <v-card tile flat class="snapshot-card ma-4 pa-4" v-if="this.snapshot && Object.keys(this.snapshot).length > 0">
          <v-col class="snapshot-inputs">
            <v-row no-gutters>
              <v-col cols="8">
                <v-text-field
                  :rules="posRules"
                  @input="updateSnapshot()"
                  @focus="$event.target.select()"
                  label="Niveau actuel du silo"
                  type="number"
                  v-model="snapshot.level"
                />
              </v-col>
              <v-col cols="4">
                <v-select @change="updateSnapshot()" :items="level_units" v-model="snapshot.level_unit" />
              </v-col>
            </v-row>
            <v-text-field
              :rules="perRules"
              @input="updateSnapshot()"
              @focus="$event.target.select()"
              label="Objectif de remplissage"
              suffix="%"
              type="number"
              class="goal-input"
              v-model="snapshot.goal"
            />
          </v-col>
          <v-card-actions class="d-flex pa-0 snapshot-actions">
            <v-btn large block tile color="light-blue" @click="Actualize()" class="white--text font-weight-bold">
              Actualiser
              <v-icon small class="mr-2">
                mdi-refresh
              </v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>

        <v-data-table
          v-if="this.appro"
          :headers="planning_headers"
          :items="this.appro"
          :item-class="itemRowBackground"
          item-key="id"
          hide-default-footer
          hide-default-header
          class="pa-4 ma-4 planning-table"
        >
          <template v-slot:top>
            <v-toolbar flat class="d-flex justify-center planning-head">
              <v-toolbar-title class="text-uppercase light-blue--text planning-title">
                livraisons
              </v-toolbar-title>
            </v-toolbar>
          </template>
          <template #header="{ }">
            <thead class="v-data-table-header">
              <tr>
                <th
                  v-for="(h, i) in planning_headers"
                  :key="i"
                  class="text-center parent-header td-border-style"
                  :rowspan="h.children ? 1 : 2"
                  :colspan="h.children ? h.children.length : 1"
                >
                  {{ h.text }}
                </th>
              </tr>
            </thead>
          </template>
          <template v-slot:[`body.append`]>
            <tr class="planning-footer">
              <td class="planning-mornings">{{ total_morning }}</td>
              <td class="planning-noons">{{ total_afternoon }}</td>
              <th class="planning-total">total</th>
            </tr>
          </template>
        </v-data-table>
      </v-col>
      <v-col lg="8" xl="9" class="main-col flex-shrink-0 flex-grow-0">
        <v-row no-gutters class="chart-row ">
          <v-col lg="6" class="pa-4">
            <v-card elevation="2" class="pa-5">
              <stock-bois ref="biomass-chart" v-if="this.wood !== undefined" />
            </v-card>
          </v-col>
          <v-col lg="6" class="pa-4 prevision-chart">
            <v-card elevation="2" class="pa-5">
              <puissance-temperature ref="prevision-chart" v-if="this.demand !== undefined && this.meteo !== undefined" />
            </v-card>
          </v-col>
        </v-row>
        <v-row no-gutters>
          <!-- sort-by="id" -->

          <v-data-table
            hide-default-footer
            :headers="headers"
            :items="sortedRules"
            class="elevation-0 pa-4 rule-table"
            hide-default-header
            loading-text="Chargement..."
          >
            <template v-slot:top>
              <v-toolbar class="add-toolbar">
                <v-col cols="12" class="pa-0">
                  <v-sheet class="add-sheet d-flex flex-direction-row pa-2">
                    <v-menu :close-on-content-click="false" bottom offset-y>
                      <template v-slot:activator="{ on }">
                        <v-btn color="light-blue" large v-on="on" plain class="add-btn font-weight-bold pl-7">
                          ajouter
                          <v-icon class="mr-2">
                            mdi-table-row-plus-after
                          </v-icon>
                        </v-btn>
                      </template>

                      <v-list class="pa-0">
                        <v-list-group v-for="(item, index) in items" :key="item.title" v-model="item.active" no-action>
                          <v-icon slot="prependIcon" large color="primary">${{ item.action }}</v-icon>
                          <template v-slot:activator>
                            <v-list-item-content>
                              <v-list-item-title class="menu-text">{{ item.title }}</v-list-item-title>
                            </v-list-item-content>
                          </template>

                          <v-list-item v-for="child in item.items" :key="child.title" link @click="setDialogBox(child.title), showDialog()">
                            <v-list-item-content class="pl-3 pr-12">
                              <v-list-item-title class="menu-text">{{ child.title }}</v-list-item-title>
                            </v-list-item-content>
                          </v-list-item>
                          <v-divider class="ma-0" v-if="index < items.length - 1" :key="`${index}-divider`"></v-divider>
                        </v-list-group>
                      </v-list>
                    </v-menu>
                    <v-divider class="vertical-divider" vertical></v-divider>
                    <v-toolbar-title class=" mx-2 tool-title text-uppercase d-flex align-center light-blue--text">
                      contraintes sur le planning d'approvisionnement
                    </v-toolbar-title>
                    <!-- <v-col class="pa-0" cols="4">
                      <v-select
                        v-model="selected_item"
                        :items="select_items"
                        :menu-props="{ bottom: true, offsetY: true }"
                        class="mr-2 add-select"
                        filled
                        dense
                        hide-details
                      ></v-select>
                    </v-col> -->
                    <v-col cols="auto" class="pa-0">
                      <v-dialog v-model="dialog" max-width="300px">
                        <!-- v-slot:activator="{ on, attrs }" -->
                        <template>
                          <!-- <v-btn
                            :disabled="selected_item === ''"
                            elevation="1"
                            tile
                            large
                            outlined
                            color="primary"
                            class="add-btn font-weight-bold pl-7"
                            v-bind="attrs"
                            v-on="on"
                            @click="setDialogBox(selected_item)"
                          >
                            ajouter
                            <v-icon class="mr-2">
                              mdi-table-row-plus-after
                            </v-icon>
                          </v-btn> -->
                        </template>
                        <v-card>
                          <v-card-title>
                            <span class="dialog-title text-h5">AJOUTER</span>
                          </v-card-title>

                          <v-card-text>
                            <v-container>
                              <v-row class="pl-8">
                                <v-col cols="10">
                                  <v-text-field
                                    persistent-placeholder
                                    type="number"
                                    @focus="$event.target.select()"
                                    v-model="editedItem.value"
                                    :label="props.label"
                                    :suffix="props.suffix"
                                  ></v-text-field>
                                </v-col>
                                <v-col cols="10">
                                  <v-menu
                                    v-model="startDateMenu"
                                    :close-on-content-click="false"
                                    :nudge-right="40"
                                    transition="scale-transition"
                                    offset-y
                                    max-width="290px"
                                    min-width="290px"
                                  >
                                    <template v-slot:activator="{ on }">
                                      <v-text-field v-model="startDateDisp" label="Date début" readonly v-on="on" />
                                    </template>
                                    <v-date-picker
                                      locale="fr-fr"
                                      :min="today_str"
                                      v-model="editedItem.date_begin"
                                      no-title
                                      @input="startDateMenu = false"
                                    />
                                  </v-menu>
                                </v-col>
                                <v-col cols="10">
                                  <v-select
                                    v-if="!editedItem.name.includes('Livraisons')"
                                    :menu-props="{ bottom: true, offsetY: true }"
                                    :items="hours"
                                    v-model="string_begin"
                                    label="Heure début"
                                    type="text"
                                    @change="formatHour({ begin: true, hour: string_begin })"
                                  />
                                  <v-select
                                    v-else
                                    :menu-props="{ bottom: true, offsetY: true }"
                                    :items="times"
                                    v-model="editedItem.time_begin"
                                    label="Heure début"
                                  />
                                </v-col>
                                <v-col cols="10">
                                  <v-menu
                                    v-model="endDateMenu"
                                    :close-on-content-click="false"
                                    :nudge-right="40"
                                    transition="scale-transition"
                                    offset-y
                                    max-width="290px"
                                    min-width="290px"
                                  >
                                    <template v-slot:activator="{ on }">
                                      <v-text-field v-model="endDateDisp" label="Date fin" readonly v-on="on" />
                                    </template>
                                    <v-date-picker
                                      locale="fr-fr"
                                      :min="startDate"
                                      v-model="editedItem.date_end"
                                      no-title
                                      @input="endDateMenu = false"
                                    />
                                  </v-menu>
                                </v-col>
                                <v-col cols="10">
                                  <v-select
                                    v-if="!editedItem.name.includes('Livraisons')"
                                    :menu-props="{ bottom: true, offsetY: true }"
                                    :items="hours"
                                    v-model="string_end"
                                    label="Heure fin"
                                    @change="formatHour({ begin: false, hour: string_end })"
                                  />
                                  <v-select
                                    v-else
                                    :menu-props="{ bottom: true, offsetY: true }"
                                    :items="times"
                                    v-model="editedItem.time_end"
                                    label="Heure fin"
                                  />
                                </v-col>
                              </v-row>
                            </v-container>
                          </v-card-text>

                          <v-card-actions>
                            <v-btn class="font-weight-bold" color="blue darken-1" text @click="close">
                              Annuler
                            </v-btn>
                            <v-spacer />
                            <v-btn class="font-weight-bold" color="blue darken-1" text @click="save" :disabled="editedItem.value === null">
                              Sauvegarder
                            </v-btn>
                          </v-card-actions>
                        </v-card>
                      </v-dialog>
                    </v-col>
                  </v-sheet>
                </v-col>

                <v-dialog v-model="dialogDelete" max-width="500px">
                  <v-card class="pa-7">
                    <v-card-title class="text-h5 justify-center pa-7"> Supprimer contrainte {{ editedIndex + 1 }} ? </v-card-title>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="blue darken-1" text @click="closeDelete" class="font-weight-bold">
                        Annuler
                      </v-btn>
                      <v-spacer />
                      <v-btn color="blue darken-1" text @click="deleteItemConfirm" class="font-weight-bold">
                        Supprimer
                      </v-btn>
                      <v-spacer />
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-toolbar>
            </template>

            <template #header="{ }">
              <thead class="v-data-table-header">
                <tr>
                  <!--                     :rowspan="h.children ? 1 : 2"
                    :colspan="h.children ? h.children.length : 1"
 -->
                  <th v-for="(h, i) in headers" :key="i" class="text-center parent-header td-border-style">
                    <v-switch class="switch" inset v-model="allowDrag" v-if="h.text === ''" />
                    {{ h.text }}
                  </th>
                </tr>
              </thead>
            </template>
            <template v-slot:body="props">
              <!-- @end="onDropCallback" -->
              <draggable
                :list="props.items"
                tag="tbody"
                :disabled="!allowDrag"
                :move="onMoveCallback"
                :clone="onCloneCallback"
                @end="lookForChanges(props.items)"
                handle=".grab-icon"
              >
                <tr v-for="(item, index) in props.items" :key="index">
                  <td>
                    <div class="d-flex justify-center">
                      <v-icon small color="black" class="grab-icon" :class="{ 'no-drag': !allowDrag }">
                        mdi-swap-vertical-bold
                      </v-icon>
                    </div>
                  </td>
                  <td class="text-center">
                    {{ index + 1 }}
                  </td>
                  <td class="text-center" v-for="(c, ci) in getRows(item)" :key="ci">
                    {{ c }}
                  </td>
                  <td class="px-0 td-actions">
                    <div class="d-flex justify-center">
                      <v-btn elevation="0" icon color="light-blue">
                        <v-icon small class="mr-2" @click="setDialogBox(item.name), editItem(item)">
                          mdi-pencil
                        </v-icon>
                      </v-btn>
                      <v-divider vertical class="action-divider"></v-divider>
                      <v-btn elevation="0" icon color="error">
                        <v-icon class="mr-2" small @click="deleteItem(item)">
                          mdi-delete
                        </v-icon>
                      </v-btn>
                    </div>
                  </td>
                </tr>
              </draggable>
            </template>
            <!--             
            <template #item="props">
                <tr>
                  <td class="text-center" v-for="(c, ci) in getRows(props.item)" :key="ci">
                    {{ c }}
                  </td>
                  <td class="d-flex justify-space-around">
                    <v-icon small @click="deleteItem(props.item)">
                      mdi-delete
                    </v-icon>
                  </td>
                </tr>
            </template>

            <template v-slot:[`item.actions`]="{ props }">
              <v-icon small class="mr-2" @click="editItem(props.item)">
                mdi-pencil
              </v-icon>
              <v-icon small @click="deleteItem(props.item)">
                mdi-delete
              </v-icon>
            </template> -->
          </v-data-table>
          <v-row no-gutters class="pa-4" v-if="isTest">
            <v-col class="pa-1">
              <v-btn large block tile outlined @click="refreshDemande()" class="test-btn primary--text font-weight-bold"
                >prevision demande</v-btn
              >
            </v-col>
            <v-col class="pa-1">
              <v-btn large block tile outlined @click="refreshStockBois()" class="test-btn primary--text font-weight-bold"
                >évolution stock de bois</v-btn
              >
            </v-col>
            <v-col class="pa-1">
              <v-btn large block tile outlined @click="refreshPlanningAppro()" class="test-btn primary--text font-weight-bold"
                >stock biomasse</v-btn
              >
            </v-col>
            <v-col class="pa-1">
              <v-btn large block tile outlined @click="getPrevisions()" class="test-btn primary--text font-weight-bold"
                >onglet prevision</v-btn
              >
            </v-col>
          </v-row>
        </v-row>
      </v-col>
    </v-row>
  </div>
</template>

<script>
/* eslint-disable */

import store from '../store/index';
import NavPrevisions from '../navigation/PrevisionsNavbar.vue';
import { mapState, mapGetters } from 'vuex';
import StockBois from '../charts/StockBois.vue';
import PuissanceTemperature from '../charts/PuissanceTemperature.vue';
import moment from 'moment';
import draggable from 'vuedraggable';
import BoilerIcon from '../icons/boiler.vue';

export default {
  components: {
    NavPrevisions,
    StockBois,
    PuissanceTemperature,
    draggable,
    BoilerIcon,
  },

  store: store,
  data() {
    return {
      sortedRules: [],
      string_begin: '00:00',
      string_end: '23:00',
      allowDrag: true,
      dialog: false,
      dialogDelete: false,
      isTest: true,
      perRules: [(v) => (v && v >= 0) || '', (v) => (v && v <= 100) || ''],
      posRules: [(v) => (v && v >= 0) || ''],
      props: {
        label: 'label',
        suffix: 'suffix',
      },
      selected_item: '',
      select_items: [
        'Cogénération : Puissance',
        'Densité du bois',
        'Livraisons maximales sur la demi-journée',
        'Livraisons minimales sur la demi-journée',
        'PCI du bois',
        'Volume moyen de biomasse par camion',
      ],
      items: [],
      loading: true,
      planning_headers: [
        {
          text: 'Matin',
          align: 'center',
          value: 'NB_CAMIONS_1',
        },
        {
          text: 'Après-midi',
          value: 'NB_CAMIONS_2',
          align: 'center',
        },
        {
          text: 'Date',
          value: 'DATE',
          align: 'center',
        },
      ],
      snapshot: {},
      times: ['Matin', 'Après-midi'],
      total_morning: 0,
      total_afternoon: 0,
      today_str: new Date().toISOString().split('T')[0],
      today_timestamp: new Date().getTime(),
      year_before: new Date(new Date().setFullYear(new Date().getFullYear() - 1)).getTime(),
      hours: [],
      frequencies: ['Jour', 'Semaine', 'Mois', 'Année'],
      level_units: ['m³', 'Wh', 'kW'],
      // planning table related data
      headers: [
        { text: '' },
        { text: '#' },
        {
          text: 'Contrainte',
          value: 'name',
        },
        {
          text: 'Valeur',
          value: 'value',
        },
        {
          text: 'Date début',
          value: 'date_begin',
        },
        {
          text: 'Heure début',
          value: 'hour_begin',
        },
        {
          text: 'Date fin',
          value: 'date_end',
        },
        {
          text: 'Heure fin',
          value: 'hour_end',
        },
        {
          text: 'Actions',
          value: 'actions',
          sortable: false,
          align: 'center',
        },
      ],
      editedIndex: -1,
      editedItem: {
        name: '',
        value: null,
        date_begin: new Date().toISOString().split('T')[0],
        date_end: new Date().toISOString().split('T')[0],
        hour_begin: new Date().getHours(),
        hour_end: new Date().getHours() + 1,
        time_begin: 'Matin',
        time_end: 'Matin',
      },
      defaultItem: {
        silo_id: 1,
        name: '',
        value: null,
        date_begin: new Date().toISOString().split('T')[0],
        date_end: new Date().toISOString().split('T')[0],
        hour_begin: new Date().getHours(),
        hour_end: new Date().getHours() + 1,
        time_begin: 'Matin',
        time_end: 'Matin',
      },
      startDateMenu: false,
      endDateMenu: false,
    };
  },
  created() {
    // fill hours array
    this.fillHourArray();
    if (this.config.compl === 3) this.setupPrevisions(this.config.id);
  },
  methods: {
    lookForChanges(items) {
      if (items.length === this.ruleList.length) {
        for (let i = 0; i < items.length; i++) {
          const item = items[i];
          if (item.index !== i) {
            const to_commit = {
              given_index: i,
              found_index: this.indexRuleFromId(item.id),
            };
            store.commit('PUT_INDEX', to_commit);
            const to_dispatch = {
              plant: this.plant.config_id,
              silo: item.silo_id,
              id: item.id,
              state: this.rules[to_commit.found_index],
            };
            store.dispatch('updateConstraint', to_dispatch);
          }
        }
      }
    },
    fillHourArray() {
      for (var i = 0; i <= 23; i++) {
        var hour = i + ':00';
        if (i < 10) hour = ['0', hour].join('');
        // set hour string for beginning and end
        if (i === this.defaultItem.hour_begin) this.string_begin = hour;
        if (i === this.defaultItem.hour_end) this.string_end = hour;
        this.hours.push(hour);
      }
    },
    formatHour(obj) {
      const hour = parseInt(obj.split(':')[0]);
      if (obj.begin) this.editedItem.hour_begin = hour;
      else this.editedItem.hour_end = hour;
    },
    onCloneCallback(item) {
      // Create a fresh copy of item
      const cloneMe = JSON.parse(JSON.stringify(item));
      return cloneMe;
    },
    onMoveCallback(evt, originalEvent) {
      const item = evt.draggedContext.element;
      if (item.locked) return false;
      return true;
    },
    onDropCallback(evt, originalEvent) {
      this.isDrag = false;
    },
    witchIsIt(name) {
      if (name.includes('Densité')) return ' T/m³';
      if (name.includes('Livraisons')) return ' camions(s)';
      if (name.includes('PCI')) return ' kWh/T';
      if (name.includes('Puissance')) return ' kWh';
      if (name.includes('Rendement') || name.includes('Seuil')) return ' %';
      if (name.includes('Volume')) return ' m³';
      return '';
    },
    setDialogBox(item) {
      this.editedItem.name = item;
      this.editedItem.hour_begin = this.editedItem.hour_begin;
      this.editedItem.hour_end = this.editedItem.hour_end;
      if (item.includes('Puissance')) {
        this.props.label = 'Puissance cogénération';
        this.props.suffix = 'kWh';
      }
      if (item.includes('PCI')) {
        this.props.label = 'PCI';
        this.props.suffix = 'kWh/T';
      }
      if (item.includes('Densité')) {
        this.props.label = 'Densité';
        this.props.suffix = 'T/m³';
      }
      if (item.includes('Volume maximal')) {
        this.props.label = 'Volume maximal';
        this.props.suffix = 'm³';
      }
      if (item.includes('Seuil')) {
        this.props.label = 'Seuil limite basse';
        this.props.suffix = '%';
      }
      if (item.includes('Livraisons minimales')) {
        this.props.label = 'Livraisons minimales';
        this.props.suffix = 'camions(s)';
      }
      if (item.includes('Livraisons maximales')) {
        this.props.label = 'Livraisons maximales';
        this.props.suffix = 'camions(s)';
      }
      if (item.includes('Volume moyen')) {
        this.props.label = 'Volume moyen biomasse';
        this.props.suffix = 'm³';
      }
      if (item.includes('Rendement')) {
        this.props.label = 'Rendement';
        this.props.suffix = '%';
      }
      if (item.includes('Puissance minimale')) {
        this.props.label = 'Puissance minimale';
        this.props.suffix = 'kW';
      }
      if (item.includes('Charge')) {
        this.props.label = 'Charge';
        this.props.suffix = '%';
      }
    },
    showDialog() {
      this.dialog = true;
    },

    // format plannig table date
    moment(date) {
      return moment(date, 'DD MMMM YYYY', 'fr');
    },
    isWeekend(str) {
      const date_str = str + ' 2022';
      const moment = this.moment(date_str);
      const date = new Date(moment);
      if (date.getDay() == 6 || date.getDay() == 0) {
        return true;
      }
    },
    itemRowBackground(item) {
      return this.isWeekend(item.DATE) ? 'week-end' : '';
    },

    formatDate(date) {
      if (!date) return null;
      const [year, month, day] = date.split('-');
      return `${day}/${month}/${year}`;
    },
    parseDate(date) {
      if (!date) return null;
      const [month, day, year] = date.split('/');
      return `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
    },
    getMainHeader(headers) {
      return headers.filter((i) => i.children);
    },
    getSubHeader(headers) {
      let result = [];
      headers
        .filter((i) => i.children)
        .forEach((v) => {
          result = result.concat(v.children);
        });
      return result;
    },
    hourToString(hour) {
      var hourString = hour + ':00';
      if (hour < 10) {
        hourString = 0 + hourString;
      }
      return hourString;
    },
    getRows(rows) {
      let result = {};
      let array = [];

      array.push(['name', rows.name]);
      array.push(['value', rows.value + this.witchIsIt(rows.name)]);
      array.push(['date_begin', this.formatDate(rows.date_begin)]);
      array.push(['hour_begin', this.hourToString(rows.hour_begin)]);
      array.push(['date_end', this.formatDate(rows.date_end)]);
      array.push(['hour_end', this.hourToString(rows.hour_end)]);

      array.forEach(function(item) {
        result[item[0]] = item[1];
      });
      return result;
    },
    async updateSnapshot() {
      const payload = {
        state: this.snapshot,
        silo_id: this.snapshot.silo_id,
        plant_id: this.plant.config_id,
      };
      await store.dispatch('updateSnapshot', payload);
    },
    async Actualize() {
      const payload = {
        user: this.user.id,
        config: this.config.id,
        refresh: true,
      };

      let planning = await store.dispatch('getStockBiomasse', payload); // non formatted object
      console.log('--- STOCK BIOMASSE ---');
      let planning_formated = Object.values(planning); // formatted array
      console.log(planning_formated);
      const appros_length = (Object.keys(planning_formated[0]).length - 1) / 2;
      const empty_array = Array.from({ length: appros_length }, () => Array.from({ length: planning_formated.length }, () => ({})));
      this.$store.commit('SET_APPRO', empty_array);

      for (let i = 0; i < planning_formated.length; i++) {
        let planning_cut = planning_formated[i];
        let planning_entries = Object.entries(planning_cut);
        for (let j = 1; j <= appros_length; j++) {
          console.log(j); // JLE
          console.log(appros_length); // JLE
          let object = {
            DATE: planning_entries.find((arr) => arr[0] === 'DATE')[1],
            NB_CAMIONS_1: planning_entries.find((arr) => arr[0] === `NB_CAMIONS_1_SILO${j}`)[1],
            NB_CAMIONS_2: planning_entries.find((arr) => arr[0] === `NB_CAMIONS_2_SILO${j}`)[1],
          };
          let payload = {
            date: i,
            silo: j - 1,
            planning: object,
          };
          this.$store.commit('ADD_APPRO', payload);
        }
      }
      payload.refresh = false;
      let demand = await store.dispatch('getPrevisionDemande', payload);
      console.log('--- PREVISION DEMANDE ---');
      let demand_formated = Object.values(demand);
      let demand_filtered = demand_formated.filter((value) => Date.parse(value.DATE) >= this.year_before);
      console.log(demand_filtered);
      for (let i = 0; i < demand_filtered.length; i++) {
        if (demand_filtered[i].DEMANDE === 'NaN') {
          let j = i;
          do {
            j++;
          } while (j < demand_filtered.length && demand_filtered[j].DEMANDE === 'NaN');
          if (j === demand_filtered.length) {
            do {
              j--;
            } while (j > 0 && demand_filtered[j].DEMANDE === 'NaN');
          }
          demand_filtered[i].DEMANDE = demand_filtered[j].DEMANDE;
        }
      }
      let demand_mapped = demand_filtered.map((item) => [Date.parse(item.DATE), item.DEMANDE]);
      store.commit('ADD_DEMAND', demand_mapped);

      let woodstock = await store.dispatch('getBesoinBiomasse', payload);
      console.log(woodstock);
      console.log('--- BESOIN BIOMASSE ---');
      store.commit('RESET_WOOD');
      let woodstock_formated = Object.values(woodstock);
      console.log(woodstock_formated);
      const woodstock_length = Object.keys(woodstock_formated[0]).length - 1;
      let woodstock_filtered = woodstock_formated.filter((value) => value.DATE >= this.year_before);
      for (let i = 0; i < woodstock_length; i++) {
        let woodstock_mapped = woodstock_filtered.map((item) => [item['DATE'], item[`VOLUME_ACTUEL${i + 1}`]]);
        store.commit('ADD_WOOD', woodstock_mapped);
      }

      let meteo = await store.dispatch('getPrevisionMeteo', payload);
      console.log('--- PREVISION METEO ---');
      let meteo_entries = Object.entries(meteo);
      console.log(meteo_entries);
      let meteo_filtered = meteo_entries.filter((entry) => entry[0] >= this.year_before);
      let meteo_mapped = meteo_filtered.map((item) => [parseInt(item[0]), item[1]['temp.fore']]);
      store.commit('ADD_METEO', meteo_mapped);
    },

    refreshMeteo() {
      store.dispatch('getPrevisionMeteo', true);
    },
    refreshPlanningAppro() {
      const payload = {
        refresh: true,
        id: this.user.id,
      };
      store.dispatch('getStockBiomasse', payload);
    },
    refreshDemande() {
      const payload = {
        id: this.user.id,
        refresh: true,
      };
      store.dispatch('getPrevisionDemande', payload);
    },
    refreshStockBois() {
      store.dispatch('getBesoinBiomasse', true);
    },

    getPrevisions() {
      const payload = {
        user: this.user.id,
        config: this.plant.config_id,
        show: true,
      };
      store.dispatch('getPrevisions', payload);
    },
    inputLevel(value) {
      store.commit('PUT_LEVEL', parseInt(value));
    },
    inputGoal(value) {
      store.commit('PUT_GOAL', parseInt(value));
    },

    inputConstraintLoad(load) {
      store.commit('PUT_LOAD', load.state);
      store.dispatch('updateConstraint', load.id);
    },
    inputConstraintMin(min) {
      store.commit('PUT_MIN', min.state);
      store.dispatch('updateConstraint', min.id);
    },
    inputConstraintMax(max) {
      store.commit('PUT_MAX', max.state);
      store.dispatch('updateConstraint', max.id);
    },
    inputConstraintStart(start) {
      store.commit('PUT_START', start.state);
      store.dispatch('updateConstraint', start.id);
    },
    inputConstraintEnd(end) {
      store.commit('PUT_END', end.state);
      store.dispatch('updateConstraint', end.id);
    },
    async removeConstraint(id) {
      store.dispatch('remConstraint', id);
    },
    async addConstraint() {
      let payload = {
        plant: this.user.id,
        silo: this.silo.id,
      };
      const rule = await store.dispatch('addConstraint', payload);
      for (const boiler of this.boilerList) {
        payload = {
          plant: this.user.id,
          rule: rule.id,
          boiler: boiler.id,
          value: boiler.load,
        };
        await store.dispatch('addBoilerLoad', payload);
      }
    },
    async setupPrevisions(id) {
      console.log('initializing previsions view');

      if (this.snapshots.length === 0) {
        console.log('adding snapshot values');
        let snapshots = await store.dispatch('getSnapshotList', id);
        if (this.silos.length > snapshots.length) {
          console.log('missing value(s)');
          for (let silo of this.silos) {
            let has_snapshot = snapshots.some((snapshot) => snapshot.silo_id === silo.id);
            if (!has_snapshot) {
              console.log('adding in silo ' + silo.id);
              await store.dispatch('addSnapshot', { index: this.silos.indexOf(silo), silo_id: silo.id });
            }
          }
        }
      }

      if (Object.keys(this.snapshot).length === 0) {
        this.snapshot = this.snapshots[this.silo_index];
      }

      for (let i = this.indexBeforeBoiler; i < this.boilerList.length; i++) {
        this.select_items.push(`Rendement de la chaudière ${i + 1}`);
        this.select_items.push(`Puissance minimale de la chaudière ${i + 1}`);
        this.select_items.push(`Charge de la chaudière ${i + 1}`);
      }

      this.defaultItem.silo_id = this.silo.id;
      this.editedItem.silo_id = this.silo.id;

      if (this.rules.length === 0) {
        console.log('adding rules list');
        await store.dispatch('getConstraintList', id);
      }

      this.loading = false;

      const payload = {
        user: this.user.id,
        config: this.config.id,
        refresh: false,
      };

      let planning = await store.dispatch('getStockBiomasse', payload); // non formatted object
      console.log('--- STOCK BIOMASSE ---');
      let planning_formated = Object.values(planning); // formatted array
      console.log(planning_formated);
      const appros_length = (Object.keys(planning_formated[0]).length - 1) / 2;
      const empty_array = Array.from({ length: appros_length }, () => Array.from({ length: planning_formated.length }, () => ({})));
      this.$store.commit('SET_APPRO', empty_array);

      for (let i = 0; i < planning_formated.length; i++) {
        let planning_cut = planning_formated[i];
        let planning_entries = Object.entries(planning_cut);
        for (let j = 1; j <= appros_length; j++) {
          let object = {
            DATE: new Date(planning_entries.find((arr) => arr[0] === 'DATE')[1]).toLocaleString('fr', { day: 'numeric', month: 'long' }),
            NB_CAMIONS_1: planning_entries.find((arr) => arr[0] === `NB_CAMIONS_1_SILO${j}`)[1],
            NB_CAMIONS_2: planning_entries.find((arr) => arr[0] === `NB_CAMIONS_2_SILO${j}`)[1],
          };
          let payload = {
            date: i,
            silo: j - 1,
            planning: object,
          };
          this.$store.commit('ADD_APPRO', payload);
        }
      }

      let demand = await store.dispatch('getPrevisionDemande', payload);
      console.log('--- PREVISION DEMANDE ---');
      let demand_formated = Object.values(demand);
      console.log(demand_formated);
      let demand_filtered = demand_formated.filter((value) => Date.parse(value.DATE) >= this.year_before);
      for (let i = 0; i < demand_filtered.length; i++) {
        if (demand_filtered[i].DEMANDE === 'NaN') {
          let j = i;
          do {
            j++;
          } while (j < demand_filtered.length && demand_filtered[j].DEMANDE === 'NaN');
          if (j === demand_filtered.length) {
            do {
              j--;
            } while (j > 0 && demand_filtered[j].DEMANDE === 'NaN');
          }
          demand_filtered[i].DEMANDE = demand_filtered[j].DEMANDE;
        }
      }
      let demand_mapped = demand_filtered.map((item) => [Date.parse(item.DATE), item.DEMANDE]);
      store.commit('ADD_DEMAND', demand_mapped);

      let woodstock = await store.dispatch('getBesoinBiomasse', payload);
      console.log('--- BESOIN BIOMASSE ---');
      let woodstock_formated = Object.values(woodstock);
      console.log(woodstock_formated);
      const woodstock_length = Object.keys(woodstock_formated[0]).length - 1;
      let woodstock_filtered = woodstock_formated.filter((value) => value.DATE >= this.year_before);
      for (let i = 0; i < woodstock_length; i++) {
        let woodstock_mapped = woodstock_filtered.map((item) => [item['DATE'], item[`VOLUME_ACTUEL${i + 1}`]]);
        store.commit('ADD_WOOD', woodstock_mapped);
      }

      let meteo = await store.dispatch('getPrevisionMeteo', payload);
      console.log('--- PREVISION METEO ---');
      let meteo_entries = Object.entries(meteo);
      console.log(meteo_entries);
      let meteo_filtered = meteo_entries.filter(
        (entry) => entry[0] >= this.demand[0][0] && entry[0] <= this.demand[this.demand.length - 1][0]
      );
      let meteo_mapped = meteo_filtered.map((item) => [parseInt(item[0]), item[1]['T_EXT']]);
      // meteo_mapped.forEach((element) => {
      //   if (element[1] === null) {
      //     element[1] = Math.floor(Math.random() * (31 - 14 + 1) + 14);
      //   }
      // });
      store.commit('ADD_METEO', meteo_mapped);
      this.setItemSelect();
    },
    async redoConfiguration() {
      store.commit('SET_COMPL', 2);
      await store.dispatch('updateUser');
      this.$router.push('/configuration/donnees-chaufferie');
    },
    changeSelectedSilo(index) {
      store.commit('changeSelectedSilo', index);
    },
    changeSelectedBoiler(index) {
      store.commit('changeSelectedBoiler', index);
    },
    isActiveSilo(index) {
      this.activeSiloBtn = `silo${index}`;
      console.log(this.activeBtn);
    },
    isActiveBoiler(index) {
      this.activeBoilerBtn = `boiler${index}`;
    },
    // TABLE related
    editItem(item) {
      this.editedIndex = this.ruleList.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },
    deleteItem(item) {
      this.editedIndex = this.ruleList.indexOf(item);
      this.editedItem = Object.assign({}, item);
      // Note : for deletion confirmation decomment next line and remove what's under
      this.dialogDelete = true;
      // store.dispatch('remConstraint', this.rule_payload);
      // this.closeDelete();
    },
    deleteItemConfirm() {
      store.dispatch('remConstraint', this.rule_payload);
      const loads = this.loadList(this.rule_payload.id);
      for (const load of loads) {
        store.commit('REM_LOAD', load.id);
      }
      this.Actualize();
      this.closeDelete();
    },
    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },
    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },
    async save() {
      if (this.editedItem.name.includes('Livraisons')) {
        if (this.editedItem.time_begin === 'Matin') this.editedItem.hour_begin = 9;
        else this.editedItem.hour_begin = 14;
        if (this.editedItem.time_end === 'Matin') this.editedItem.hour_end = 14;
        else this.editedItem.hour_end = 19;
      }
      if (this.editedIndex > -1) {
        store.dispatch('updateConstraint', this.rule_payload);
        const rule = this.editedItem;
        const boilers_length = this.boilerList.length;
        const values = Object.values(rule.loads.children);
        const loads = this.loadList(rule.id);
        const loads_mapped = loads.map((el) => el.id);
        const boilers = this.boilerList;
        const boilers_mapped = boilers.map((el) => el.id);
        for (let i = 0; i < boilers_length; i++) {
          const payload = {
            boiler_id: boilers_mapped[i],
            rule_id: rule.id,
            id: loads_mapped[i],
            plant_id: this.plant.user_id,
            value: values[i],
          };
          store.dispatch('updateBoilerLoad', payload);
        }
      } else {
        await store.dispatch('addConstraint', this.rule_payload);
      }
      this.Actualize();
      this.close();
    },
    setItemSelect() {
      var index = this.indexBeforeBoiler;
      let items = [
        {
          action: 'wood',
          title: `Caractéristiques du bois`,
          items: [{ title: 'Densité' }, { title: 'PCI' }],
        },
      ];
      for (let i = 0; i < this.boilerList.length; i++) {
        items.push({
          action: 'boiler',
          title: `Chaudière ${index + 1}`,
          active: true,
          items: [{ title: 'Charge' }, { title: 'Puissance minimale' }, { title: 'Rendement de la chaudière' }],
        });
        index++;
      }
      const to_push = [
        {
          action: 'cogeneration',
          title: `Cogénération`,
          items: [{ title: 'Puissance' }],
        },
        {
          action: 'delivery',
          title: `Données de livraison biomasse`,
          items: [
            { title: 'Livraisons maximales sur la demi-journée' },
            { title: 'Livraisons minimales sur la demi-journée' },
            { title: 'Volume moyen par camion' },
          ],
        },
        {
          action: 'silo',
          title: `Silo ${this.silo_index + 1}`,
          items: [{ title: 'Niveau minimum' }, { title: 'Volume maximal' }],
        },
      ];
      for (const item of to_push) {
        items.push(item);
      }
      this.items = items;
    },
  },
  computed: {
    activeHeaders() {
      return this.headers.filter((h) => {
        if (!this.allowDrag && h.text === '') {
          return false;
        }
        return true;
      });
    },
    startDate() {
      return this.editedItem.date_begin;
    },
    startDateDisp() {
      const string_start = this.editedItem.date_begin;
      const string_end = this.editedItem.date_end;
      const date_begin = new Date(string_start);
      const date_end = new Date(string_end);
      if (date_end < date_begin) {
        this.editedItem.date_end = string_start;
      }
      return this.formatDate(this.editedItem.date_begin);
    },
    endDateDisp() {
      return this.formatDate(this.editedItem.date_end);
    },
    rule_payload() {
      return {
        plant: this.plant.config_id,
        silo: this.editedItem.silo_id,
        id: this.editedItem.id,
        state: this.editedItem,
      };
    },
    snap_load() {
      return {
        state: this.snapshot,
        silo_id: this.snapshot.silo_id,
        plant_id: this.plant.user_id,
      };
    },
    store() {
      return this.$store.state;
    },
    ...mapState([
      'user',
      'plant',
      'silos',
      'silo_index',
      'snapshots',
      'rules',
      'boilers',
      'loads',
      'appros',
      'woods',
      'meteos',
      'plannings',
      'config',
    ]),
    ...mapState({
      silo: (state) => state.silos[state.silo_index],
      planning: (state) => state.plannings[state.silo_index],
      wood: (state) => state.woods[state.silo_index],
      appro: (state) => state.appros[state.silo_index],
      demand: (state) => state.demands[0],
      meteo: (state) => state.meteos[0],
    }),
    ...mapGetters(['ruleList', 'boilerList', 'indexFirstBoiler', 'loadList', 'loadListFromSilo', 'indexRuleFromId']),
    indexBeforeBoiler() {
      return this.indexFirstBoiler(this.silo.id);
    },
  },
  watch: {
    ruleList() {
      this.sortedRules = this.ruleList.sort((a, b) => parseInt(a.index) - parseInt(b.index));
      this.defaultItem.index = this.ruleList.length;
    },
    snapshots() {
      if (this.snapshots.length > 0 && Object.keys(this.snapshot).length === 0) {
        this.snapshot = this.snapshots[this.silo_index];
      }
    },
    defaultItem(next, prev) {
      if (prev.date_begin !== next.date_begin) {
        this.dateFormatted = this.formatDate(this.date);
      }
    },
    silo_index() {
      this.snapshot = this.snapshots[this.silo_index];
      this.setItemSelect();
    },
    silo(_, silo) {
      if (silo && Object.keys(silo).length > 0) {
        this.defaultItem.silo_id = this.silo.id;
        this.editedItem.silo_id = this.silo.id;
      }
    },
    planning(_, planning) {
      if (planning && Object.keys(planning).length > 0) {
        this.defaultItem.drop_min = this.planning.drop_min;
        this.defaultItem.drop_max = this.planning.drop_max;
        this.editedItem.drop_min = this.planning.drop_min;
        this.editedItem.drop_max = this.planning.drop_max;
      }
    },
    appro() {
      const mornings = this.appro.map((el) => el.NB_CAMIONS_1);
      const noons = this.appro.map((el) => el.NB_CAMIONS_2);
      this.total_morning = mornings.reduce((partial_sum, current_num) => partial_sum + current_num, 0);
      this.total_afternoon = noons.reduce((partial_sum, current_num) => partial_sum + current_num, 0);
    },
    config(present, previous) {
      if (previous.compl === undefined && present.compl === 3) {
        this.setupPrevisions(present.id);
      }
    },
    // TABLE related
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete();
    },
  },
};
</script>

<style scoped>
.action-divider {
  background-color: darkgray;
  margin: 5px;
}

.grab-icon {
  cursor: none;
}
.grab-icon:hover {
  cursor: grab;
}

.no-drag {
  cursor: not-allowed !important;
}
.snapshot-title,
.planning-title,
.tool-title {
  letter-spacing: 0.1em;
  font-weight: bold;
  text-shadow: 1px 1px 1px rgba(0, 0, 0, 0.1);
}

/* PLANNING */

.planning-mornings,
.planning-noons {
  border-right: white solid 1px !important;
}

.planning-mornings,
.planning-noons,
.planning-total {
  text-transform: uppercase;
  text-align: center !important;
  color: white;
  background-color: #00aaff !important;
  letter-spacing: 0.1em;
}

.snapshot-inputs {
  padding: 0em 1em 0.5em 1em;
}

.v-data-table th {
  background-color: #e6e6e6;
}

.v-data-table,
table,
.v-card {
  border-radius: 0px !important;
}

.v-btn .v-icon {
  margin-left: 0.5em;
}

.main-content {
  height: calc(100vh - 97px);
  width: 100%;
  overflow: none;
  background-color: rgb(254, 254, 254);
}

.snapshot-card {
  border: #00aaff 1px solid !important;
}

.planning-table {
  margin-top: 0px !important;
  padding-top: 0px !important;
  background-color: transparent !important;
  border: 1px solid #e6e6e6 !important;
}

.chart-row .theme--light.v-card {
  background-color: transparent;
}
.biomass-chart {
  padding-right: 8px !important;
}

.prevision-chart {
  padding-left: 8px !important;
}

.card-col,
.main-col {
  overflow-y: auto;
  height: calc(100vh - 97px);
}

.card-col {
  border-right: solid lightgrey 2px;
}

.rule-table.v-data-table {
  background-color: transparent;
}
.test-btn {
  background-color: white;
}

.add-btn {
  height: 2.9em !important;
  border: none;
}

.dialog-title {
  font-weight: bold;
  letter-spacing: 0.1em !important;
  border-left: 0.2em solid #00aaff;
  padding-left: 0.5em;
}

.menu-text {
  letter-spacing: 0.025em;
}

.vertical-divider {
  background-color: darkgray;
  height: inherit;
}

.switch {
  width: 0px;
}

.td-actions {
  width: 10em;
}
</style>
