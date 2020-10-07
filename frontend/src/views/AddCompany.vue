<template>
  <div id="addcompany">
    <h1>会社登録</h1>
    <div v-for="key of Object.keys(company_data)" :key="key">
      <input type="text" v-model="company_data[key]">
    </div>
    <div>
      <h3>他の管理者</h3>
      <textarea v-model="hidden_status.sub_admin" cols="30" rows="3"></textarea>
      <h3>社員</h3>
      <textarea v-model="hidden_status.members" cols="30" rows="3"></textarea>
    </div>
    <div>
      <button class="btn btn-primary" @click="submitData()">Create</button>
    </div>
  </div>
</template>

<script>
import Axios from 'axios'
export default {
  data () {
    return {
      company_data: {
        company_name: '株式会社LinkX',
        department: 'department',
        employee_number: 0,
        zipcode: '000-0000',
        address: '住所',
        email: 'hogehoge@example.com',
        phone_number: '000-0000-0000'
      },
      hidden_status: {
        sub_admin: '',
        members: ''
      }
    }
  },
  methods: {
    submitData () {
      this.company_data.employee_number = parseInt(this.company_data.employee_number)
      Axios.post(process.env.VUE_APP_BASE_URL + '/api/createcompany', Object.assign({}, this.company_data, {
        token: this.$store.getters.current_token,
        sub_admin: this.splitMembers(this.hidden_status.sub_admin),
        members: this.splitMembers(this.hidden_status.members)
      })).then(async response => {
        if (response.data.isValid) {
          await this.$_refreshValidHashID(['company', 'user'])
          this.$router.push({
            name: 'companysettings',
            params: { id: response.data.accesshash }
          })
        }
      }).catch(error => {
        if (process.env.NODE_ENV !== 'production') alert(error)
      })
    },
    splitMembers (s) {
      if (s.length <= 0) return []
      else {
        return s.split(' ').filter(e => this.$_decodeHashID(e).type === 'user')
      }
    }
  }
}
</script>
