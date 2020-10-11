<template>
  <div id="calendarapi">
    <h3 class="text-center py-3 px-4 border-bottom">{{ $t('Settings.calendarapi') }}</h3>
    <div class="text-center" v-if="!has_google">
      <h4>{{ $t('Settings.getauth') }}</h4>
      <button class="btn btn-info btn-lg" @click="getAuthCode">{{ $t('Settings.getauthbtn') }}</button>
    </div>
    <div v-if="has_google">
      <h4 class="my-3">{{ $t('Settings.setprivacy') }}</h4>
      <div v-for="c in calendar_list" :key="c" class="d-flex border-top py-2">
        <div class="d-block text-truncate align-self-center"><b>{{ c.summary }}</b></div>
        <div class="d-block text-truncate align-self-center flex-grow-1">{{ c.description }}</div>
        <div>
          <b-dropdown right>
            <template v-slot:button-content>
              {{ privacy_msg[c.privacy_level] }}
            </template>
            <b-dropdown-item v-for="(msg, index) in privacy_msg" :key="index" @click="changeLevel(c, index)">
              {{ msg }}
            </b-dropdown-item>
          </b-dropdown>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Axios from 'axios'
export default {
  data () {
    return {
      has_google: false,
      calendar_list: [],
      privacy_msg: [
        this.$t('Settings.privacy_level_public'),
        this.$t('Settings.privacy_level_private')
      ]
    }
  },
  methods: {
    getAuthCode () {
      this.$gAuth.getAuthCode().then(authCode => {
        Axios.post(process.env.VUE_APP_BASE_URL + '/auth/googlecalendar', {
          code: authCode,
          redirect_uri: 'postmessage',
          token: this.$store.getters.current_token
        }).then(response => {
          if (response.data) {
            this.has_google = response.data.success
            if (this.has_google) {
              this.getCalendarList()
            }
          }
        }).catch(error => {
          alert(`Error: ${error}`)
        })
      })
    },
    getCalendarList () {
      if (!this.has_google) return
      Axios.post(process.env.VUE_APP_BASE_URL + '/google/getmycalendars', {
        token: this.$store.getters.current_token
      }).then(response => {
        this.calendar_list = response.data.calendarList
        this.$forceUpdate()
      })
    },
    changeLevel (calendar, level) {
      if (calendar.privacy_level === level) return
      Axios.post(process.env.VUE_APP_BASE_URL + '/setting/calendarprivacylevel', {
        token: this.$store.getters.current_token,
        c_id: calendar.id,
        new_level: level
      }).then(response => {
        if (!response.data.isValid) alert(this.$t('Error.plzreload'))
      }).catch(error => {
        alert(this.$t('Error.error') + error + this.$t('Error.plzreload'))
      })
      calendar.privacy_level = level
      this.$forceUpdate()
    }
  },
  mounted () {
    Axios.post(process.env.VUE_APP_BASE_URL + '/auth/hasgoogle', {
      token: this.$store.getters.current_token
    }).then(response => {
      this.has_google = response.data.isValid
      if (this.has_google) {
        this.getCalendarList()
      }
    })
  }
}
</script>
