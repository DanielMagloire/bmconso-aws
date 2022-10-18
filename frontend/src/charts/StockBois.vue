<template>
  <div>
    <highcharts ref="chart" :options="chartOptions" />
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
  name: 'woodStockChart',
  data() {
    return {
      chartOptions: Highcharts.merge(this.options, {
        chart: {
          backgroundColor: 'rgba(0,0,0,0)',
        },
        credits: {
          enabled: false,
        },
        title: {
          text: 'ÉVOLUTION STOCK DE BOIS',
          align: 'center',
          style: {
            fontWeight: 'bold',
          },
        },
        subtitle: {
          text: 'Sur les dix prochains jours',
          align: 'center',
        },
        legend: {
          enabled: false,
        },
        yAxis: {
          title: {
            text: 'Niveau du stock en m³',
          },
          labels: {
            format: '{value}',
          },
          tickInterval: 10,
        },
        xAxis: {
          crosshair: true,
          type: 'datetime',
          dateTimeLabelFormats: {
            minute: '%H:%M',
          },
          tickInterval: 36e5,
          title: {
            text: '',
          },
          tickPositioner() {
            var data = store.state.woods[store.state.silo_index];
            var data_maped = data.map((item) => item[0]);
            var positions = [];
            for (let tick of data_maped) {
              var datetime = new Date(tick);
              let isEleven = () => datetime.getHours() === 11 && datetime.getMinutes() === 0;
              let isMidnight = () => datetime.getHours() === 0 && datetime.getMinutes() === 0;
              if (isEleven() || isMidnight()) {
                positions.push(tick);
              }
            }
            return positions;
          },
          labels: {
            formatter() {
              var label = this.axis.defaultLabelFormatter.call(this);
              if (label === '00:00') {
                label = `${Highcharts.dateFormat('%e %b', this.value)}`;
              }
              return label;
            },
          },
          lineWidth: 1,
        },
        series: [
          {
            name: 'besion biomasse',
            marker: {
              enabled: false,
            },
            data: store.state.woods[store.state.silo_index],
            tooltip: {
              valueSuffix: ' m³',
              valueDecimals: 0,
            },
          },
        ],
      }),
    };
  },
  computed: {
    ...mapState({
      woodstock: (state) => state.woods[state.silo_index],
    }),
  },
  watch: {
    woodstock() {
      this.$refs.chart.chart.series[0].setData(this.woodstock, true);
    },
  },
};
</script>

<style scoped>
div {
  height: 100%;
}
</style>
