<template>
  <div>
    <highcharts :options="chartOptions" />
  </div>
</template>

<script>
/* eslint-disable */
import { mapState } from 'vuex';
import { Chart } from 'highcharts-vue';
import Highcharts from 'highcharts';
import HighchartsMore from 'highcharts/highcharts-more';
import store from '../store/index';

HighchartsMore(Highcharts);

export default {
  props: ['options'],
  components: {
    highcharts: Chart,
  },
  name: 'demandChart',
  data() {
    return {
      chartOptions: Highcharts.merge(this.options, {
        chart: {
          backgroundColor: 'rgba(0,0,0,0)',
        },
        legend: {
          align: 'center',
          verticalAlign: 'top',
        },
        credits: {
          enabled: false,
        },
        title: {
          text: 'PRÉVISION METEO & DEMANDE',
          align: 'center',
          style: {
            fontWeight: 'bold',
          },
        },
        subtitle: {
          text: 'Sur les dix prochains jours',
          align: 'center',
        },

        yAxis: [
          {
            min: 0,
            title: {
              text: '',
            },
            labels: {
              format: '{value}',
              style: {
                color: Highcharts.getOptions().colors[0],
              },
            },
            tickInterval: 500,
          },
          {
            min: 0,
            labels: {
              format: '{value}',
              style: {
                color: Highcharts.getOptions().colors[2],
              },
            },
            title: {
              text: '',
            },
            tickInterval: 5,
            opposite: true,
          },
        ],
        tooltip: {
          shared: true,
        },
        xAxis: {
          crosshair: true,
          type: 'datetime',
          dateTimeLabelFormats: {
            day: '%e. %b',
          },
          tickInterval: 864e5,
          title: {
            text: '',
          },
          lineWidth: 1,
        },
        series: [
          {
            name: 'demande réseau en kW',
            marker: {
              enabled: false,
            },
            data: store.state.demands[store.state.silo_index],
            yAxis: 0,
            tooltip: {
              valueSuffix: ' kW',
              valueDecimals: 0,
            },
            color: Highcharts.getOptions().colors[0],
          },
          {
            color: Highcharts.getOptions().colors[2],
            name: 'température extérieure en °C',
            marker: {
              enabled: false,
            },
            data: store.state.meteos[store.state.silo_index],
            yAxis: 1,
            tooltip: {
              valueSuffix: ' °C',
              valueDecimals: 0,
            },
          },
        ],
      }),
    };
  },
};
</script>

<style scoped>
div {
  height: 100%;
}
</style>
