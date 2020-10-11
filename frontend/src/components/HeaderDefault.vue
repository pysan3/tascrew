<template>
  <div id="headerDefault" class="header-default">
    <b-navbar toggleable="md" type="dark" variant="dark" sticky>
      <b-navbar-brand to="/" class="mr-auto px-2">{{ $t('Pagename.title') }}</b-navbar-brand>
      <b-navbar-nav v-show="is_loggedin" @click="chooseproject = !chooseproject">
        <b-nav-item class="font-weight-bold" style="min-width: 128px;">
          <span style="display: inline-block; min-width: 112px;">
            {{ project_name }}
          </span>
          <!-- pull down icon -->
          <!-- <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-caret-down" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" d="M3.204 5L8 10.481 12.796 5H3.204zm-.753.659l4.796 5.48a1 1 0 0 0 1.506 0l4.796-5.48c.566-.647.106-1.659-.753-1.659H3.204a1 1 0 0 0-.753 1.659z"/>
          </svg> -->
          <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-caret-down-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
            <path d="M7.247 11.14L2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"/>
          </svg>
        </b-nav-item>
      </b-navbar-nav>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item v-show="is_loggedin" :to="$_generateURL('', $route.params.id)">{{ $t('Pagename.home') }}</b-nav-item>
          <b-nav-item v-show="is_loggedin" :to="$_generateURL('calendar', $route.params.id)">{{ $t('Pagename.calendar') }}</b-nav-item>
          <b-nav-item v-show="is_loggedin" :to="$_generateURL('tasks', $route.params.id)">{{ $t('Pagename.tasks') }}</b-nav-item>
          <b-nav-item v-show="is_loggedin" :to="$_generateURL('board', $route.params.id)">{{ $t('Pagename.board') }}</b-nav-item>
          <b-nav-item v-show="is_loggedin" :to="$_generateURL('chart', $route.params.id)">{{ $t('Pagename.chart') }}</b-nav-item>
          <b-nav-item v-show="is_loggedin && !isFriendsPage()" :to="$_generateURL('members', $route.params.id)">{{ $t('Pagename.members') }}</b-nav-item>
          <b-nav-item v-show="is_loggedin && !isFriendsPage()" :to="$_generateURL('settings', $route.params.id)">{{ $t('Pagename.settings') }}</b-nav-item>
          <b-nav-item v-show="!is_loggedin" to="/tryaccess/login">{{ $t('Pagename.login') }}</b-nav-item>
          <b-nav-item v-show="!is_loggedin" to="/tryaccess/signup">{{ $t('Pagename.signup') }}</b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav class="ml-auto">
          <b-nav-item v-show="is_loggedin">(Bell)</b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav>
          <b-nav-item-dropdown right id="user-dropdown">
            <template slot="button-content">{{ user_name }}</template>
            <b-dropdown-item to="/user">{{ $t('Store.accessType_user') + $t('Pagename.home') }}</b-dropdown-item>
            <b-dropdown-item v-if="!is_loggedin" to="/tryaccess/login">{{ $t('Pagename.login') }}</b-dropdown-item>
            <b-dropdown-item v-if="!is_loggedin" to="/tryaccess/signup">{{ $t('Pagename.signup') }}</b-dropdown-item>
            <!-- <b-dropdown-item v-if="is_loggedin" to="/settings">MyProjects</b-dropdown-item> -->
            <b-dropdown-item v-if="is_loggedin" to="/usersettings">{{ $t('Store.accessType_user') + $t('Pagename.settings') }}</b-dropdown-item>
            <b-dropdown-item to="/customerservice">{{ $t('Pagename.customerservice') }}</b-dropdown-item>
            <b-dropdown-item to="/help">{{ $t('Pagename.help') }}</b-dropdown-item>
            <b-dropdown-item to="/feedback"><b>{{ $t('Pagename.feedback') }}</b></b-dropdown-item>
            <b-dropdown-item v-if="is_loggedin" @click="logout()"><b>{{ $t('Pagename.logout') }}</b></b-dropdown-item>
            <b-dropdown-divider></b-dropdown-divider>
            <b-dropdown-item>
              <div class="d-flex justify-content-around">
                <img v-for="locale of $i18n.availableLocales" :key="locale" :src="`/static/img/languages/${locale}.jpg`" @click="$i18n.locale = locale" class="language-flag">
              </div>
            </b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <ChooseProject v-if="is_loggedin" v-show="chooseproject" @togglechoise="chooseproject = !chooseproject"/>
    <ProfileBar v-if="is_loggedin"/>
  </div>
</template>

<script>
import ChooseProject from '@/components/ChooseProject'
import ProfileBar from '@/components/ProfileBar'
import Axios from 'axios'
export default {
  components: {
    ChooseProject,
    ProfileBar
  },
  props: [
    'is_loggedin'
  ],
  data () {
    return {
      user_name: this.$t('Message.anonymoususername'),
      project_name: 'very_long_project_name',
      chooseproject: false
    }
  },
  methods: {
    logout () {
      localStorage.removeItem('token')
      this.$store.commit('set_token', 'none')
      this.$store.commit('set_loggedin', false)
      this.user_name = this.$t('Message.anonymoususername')
      this.$router.push('/').catch(err => {}) // eslint-disable-line
    },
    isFriendsPage () {
      return (this.$route.params.id !== undefined) && (this.$_decodeHashID(this.$route.params.id).type === 'user')
    }
  },
  watch: {
    is_loggedin: function (to, from) { // eslint-disable-line no-unused-vars
      if (to) {
        Axios.post(process.env.VUE_APP_BASE_URL + '/api/username', {
          token: this.$store.getters.current_token
        }).then(response => {
          this.user_name = response.data.user_name
        }).catch(error => {
          if (process.env.NODE_ENV !== 'production') alert(error)
        })
        this.$_refreshValidHashID('all')
      } else {
        this.user_name = this.$t('Message.anonymoususername')
      }
    },
    '$route': async function () {
      const info = await this.$_accessInformation(this.$route.params.id)
      if (['addproject', 'addcompany', 'user'].includes(this.$route.name)) {
        this.project_name = ''
      } else if (info !== undefined) {
        this.project_name = info.name
      } else {
        this.project_name = this.$t('Message.all')
      }
      this.$forceUpdate()
    }
  }
}
</script>

<style lang="stylus" scoped>
img.language-flag
  height 1em
  vertical-align bottom
</style>
