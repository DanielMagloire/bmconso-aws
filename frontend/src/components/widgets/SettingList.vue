<template>
  <v-list class="pa-0" elevation="1">
    <v-subheader>
      <v-icon class="mr-3">account_circle</v-icon>
      {{ user ? user.name : generateMessage('boilerplate.unknown_user') }}
    </v-subheader>
    <v-divider></v-divider>
    <v-list-item v-for="(item, index) in items" @click="item.click" ripple="ripple" rel="noopener" :key="index">
      <v-list-item-action v-if="item.icon">
        <v-icon>{{ item.icon }}</v-icon>
      </v-list-item-action>
      <v-list-item-content>
        <v-list-item-title>{{ generateMessage(item.title) }}</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
  </v-list>
</template>

<script>
import { mapGetters } from 'vuex';
import { generateMessage } from '@/utils/i18n';

export default {
  name: 'c-setting-list',
  data: () => ({
    languages: [
      {
        value: 'en',
        label: 'English',
        icon: 'https://countryflags.io/us/flat/24.png',
      },
      {
        value: 'fr',
        label: 'Français',
        icon: 'https://countryflags.io/fr/flat/24.png',
      },
    ],
    items: [],
  }),
  created() {
    this.setItem();
  },
  computed: {
    authenticated: {
      get() {
        return this.isAuthenticated();
      },
      set(val) {
        const loginItem = this.items.find((obj) => obj.id === 'login');
        loginItem.title = val ? 'boilerplate.logout' : 'boilerplate.login';
        loginItem.click = val ? this.logout : this.login;
      },
    },
    ...mapGetters({ user: 'global/user' }),
    ...mapGetters({ darkThemeEnabled: 'boilerplate/darkThemeEnabled' }),
    ...mapGetters({ scrollOffNavbarEnabled: 'boilerplate/scrollOffNavbarEnabled' }),
  },
  watch: {
    darkThemeEnabled(enabled) {
      const themeItem = this.items.find((obj) => obj.id === 'theme');
      themeItem.title = this.getThemeTitle(enabled);
    },
    scrollOffNavbarEnabled(enabled) {
      const themeItem = this.items.find((obj) => obj.id === 'scrollOffNavbar');
      themeItem.title = this.getScrollOffNavbarTitle(enabled);
    },
  },
  methods: {
    setItem() {
      this.items = [
        {
          id: 'login',
          icon: 'exit_to_app',
          href: '#',
          title: 'boilerplate.logout',
          click: this.logout,
        },
      ];
    },
    async isAuthenticated() {
      this.authenticated = await this.$auth.isAuthenticated();
    },
    toggleDarkTheme() {
      this.$store.dispatch('boilerplate/toggleDarkTheme');
    },
    toggleScrollOffNavbar() {
      this.$store.dispatch('boilerplate/toggleScrollOffNavbar');
    },
    async logout() {
      this.$store.dispatch('global/setUser', null);
      this.$store.dispatch('boilerplate/setAuthenticated', false);
      try {
        await this.$auth.logout();
        await this.isAuthenticated();
      } catch (error) {
        // logout function do 2 things sequencely
        // at first clearing localStorage and second destroying user session on server
        // if origin are not allowed cors error will be raised
        // this leads to clearing localStorage but not destroying session
        // to fix the issue origin most be declared on the trusted oring in okta org
        // this fix are juste for not blocking vue js app
        await this.isAuthenticated();
      }
    },
    async login() {
      this.$store.dispatch('boilerplate/setAuthenticated', true);
      await this.$auth.loginRedirect('/');
      await this.isAuthenticated();
    },
    setLanguage(language) {
      this.$store.dispatch('boilerplate/setLanguage', language);
    },
    getThemeTitle(darkThemeEnabled) {
      return darkThemeEnabled ? 'boilerplate.light' : 'boilerplate.dark';
    },
    getScrollOffNavbarTitle(scrollOffNavbarEnabled) {
      return scrollOffNavbarEnabled ? 'boilerplate.scrollOffNavbarOff' : 'boilerplate.scrollOffNavbarOn';
    },
    generateMessage,
  },
};
</script>
