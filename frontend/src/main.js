import Vue from 'vue'
import App from '@/App.vue'
import router from '@/router'
import store from '@/store'
import dictionary from '@/lang/dictionary.json'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import VueI18n from 'vue-i18n'
import GAuth from 'vue-google-oauth2'

const gauthOption = {
  clientId: '77701347155-oc5bqd2mfkof8oiukmg2hu6rkd4hqedt.apps.googleusercontent.com',
  scope: 'https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/userinfo.email openid https://www.googleapis.com/auth/userinfo.profile',
  prompt: 'select_account'
}

Vue.use(GAuth, gauthOption)
Vue.use(BootstrapVue)
Vue.use(VueI18n)
Vue.config.productionTip = true

const i18n = new VueI18n({
  locale: ((window.navigator.languages && window.navigator.languages[0]) || window.navigator.language || window.navigator.userLanguage || window.navigator.browserLanguage).includes('ja') ? 'ja' : 'en',
  fallbackLocale: 'ja',
  messages: dictionary
})

const checkHashID = async (id) => {
  if (store.dispatch('checkValidHashID', id)) return true
  else {
    await store.dispatch('refreshValidHashID', store.dispatch('decodeHashID', id).type)
    return store.dispatch('checkValidHashID', id)
  }
}

router.beforeEach(async (to, from, next) => { // eslint-disable-line no-unused-vars
  if (to.matched.some(record => record.meta.requiredAuth) && !store.getters.is_loggedin) {
    if (!(await store.dispatch('checkIsLoggedin'))) { // check if login is needed
      to.query['nexturl'] = to.path
      next({
        name: 'tryaccess',
        params: { page: 'login' },
        query: to.query
      })
      return
    }
  }
  if (to.matched.some(record => record.meta.checkHashID) && to.params.id) {
    if (!(await checkHashID(to.params.id))) { // check if this project/company/user is valid
      alert('invalid project id')
      next({
        name: 'notfound'
      })
      return
    }
  }
  next()
})

new Vue({
  i18n,
  router,
  store,
  render: h => h(App)
}).$mount('#app')
