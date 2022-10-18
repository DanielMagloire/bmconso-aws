// Internal libraries. Must be the full names, or a RegExp using only .* wildcard.
const INTERNAL_LIBS = ['genesis.*'];
// All EcmaScript libraries, including our internal libraries and third party ones. Must be the full names, or a RegExp using only .* wildcard.
const PURE_ESM_LIBS = [...INTERNAL_LIBS];

/**
 * @returns Utility to get RegExp or Glob patterns of the libraries in use in the genesis stack.
 */
module.exports = {
    /**
     * Array of matchers all the our own internal libraries.
     */
    INTERNAL_LIBS,

    /**
     * List of matchers for all the libraries that we use, internal or not, written in vanilla EcmaScript 6+
     * and exposed as ES modules. Therefor those need to be transpiled.
     */
    PURE_ESM_LIBS,

    /**
     * Build a RegExp that matches a list of libraries in node_modules.
     * @param {Array<string>} libs The libraries to match. Each should be a string that represents a RegExp.
     * See INTERNAL_LIBS or PURE_ES6PLUS_LIBS for example.
     * @returns {RegExp} The RegExp
     */
    buildRegExpIncluding(libs) {
        return new RegExp(`/node_modules/?(${libs.join('|')})/.*`);
    },

    /**
     * Build a RegExp that matches all the libraries in node_modules except the given libraries in parameter.
     * @param {Array<string>} libs The libraries to exclude from the match. Each should be a string that represents a RegExp.
     * See INTERNAL_LIBS or PURE_ES6PLUS_LIBS for example.
     * @returns {RegExp} The RegExp
     */
    buildRegExpExcluding(libs) {
        return new RegExp(`/node_modules/(?!(${libs.join('|')})/).*`);
    },

    /**
     * Build a Glob pattern that matches a list of libraries in node_modules.
     * @param {Array<string>} libs The libraries to match. Each should be a string that represents a RegExp (LIMITATION: only use '.*' for wildcards).
     * See INTERNAL_LIBS or PURE_ES6PLUS_LIBS for example.
     * @returns {string} The Glob pattern
     */
    buildGlobIncluding(libs) {
        return `/node_modules/?(${libs.map(toGlob).join('|')})/`;
    },

    /**
     * Build a Glob pattern that matches all the libraries in node_modules except the given libraries in parameter.
     * @param {Array<string>} libs The libraries to exclude from the match. Each should be a string that represents a RegExp (LIMITATION: only use '.*' for wildcards).
     * See INTERNAL_LIBS or PURE_ES6PLUS_LIBS for example.
     * @returns {string} The Glob pattern
     */
    buildGlobExcluding(libs) {
        return `/node_modules/!(${libs.map(toGlob).join('|')})/`;
    },
};

function toGlob(regExpString) {
    return regExpString.replace('.*', '*');
}
