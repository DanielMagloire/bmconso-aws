import boilerplateMessageFr from './boilerplate/fr-FR';
import boilerplateMessageEn from './boilerplate/en-US';
import homeMessageFr from './home/fr-FR';
import homeMessageEn from './home/en-US';
import fr from './fr-FR';
import en from './en-US';

const messages = {
  fr: {
    message: {
      boilerplate: boilerplateMessageFr,
      home: homeMessageFr,
      ...fr.message,
    },
    route: fr.route,
  },
  en: {
    message: {
      boilerplate: boilerplateMessageEn,
      home: homeMessageEn,
      ...en.message,
    },
    route: en.route,
  },
};

export default messages;
