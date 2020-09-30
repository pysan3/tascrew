<template>
  <div id="feedback">
    <textarea id="feedback" cols="30" rows="10" v-model="feedback"></textarea>
    <button class="btn btn-dark" @click="send_feedback()">Send</button>
  </div>
</template>

<script>
import Axios from 'axios'
export default {
  data () {
    return {
      feedback: ''
    }
  },
  methods: {
    send_feedback () {
      if (this.feedback.length === 0) {
        alert('文字を入力してください')
        return
      }
      Axios.post(process.env.VUE_APP_BASE_URL + '/api/feedback', {
        token: this.$store.getters.current_token,
        feedback: this.feedback
      }).then(() => {
        alert(this.$t('Message.fbthx'))
        this.$router.push('/')
      })
    }
  }
}
</script>
