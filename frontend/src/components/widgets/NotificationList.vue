<template>
  <v-card class="elevation-0">
    <v-card-title dense color="transparent">
      <h4>Notification</h4>
    </v-card-title>
    <v-divider></v-divider>
    <v-card-text class="pa-0">
      <v-list two-line class="pa-0">
        <template v-for="(item, index) in items">
          <v-subheader v-if="item.header" :key="item.header">{{ item.header }}</v-subheader>
          <v-divider v-else-if="item.divider" :key="index"></v-divider>
          <v-list-item v-else :key="item.title" @click="handleClick">
            <v-list-item-avatar :color="item.color">
              <v-icon dark>{{ item.icon }}</v-icon>
            </v-list-item-avatar>
            <v-list-item-content v-html="item.title"></v-list-item-content>
            <v-list-item-action class="caption">
              {{ item.timeLabel }}
            </v-list-item-action>
          </v-list-item>
        </template>
      </v-list>
      <v-divider></v-divider>
      <v-btn block text class="ma-0">All</v-btn>
      <v-divider></v-divider>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  data: () => ({
    items: [
      {
        title: 'New notification from server',
        color: 'red',
        icon: 'laptop_windows',
        timeLabel: 'Just now',
      },
      { divider: true, inset: true },
      {
        title: 'New order received',
        color: 'light-blue',
        icon: 'card_travel',
        timeLabel: '2 min ago',
      },
      { divider: true, inset: true },
      {
        title: 'Successfull registring ',
        color: 'light-green',
        icon: 'offline_pin',
        timeLabel: '1 hour ago',
      },
    ],
  }),
  methods: {
    handleClick: (e) => {
      // eslint-disable-next-line
      console.log(e);
    },
  },
};
</script>
