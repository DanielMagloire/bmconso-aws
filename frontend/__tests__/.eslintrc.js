module.exports = {
  extends: ['plugin:jest/recommended'],
  env: {
    browser: true,
    jest: true,
    'jest/globals': true,
  },
  rules: {
    'global-require': 0,
    'no-console': 0,
  },
  plugins: ['jest'],
};
