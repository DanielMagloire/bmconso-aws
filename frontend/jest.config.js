const libs = require('./build/libs');

module.exports = {
  verbose: true,
  browser: true,
  clearMocks: true,
  collectCoverage: true,
  globals: {
    __DEV__: true,
  },
  rootDir: '.',
  moduleNameMapper: {
    '^vue$': 'vue/dist/vue.common.js',
    '@/(.*)$': '<rootDir>/src/$1',
  },
  testRegex: '/__tests__/.*.test.js$',
  coverageDirectory: '__tests__/test-reports/coverage/',
  collectCoverageFrom: [
    '<rootDir>/src/**/*.{js,jsx,vue}',
    '!<rootDir>/tests/**',
    '!<rootDir>/**/boilerplate/**',
    '!<rootDir>/**/*boilerplate*',
    '!<rootDir>/node_modules/**',
  ],
  reporters: [
    'default',
    [
      'jest-junit',
      {
        outputDirectory: '__tests__/test-reports/',
      },
    ],
    [
      'jest-html-reporter',
      {
        outputPath: '__tests__/test-reports/report.html',
        includeFailureMsg: true,
        includeConsoleLog: true,
      },
    ],
  ],
  transform: {
    '^.+\\.js$': 'babel-jest',
  },
  transformIgnorePatterns: [`<rootDir>${libs.buildGlobExcluding(libs.PURE_ESM_LIBS)}`],
};
