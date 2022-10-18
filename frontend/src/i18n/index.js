import Vue from 'vue';
import VueI18n from 'vue-i18n';
import locale from 'locale2';
import messages from './messages';

Vue.use(VueI18n);

const vueI18n = new VueI18n({
  locale: locale.split('-')[0] || 'fr', // get current language tag RFC 5646
  messages,
});

export default vueI18n;
