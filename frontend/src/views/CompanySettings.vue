<template>
  <div id="companysettings">
    <h1>{{ $t('Store.accessType_company') + $t('Pagename.settings') }}</h1>
    <div v-for="(v, k) in elementdata" :key="k">
      {{ k }} : {{ v }}
    </div>
    <h2>{{ $t('Head.invite') }}</h2>
    <a :href="inviteURL()">{{ inviteURL() }}</a>
  </div>
</template>

<script>
export default {
  data () {
    return {
      elementdata: {}
    }
  },
  methods: {
    inviteURL () {
      return process.env.VUE_APP_BASE_URL + '/tryaccess/login?code=' + this.$route.params.id
    }
  },
  async created () {
    this.elementdata = await this.$_accessInformation(this.$route.params.id)
  }
}
</script>
