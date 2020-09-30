<template>
  <div id="headerDefault" class="header-default">
    <b-navbar toggleable="sm" type="dark" variant="dark" sticky="true">
      <b-navbar-brand to="/" class="mr-auto px-2">{{ $t('Message.title') }}</b-navbar-brand>
      <b-navbar-nav>
        <b-nav-item-dropdown>
          <template slot="button-content">{{ project_name }}</template>
        </b-nav-item-dropdown>
      </b-navbar-nav>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item v-show="is_loggedin" to="/project">Home</b-nav-item>
          <b-nav-item v-show="is_loggedin" to="/calendar">Calendar</b-nav-item>
          <b-nav-item v-show="is_loggedin" to="/tasks">Tasks</b-nav-item>
          <b-nav-item v-show="is_loggedin" to="/board">Board</b-nav-item>
          <b-nav-item v-show="is_loggedin" to="/chart">Chart</b-nav-item>
          <b-nav-item v-show="is_loggedin" to="/members">Members</b-nav-item>
          <b-nav-item v-show="is_loggedin" to="/settings">Setting</b-nav-item>
          <b-nav-item v-show="!is_loggedin" to="/tryaccess/login">Login</b-nav-item>
          <b-nav-item v-show="!is_loggedin" to="/tryaccess/signup">Signup</b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav class="ml-auto">
          <b-nav-item>Bell</b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav>
          <b-nav-item-dropdown right id="user-dropdown">
            <template slot="button-content">{{ user_name }}</template>
            <b-dropdown-item to="/">UserHome</b-dropdown-item>
            <b-dropdown-item v-if="!is_loggedin" to="/tryaccess/login">login</b-dropdown-item>
            <b-dropdown-item v-if="!is_loggedin" to="/tryaccess/signup">signup</b-dropdown-item>
            <!-- <b-dropdown-item v-if="is_loggedin" to="/settings">MyProjects</b-dropdown-item> -->
            <b-dropdown-item v-if="is_loggedin" to="/usersettings">UserSetting</b-dropdown-item>
            <b-dropdown-item to="/customerservice">Customer Service</b-dropdown-item>
            <b-dropdown-item to="/help">Help</b-dropdown-item>
            <b-dropdown-item to="/feedback"><b>開発者へメッセージ</b></b-dropdown-item>
            <b-dropdown-item v-if="is_loggedin" @click="logout()"><b>Log out</b></b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
import Axios from 'axios'
export default {
  props: [
    'is_loggedin'
  ],
  data () {
    return {
      user_name: 'Anonymous'
    }
  },
  methods: {
    logout () {
      localStorage.removeItem('token')
      this.$store.commit('set_token', 'none')
      this.$store.commit('set_loggedin', false)
      this.user_name = 'Anonymous'
      this.$router.push('/').catch(err => {}) // eslint-disable-line
    }
  },
  watch: {
    is_loggedin: function (to, from) { // eslint-disable-line no-unused-vars
      if (to) {
        Axios.post(process.env.VUE_APP_BASE_URL + '/api/username', {
          token: this.$store.getters.current_token
        }).then(response => {
          this.user_name = response.data.user_name
        })
      } else {
        this.user_name = 'Anonymous'
      }
    }
  }
}
</script>
