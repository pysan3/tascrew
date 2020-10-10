<template>
  <div id="members">
    <div v-if="displayMembers">

    </div>
    <div v-else id="friends">
      <h1>友達</h1>
      <table class="table">
        <thead class="thead-light"><tr>
          <th>友達</th>
          <th>user_name</th>
          <th>real_name</th>
          <th>email</th>
          <th>phone_number</th>
          <th>address</th>
        </tr></thead>
        <tr v-for="(data, hash) in friendsdata" :key="hash" class="border-bottom">
          <td><router-link :to="`/user/${hash}`">{{ data.name }}</router-link></td>
          <td>{{ data.user_name }}</td>
          <td>{{ data.real_name }}</td>
          <td><a :href="`mailto:${data.email}`" class="mailtoui">{{ data.email }}</a></td>
          <td><a :href="`tel:${data.phone_number}`">{{ data.phone_number }}</a></td>
          <td><a :href="`http://maps.google.co.jp/maps?q=${encodeURI(data.address.replace(/\//g, ' '))}`" target="_blank">Googleマップを開く</a></td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      displayMembers: true,
      friendsdata: {}
    }
  },
  methods: {
    reload () {
      const accesshash = this.$_decodeHashID(this.$route.params.id)
      if (accesshash === undefined) { // display friends of user
        this.displayMembers = false
        Promise.all(this.$store.getters.getValidAccess.user.map(async accesshash => {
          this.friendsdata[accesshash] = await this.$_accessInformation(accesshash)
        })).then(() => {
          this.$forceUpdate()
        })
      } else if (accesshash.type === 'user') { // this page should not be able to access
        // redirect to friend's homepage
        this.$router.push({
          name: 'user',
          params: this.$route.params,
          query: this.$route.query
        })
      } else {
        this.displayMembers = true
      }
    }
  },
  watch: {
    '$route.params.id': function () {
      this.reload()
    }
  },
  created () {
    this.reload()
  }
}
</script>
