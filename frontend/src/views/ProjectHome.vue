<template>
  <div id="projecthome">
    <h1>{{ $t('Store.accessType_project') + $t('Pagename.home') }}</h1>
    <div v-for="(v, k) in elementdata" :key="k">
      {{ k }} : {{ v }}
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      elementdata: {}
    }
  },
  async created () {
    this.elementdata = await this.$_accessInformation(this.$route.params.id)
  }
}
</script>
