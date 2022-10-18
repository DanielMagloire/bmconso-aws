/* eslint-disable */

import Vue from 'vue';
import Router from 'vue-router';
import Layout from '@/layouts/default';

// import Okta Vue SDK
import Auth from '@okta/okta-vue';

// import okta callback
import implicitCallback from '@/components/boilerplate/implicitCallback';

// import error page
import errorPage from '@/components/boilerplate/errorPage';

// set Okta Configuration
Vue.use(Auth, {
  issuer: process.env.OKTA_ISSUER,
  clientId: process.env.OKTA_CLIENT_ID,
  redirectUri: process.env.OKTA_REDIRECT_URL,
  scopes: ['openid', 'profile', 'email'],
  responseType: ['id_token'],
});

Vue.use(Router);

// const RouteContainer = () => import('@/layouts/routeContainer.vue');
const PageNotFound = () => import('@/pages/NotFound.vue');

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/implicit/callback',
      component: implicitCallback,
    },
    {
      path: '/error',
      name: 'error',
      component: errorPage,
    },
    {
      path: '*',
      name: 'AllPath',
      redirect: {
        path: '/404',
      },
    },
    {
      path: '/404',
      name: 'NotFound',
      component: PageNotFound,
    },
    {
      path: '/',
      name: 'Root',
      component: Layout,
      meta: {
        requiresAuth: true,
      },
      children: [
        {
          path: 'profil',
          name: 'Profil',
          component: () => import('../views/Profile.vue'),
          meta: {
            title: 'profil',
            icon: 'profil',
          },
        },
        {
          path: '/configuration',
          name: 'configuration',
          component: () => import('../views/Setting.vue'),
          children: [
            {
              path: 'station-meteo',
              name: 'Meteo',
              component: () => import('../views/Location.vue'),
            },
            {
              path: 'demande-reseau',
              name: 'Reseau',
              component: () => import('../views/Network.vue'),
            },
            {
              path: 'donnees-chaufferie',
              name: 'Chaufferie',
              component: () => import('../views/HeatingPlant.vue'),
            },
          ],
        },
        {
          path: '/historique',
          name: 'Historique',
          component: () => import('../views/Historic.vue'),
        },
        {
          path: '/previsions',
          name: 'Previsions',
          component: () => import('../views/Previsions.vue'),
        },
      ],
    },
  ],
});

router.beforeEach(Vue.prototype.$auth.authRedirectGuard());

export default router;

// import Vue from 'vue';
// import Router from 'vue-router';
// import Layout from '@/layouts/default';

// // import Okta Vue SDK
// import Auth from '@okta/okta-vue';

// // import okta callback
// import implicitCallback from '@/components/boilerplate/implicitCallback';

// // import error page
// import errorPage from '@/components/boilerplate/errorPage';

// // set Okta Configuration
// Vue.use(Auth, {
//   issuer: process.env.OKTA_ISSUER,
//   clientId: process.env.OKTA_CLIENT_ID,
//   redirectUri: process.env.OKTA_REDIRECT_URL,
//   scopes: ['openid', 'profile', 'email'],
//   responseType: ['id_token'],
// });

// Vue.use(Router);

// const PageNotFound = () => import(/* webpackChunkName: "NotFound" */ '@/pages/NotFound.vue');

// const router = new Router({
//   mode: 'history',
//   routes: [
//     {
//       path: '/implicit/callback',
//       component: implicitCallback,
//     },
//     {
//       path: '/error',
//       name: 'error',
//       component: errorPage,
//     },
//     {
//       path: '*',
//       name: 'AllPath',
//       redirect: {
//         path: '/404',
//       },
//     },
//     {
//       path: '/404',
//       name: 'NotFound',
//       component: PageNotFound,
//     },
//     {
//       path: '/',
//       name: 'Root',
//       component: Layout,
//       redirect: {
//         name: 'Meteo',
//       },

//       // Activate Protected Route
//       // Routes are protected by the authRedirectGuard, which verifies
//       // there is a valid accessToken or idToken stored.
//       // To ensure the user has been authenticated before accessing your route,
//       // activate the requiresAuth metadata:
//       meta: {
//         requiresAuth: true,
//       },
//       children: [
//         {
//           path: '/configuration',
//           name: 'configuration',
//           component: () => import('../views/Configuration.vue'),
//           children: [
//             {
//               path: 'station-meteo',
//               name: 'Meteo',
//               component: () => import('../views/Meteo.vue'),
//             },
//             {
//               path: 'demande-reseau',
//               name: 'Reseau',
//               component: () => import('../views/Reseau.vue'),
//             },
//             {
//               path: 'donnees-chaufferie',
//               name: 'Chaufferie',
//               component: () => import('../views/Chaufferie.vue'),
//             },
//           ],
//         },
//         {
//           path: '/previsions',
//           name: 'Previsions',
//           component: () => import('../views/Previsions.vue'),
//         },
//       ],
//     },
//   ],
// });

// router.beforeEach(Vue.prototype.$auth.authRedirectGuard());

// export default router;
