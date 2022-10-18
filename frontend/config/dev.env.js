'use strict';
const merge = require('webpack-merge');
const prodEnv = require('./prod.env');

module.exports = merge(prodEnv, {
    NODE_ENV: '"development"',
    BASE_URL_EXT: '"https://{host}:{port}"',
    BASE_URL_INT: '"http://127.0.0.1:8000/bmconso/api/v1/"',
    OKTA_ISSUER: '"https://engieapppreview.oktapreview.com/oauth2/default"',
    // datagora non prod
    OKTA_CLIENT_ID: '"0oa293yt6dkwcA1Rj0i7"',
    OKTA_REDIRECT_URL: '"http://localhost:8080/implicit/callback"',
});
