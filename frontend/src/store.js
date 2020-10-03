import Vue from 'vue'
import Vuex from 'vuex'
import Hashids from 'hashids'
import Axios from 'axios'

Vue.use(Vuex)

const state = {
  token: localStorage.getItem('token') !== null ? localStorage.getItem('token') : 'none',
  isLoggedin: false,
  lang: ((window.navigator.languages && window.navigator.languages[0]) ||
  window.navigator.language ||
  window.navigator.userLanguage ||
  window.navigator.browserLanguage).includes('ja') ? 'ja' : 'en',
  accessType: [
    'project',
    'company',
    'user'
  ],
  validAccess: {}
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
    return state.validAccess
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
    state.validAccess[type] = value
  }
}

const actions = {
  toggle_lang ({ commit, state }) {
    commit('set_lang', state.lang === 'ja' ? 'en' : 'ja')
  },
  decodeHashID ({ state }, { hash }) {
    const data = (new Hashids(process.env.HASHID_SALT, 10)).decode(hash)
    if (data.length !== 2 || data[1] >= state.accessType.length) return undefined
    else {
      return {
        id: data[0], // TODO: maybe we don't need this
        type: state.accessType[data[1]]
      }
    }
  },
  checkValidHashID ({ getters, dispatch }, { hash }) {
    return getters.getValidAccess[dispatch('decodeHashID', hash).type].includes(hash)
  },
  async refreshValidHashID ({ commit, getters }, types) {
    console.log(types)
    if (!Array.isArray(types)) { // only needed for debugging
      if (process.env.NODE_ENV !== 'production') alert('refreshValidHashID got a non-array object')
      return
    }
    if (types.length === 0) return
    return Axios.post(process.env.VUE_APP_BASE_URL + `/api/validhashid/${types.join('-')}`, {
      token: getters.current_token
    }).then(response => {
      response.data.forEach(e => {
        commit('setValidAccess', {
          type: e.type,
          value: e.data
        })
      })
    })
  },
  checkIsLoggedin ({ commit, getters }) {
    if (getters.current_token === 'none') return false
    return Axios.post(process.env.VUE_APP_BASE_URL + '/api/loggedin', {
      token: getters.current_token
    }).then(response => {
      if (response.data.isValid) {
        commit('set_loggedin', true)
        return true
      } else return false
    }).catch(error => {
      if (process.env.NODE_ENV !== 'production') alert(error)
      return false
    })
  }
}

export default new Vuex.Store({
  state,
  getters,
  mutations,
  actions
})
