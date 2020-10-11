import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)
Vue.config.devtools = true

const state = {
  token: localStorage.getItem('token') !== null ? localStorage.getItem('token') : 'none',
  isLoggedin: false,
  accessType: [
    'company',
    'project',
    'user'
  ],
  validAccess: {},
  accessInfo: {},
  accessData: {}
}

const getters = {
  current_token (state) {
    return state.token
  },
  is_loggedin (state) {
    return state.isLoggedin
  },
  getValidAccess (state) {
    return Object.fromEntries(state.accessType.map(e => [e, state.validAccess[e] || []]))
  },
  getAccessInfo (state) {
    return state.accessInfo
  },
  getAccessData (state) {
    return state.accessData
  }
}

const mutations = {
  set_token (state, token) {
    state.token = token
  },
  set_loggedin (state, bool) {
    state.isLoggedin = bool
  },
  setValidAccess (state, { type, value }) {
    Vue.set(state.validAccess, type, value)
  },
  setAccessInfo (state, { hash, value }) {
    Vue.set(state.accessInfo, hash, value)
  },
  setAccessData (state, { hash, value }) {
    Vue.set(state.accessData, hash, value)
  }
}

const actions = {
}

export default new Vuex.Store({
  state,
  getters,
  mutations,
  actions
})
