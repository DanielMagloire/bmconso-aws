<template>
  <div>
    <highcharts :constructorType="'stockChart'" :options="chartOptions" />
  </div>
</template>

<script>
/* eslint-disable */
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
  name: 'histoChart',
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
          text: 'HISTORIQUE DEMANDE',
          align: 'center',
          style: {
            fontWeight: 'bold',
          },
        },
        subtitle: {
          text: '',
          align: 'center',
        },

        yAxis: [
          {
            min: 0,
            title: {
              text: 'Puissance en kW',
            },
            labels: {
              format: '{value}',
              style: {
                color: Highcharts.getOptions().colors[1],
              },
            },
          },
        ],
        tooltip: {
          shared: true,
        },
        rangeSelector: {
          verticalAlign: 'top',
          x: 0,
          y: 0,
          inputPosition: {
            align: 'left',
            x: 0,
            y: 0,
          },
          buttonPosition: {
            align: 'right',
            x: 0,
            y: 0,
          },
          buttons: [
            {
              type: 'day',
              count: 1,
              text: '1j',
            },
            {
              type: 'week',
              count: 1,
              text: '1s',
            },
            {
              type: 'month',
              count: 1,
              text: '1m',
            },
            {
              type: 'month',
              count: 6,
              text: '6m',
            },
            {
              type: 'year',
              count: 1,
              text: '1a',
            },
            {
              type: 'all',
              text: 'Tout',
            },
          ],
          selected: 2,
          inputDateFormat: '%e %b %Y %H:%M',
        },
        navigator: {
          margin: 60,
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
            data: store.state.hist_heat,
            yAxis: 0,
            tooltip: {
              valueDecimals: 1,
              valueSuffix: 'kW',
            },
            color: Highcharts.getOptions().colors[1],
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
