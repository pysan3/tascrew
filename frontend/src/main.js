import Vue from 'vue'
import App from '@/App.vue'
import router from '@/router'
import store from '@/store'
import mixin from '@/mixin'
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

Vue.mixin(mixin)
Vue.use(GAuth, gauthOption)
Vue.use(BootstrapVue)
Vue.use(VueI18n)
Vue.config.productionTip = true
Vue.config.devtools = true

const i18n = new VueI18n({
  locale: ((window.navigator.languages && window.navigator.languages[0]) || window.navigator.language || window.navigator.userLanguage || window.navigator.browserLanguage).includes('ja') ? 'ja' : 'en',
  fallbackLocale: 'ja',
  messages: dictionary
})

new Vue({
  i18n,
  router,
  store,
  render: h => h(App)
}).$mount('#app')
