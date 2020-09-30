import Vue from 'vue'
import VueRouter from 'vue-router'
Vue.use(VueRouter)

const routerOptions = [
  { path: '/', component: 'Home', requiredAuth: false },
  { path: '/tryaccess/:page', component: 'TryAccess', requiredAuth: false },
  { path: '/usersettings/:menu?', component: 'UserSettings', requiredAuth: true },
  { path: '/calendar/:id?', component: 'Calendar', requiredAuth: true, checkHashID: true },
  { path: '/tasks/:id?', component: 'Tasks', requiredAuth: true, checkHashID: true },
  { path: '/board/:id?', component: 'Board', requiredAuth: true, checkHashID: true },
  { path: '/chart/:id?', component: 'Chart', requiredAuth: true, checkHashID: true },
  { path: '/members/:id?', component: 'Members', requiredAuth: true, checkHashID: true },
  { path: '/settings/:id?', component: 'Settings', requiredAuth: true, checkHashID: true },
  { path: '/project/:id?', component: 'ProjectHome', requiredAuth: true, checkHashID: true },
  { path: '/company/:id?', component: 'CompanyHome', requiredAuth: true, checkHashID: true },
  { path: '/user/:id?', component: 'UserHome', requiredAuth: true, checkHashID: true },
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

export default new VueRouter({
  // mode: 'history',
  routes
})
