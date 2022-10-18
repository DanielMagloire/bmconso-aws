# bmconso

> A Vue.js web-app starter project

## Prerequisites

- An account on [GitLab](https://gitlab.engie-cofely.net/)
- [Git](https://git-scm.com/downloads), with [the correct configuration](https://genesismobile.atlassian.net/wiki/spaces/SO/pages/290226284/GIT#GIT-D%C3%A9marrer)
- [NodeJS](https://nodejs.org/en/download/) (If you run into problem with the latest LTS version, install the [10.14.2](https://nodejs.org/dist/v10.14.2/))
- Set your `HTTP_PROXY` and `HTTPS_PROXY` environment variable if needed
- (Optional but **strongly recommended**) Install [vue-devtools](https://github.com/vuejs/vue-devtools)

## Create an app based on this starter

- Create your app's new repo on [Gitlab](https://gitlab.engie-cofely.net/). Let's say you call it **{app-repo-name}**. Do not add a README.md
- Copy your new repository remote URL (let's call it **{app-repo-remote-url}**. It should be something like `https://gitlab.engie-cofely.net/{app-repo-name}.git`)
- Open a terminal where you want to create a work folder for your new app
- `git clone https://gitlab.engie-cofely.net/vuejs/app-starter.git {app-repo-name}`
- `cd {app-repo-name}`
- `git remote set-url origin {app-repo-remote-url}`
- `git push origin master -u`
- Your `master` branch is now initialized with the code of the `app-starter`

To go further (setup Okta, etc...), see **_Rework the `app-starter` to create your own app_** in the [Internal documentation section](#internal-documentation).

## Build Setup

```bash
# install dependencies
npm install

# format, then serve with hot reload at localhost:8080
npm run dev # or 'npm start'

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report # or 'npm run build && npm run open:report'

# run all tests
npm run test
```

The build configuration is designed to be robust and require little to no adjustment from developers, except regarding the libraries that your application depends on (See the `INTERNAL_LIBS` and `PURE_ESM_LIBS` constants in `./build/libs.js`).

To change browser compatibility, modify `browserslist` in `package.json` (See the [syntax to use](https://github.com/browserslist/browserslist)).

For a more detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).

## Other commands

```bash
# lint all the code
npm run lint

# format all the code according to standard rules
npm run format

# run all tests and show the test report in your browser
npm run test && npm run open:test-report

# run all tests and show the test coverage report in your browser
npm run test && npm run open:coverage
```

## Debug...

### ...the application

On your browser, you can use the real source to set breakpoints after [enabling the use of Source Maps](https://gist.github.com/jakebellacera/336c4982194bcb02ef8a).

- In Safari, go to the `Debug` tab, then to `Source`. You can search for a particular file via the search bar on the bottom left of the tab.
- In Chrome, go to the `Sources` tab, then to `webpack://`. You can use `⌘+P` to search for a particular file.

Please take the time to learn how to use [vue-devtools](https://alligator.io/vuejs/vue-devtools/)

### ...all automated tests

You can debug all tests by following the steps below:

1. Set a breakpoint in a test file or files.

2. Go to the Debug view, select the **'Jest All'** configuration, then press F5 or click the green play button.

3. Your breakpoint will now be hit.

> **Note**: Your breakpoint may not be hit on the first run. If it isn't hit, you can rerun the tests by pressing `a` at the prompt in the Terminal. Or, by adding a `debugger` statement to the top of the script (this just gives vscode time to process the script's sourcemaps when it is loaded).

![all](https://github.com/Microsoft/vscode-recipes/blob/master/debugging-jest-tests/all.gif?raw=true)

## ...the current automated test

You can debug the test you're editing by following the steps below:

1. Set a breakpoint in a test file.

2. Go to the Debug view, select the **'Jest Current File'** configuration, then press F5 or click the green play button.

3. Your breakpoint will now be hit. (If not, see **Note** above).

![current](https://github.com/Microsoft/vscode-recipes/blob/master/debugging-jest-tests/current.gif?raw=true)

[Link to the original VSCode recipe for Jest debugging in VSCode](https://github.com/Microsoft/vscode-recipes/tree/master/debugging-jest-tests).

## Usefull links

### Internal documentation

- [The Cofely's VueJs documentation](https://genesismobile.atlassian.net/wiki/spaces/SO/overview)
- [Rework the `app-starter` to create your own app](https://genesismobile.atlassian.net/wiki/spaces/SO/pages/290160646/Initialiser+une+application+depuis+le+starter)
- [Development Guidelines](https://genesismobile.atlassian.net/wiki/spaces/SO/pages/290193437/Guidelines+v1)
- [Suggested Git Workflow](https://genesismobile.atlassian.net/wiki/spaces/SO/pages/290226284/GIT)
- [VS Code introduction (and recommended configuration)](https://genesismobile.atlassian.net/wiki/spaces/PGM/pages/174456860/Visual+Studio+Code) (URL will change)
- [JavaScript learning materials](https://genesismobile.atlassian.net/wiki/spaces/SO/pages/290160702/Formation)

### External documentation

#### Libraries

- [Vue.js](https://vuejs.org/v2/guide/)
- [Vuex](https://vuex.vuejs.org/)
- [Vuetify](https://vuetifyjs.com/en/getting-started/quick-start)
- [material-design-icons-iconfont](https://jossef.github.io/material-design-icons-iconfont/)
- [Axios](https://github.com/axios/axios#readme)
- [Okta-vue](https://github.com/okta/okta-oidc-js/tree/master/packages/okta-vue#readme)
- [Lodash](https://lodash.com/docs/4.17.11) (**Important**: import function by function. _Example_: `import debounce from 'lodash/debounce';`)

#### Tools

- [Vue-devtools](https://github.com/vuejs/vue-devtools) ([Quick introduction](https://alligator.io/vuejs/vue-devtools/))
- [Webpack](https://webpack.js.org/concepts/)
- [Jest](https://jestjs.io/docs/en/getting-started.html)
- [ESLint](https://eslint.org/docs/user-guide/configuring)
- [Prettier](https://prettier.io/docs/en/index.html)

## Upgrade VUETIFY

npm upgrade vuetify
npm install sass sass-loader fibers deepmerge -D
