import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)
Vue.config.devtools = true

const state = {
  token: localStorage.getItem('token') !== null ? localStorage.getItem('token') : 'none',
  isLoggedin: false,
  lang: ((window.navigator.languages && window.navigator.languages[0]) ||
  window.navigator.language ||
  window.navigator.userLanguage ||
  window.navigator.browserLanguage).includes('ja') ? 'ja' : 'en',
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
  current_lang (state) {
    return state.lang
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
  set_lang (state, lang) {
    state.lang = lang
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
  toggle_lang ({ commit, state }) {
    commit('set_lang', state.lang === 'ja' ? 'en' : 'ja')
  }
}

export default new Vuex.Store({
  state,
  getters,
  mutations,
  actions
})
