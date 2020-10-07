import store from '@/store'
import Hashids from 'hashids'
import Axios from 'axios'
export default {
  methods: {
    $_assign2Company (code) {
      return Axios.post(process.env.VUE_APP_BASE_URL + '/api/assign', {
        token: store.getters.current_token,
        accesshash: code
      }).then(response => {
        return response.data.isValid && (this.$_decodeHashID(code).type === 'company')
      }).catch(() => {
        return false
      })
    },
    $_decodeHashID (hash) {
      if (hash === undefined) return undefined
      const data = (new Hashids(process.env.HASHID_SALT, 10)).decode(hash)
      if (data.length !== 2 || data[1] >= store.state.accessType.length) return undefined
      else {
        return {
          id: data[0], // TODO: maybe we don't need this
          type: store.state.accessType[data[1]]
        }
      }
    },
    $_generateURL (pagetype, accesshash) {
      const accessdata = this.$_decodeHashID(accesshash)
      if (pagetype === '' || pagetype === 'settings') {
        pagetype = (accessdata === undefined ? 'user' : accessdata.type) + pagetype
      }
      return `/${pagetype}` + (accesshash === undefined ? '' : `/${accesshash}`)
    },
    $_checkValidHashID (hash) {
      return store.getters.getValidAccess[this.$_decodeHashID(hash).type].includes(hash)
    },
    $_refreshValidHashID (types) {
      if (!Array.isArray(types)) { // only needed for debugging
        // alert('refreshValidHashID got a non-array object')
        if (types === 'all') types = ['all']
        else return
      }
      if (types.length === 0) return
      return Axios.post(process.env.VUE_APP_BASE_URL + `/api/validhashid/${types.join('-')}`, {
        token: store.getters.current_token
      }).then(response => {
        response.data.forEach(e => {
          store.commit('setValidAccess', {
            type: e.type,
            value: e.data
          })
        })
      }).catch(error => {
        if (process.env.NODE_ENV !== 'production') alert(error)
      })
    },
    $_checkIsLoggedin () {
      if (store.getters.current_token === 'none') return false
      else if (store.getters.is_loggedin) return true
      return Axios.post(process.env.VUE_APP_BASE_URL + '/api/loggedin', {
        token: store.getters.current_token
      }).then(response => {
        if (response.data.isValid) {
          store.commit('set_loggedin', true)
          return true
        } else return false
      }).catch(error => {
        if (process.env.NODE_ENV !== 'production') alert(error)
        return false
      })
    },
    $_accessInformation (hash) {
      if (hash === undefined) return undefined
      else if (store.state.accessDict[hash] !== undefined) return store.state.accessDict[hash]
      return Axios.post(process.env.VUE_APP_BASE_URL + '/api/fetchaccessdata', {
        token: store.getters.current_token,
        accesshash: hash
      }).then(response => {
        store.commit('setAccessDict', {
          type: hash,
          value: response.data
        })
        return response.data
      }).catch(() => undefined)
    }
  }
}
