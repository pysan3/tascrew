import Axios from 'axios'
export default {
  methods: {
    assign2Company (companycode) {
      return Axios.post(process.env.VUE_APP_BASE_URL + '/api/assigncompany', {
        token: this.$store.getters.current_token,
        companycode: companycode
      }).then(response => {
        return response.data.isValid
      }).catch(() => {
        return false
      })
    }
  }
}
