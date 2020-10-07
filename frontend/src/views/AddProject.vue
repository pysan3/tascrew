<template>
  <div id="addproject">
    <h1>プロジェクト作成</h1>
    <div v-for="key of Object.keys(project_data)" :key="key">
      <input type="text" v-model="project_data[key]">
    </div>
    <div>
      <h3>紐付けるプロジェクト</h3>
      <b-form-select v-model="hidden_status.tree" :options="master_list">
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
      project_data: {
        project_name: 'tascrew実装',
        schedule_privacy_level: 'TODO',
        chart_color: 'TODO'
      },
      hidden_status: {
        tree: this.$route.query.parent || 'private',
        sub_admin: '',
        members: ''
      },
      master_list: [
        { value: 'private', text: 'my own project' }
      ]
    }
  },
  methods: {
    submitData () {
      Axios.post(process.env.VUE_APP_BASE_URL + '/api/createproject', Object.assign({}, this.project_data, {
        token: this.$store.getters.current_token,
        tree: this.hidden_status.tree,
        sub_admin: this.splitMembers(this.hidden_status.sub_admin),
        members: this.splitMembers(this.hidden_status.members)
      })).then(async response => {
        if (response.data.isValid) {
          await this.$_refreshValidHashID(['project', 'user'])
          this.$router.push({
            name: 'projectsettings',
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
  },
  async created () {
    const tmpList = [...this.master_list]
    await Promise.all(this.$store.getters.getValidAccess.company.map(async e => {
      const data = await this.$_accessInformation(e)
      tmpList.push({
        value: e,
        html: data.name
      })
    }).concat(this.$store.getters.getValidAccess.project.map(async e => {
      const data = await this.$_accessInformation(e)
      tmpList.push({
        value: `${data.tree}/${e}`,
        html: '&nbsp;&nbsp;&nbsp;&nbsp;'.repeat((data.tree.match(/\//g) || []).length + 1) + data.name
      })
    }))).then(() => {
      const dig = (node, s, value) => {
        if (node[s[0]] === undefined) {
          node[s[0]] = {
            value: undefined,
            children: {}
          }
        }
        if (s.length === 1) node[s[0]].value = value
        else dig(node[s[0]].children, s.slice(1), value)
      }
      const rise = (node, target) => {
        Object.entries(node).forEach(([k, v]) => {
          if (v.value !== undefined) target.push(v.value)
          rise(v.children, target)
        })
      }
      const tree = {}
      tmpList.forEach(e => {
        if (e !== undefined) dig(tree, e.value.split('/'), e)
      })
      this.master_list = []
      rise(tree, this.master_list)
      this.$forceUpdate()
    })
  }
}
</script>
