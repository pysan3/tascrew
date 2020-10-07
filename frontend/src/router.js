import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '@/store'
import mixin from '@/mixin'
const mixins = mixin.methods

Vue.use(VueRouter)

const routerOptions = [
  { path: '/', component: 'Home', requiredAuth: false },
  { path: '/tryaccess/:page', component: 'TryAccess', requiredAuth: false },
  { path: '/calendar/:id?', component: 'Calendar', requiredAuth: true, checkHashID: true },
  { path: '/tasks/:id?', component: 'Tasks', requiredAuth: true, checkHashID: true },
  { path: '/board/:id?', component: 'Board', requiredAuth: true, checkHashID: true },
  { path: '/chart/:id?', component: 'Chart', requiredAuth: true, checkHashID: true },
  { path: '/members/:id?', component: 'Members', requiredAuth: true, checkHashID: true },
  { path: '/company/:id', component: 'CompanyHome', requiredAuth: true, checkHashID: true },
  { path: '/project/:id', component: 'ProjectHome', requiredAuth: true, checkHashID: true },
  { path: '/user/:id?', component: 'UserHome', requiredAuth: true, checkHashID: true },
  { path: '/addcompany', component: 'AddCompany', requiredAuth: true },
  { path: '/addproject', component: 'AddProject', requiredAuth: true },
  { path: '/companysettings/:id', component: 'CompanySettings', requiredAuth: true, checkHashID: true },
  { path: '/projectsettings/:id', component: 'ProjectSettings', requiredAuth: true, checkHashID: true },
  { path: '/usersettings', component: 'UserSettings', requiredAuth: true },
  { path: '/feedback', component: 'Feedback', requiredAuth: false },
  { path: '*', component: 'NotFound', requiredAuth: false }
]

const routes = routerOptions.map(route => ({
  path: route.path,
  name: route.component.toLowerCase(),
  component: () => import(`@/views/${route.component}.vue`),
  meta: {
    requiredAuth: route.requiredAuth === true,
    checkHashID: route.checkHashID === true
  }
}))

const router = new VueRouter({
  // mode: 'history',
  routes
})

const checkHashIDFunc = async id => {
  if (mixins.$_checkValidHashID(id)) return true
  else {
    await mixins.$_refreshValidHashID([mixins.$_decodeHashID(id).type])
    return mixins.$_checkValidHashID(id)
  }
}

router.beforeEach(async (to, from, next) => { // eslint-disable-line no-unused-vars
  if (to.matched.some(record => record.meta.requiredAuth)) {
    if (!(await mixins.$_checkIsLoggedin())) { // check if login is needed
      to.query['nexturl'] = to.path
      next({
        name: 'tryaccess',
        params: { page: 'login' },
        query: to.query
      })
      return
    } else if (to.name !== 'addcompany' && store.getters.getValidAccess['company'].length === 0) {
      await mixins.$_refreshValidHashID(['company'])
      if (store.getters.getValidAccess['company'].length === 0) {
        next('/addcompany')
        return
      }
    }
  }
  if (to.matched.some(record => record.meta.checkHashID)) {
    if (to.params.id && !(await checkHashIDFunc(to.params.id))) { // check if this project/company/user is valid
      alert('invalid project id')
      next({
        name: 'notfound'
      })
      return
    }
  }
  next()
})

export default router
