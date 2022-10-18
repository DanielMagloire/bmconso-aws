/* eslint-disable */
export default {
  SET_USERS(state, users) {
    state.users = users;
  },
  SET_USER(state, user) {
    state.user = user;
  },
  ADD_USER(state, user) {
    state.users.push(user);
  },
  SET_AUTH(state, subentication) {
    state.user.subentication = subentication;
  },
  SET_COMPL(state, completion) {
    state.user.completion = completion;
  },
};
