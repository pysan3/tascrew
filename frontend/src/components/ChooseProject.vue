<template>
  <div id="chooseproject" class="container mb-3 py-3 px-4 border border-top-0 rounded-bottom">
    <div class="row">
      <div v-for="type of $store.state.accessType" :key="type" class="col-12 col-md-6 col-lg-4">
        <div class="border rounded px-3 py-2">
          <div class="d-flex bg-light border-top border-bottom py-2 px-1">
            <div class="flex-grow-1 text-left"><h5 class="m-0">{{ type }}</h5></div>
            <div v-if="type !== 'user'" @click="$emit('togglechoise'); $router.push(`/add${type}`)" class="px-1"><a>ADD</a></div>
            <div @click="fetchData($store.getters.getValidAccess[type])" class="px-1"><a>RELOAD</a></div>
          </div>
          <div v-for="e in $store.getters.getValidAccess[type].filter(e => elementdata[e])" :key="e" @click="push2ID(e)" class="d-flex border-bottom py-2 px-1 align-items-center">
            <div class="flex-shrink-1">
              <img :src="elementdata[e].icon" alt="ICON" height="24px" class="px-1">
            </div>
            <div>{{ elementdata[e].name }}</div>
            <div v-if="elementdata[e].description" class="ml-auto w-25 oneline">{{ elementdata[e].description }}</div>
          </div>
        </div>
      </div>
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
  methods: {
    fetchData (accesshashes) {
      Promise.all(accesshashes.map(async accesshash => {
        this.elementdata[accesshash] = await this.$_accessInformation(accesshash)
      })).then(() => {
        this.$forceUpdate()
      })
    },
    push2ID (newid) {
      this.$emit('togglechoise')
      let pagetype = this.$route.name
      // add[company, project] => ''
      // [company, project, user]home => ''
      // [company, project, user]settings => 'settings'
      this.$store.state.accessType.concat(['add', 'home']).forEach(e => {
        pagetype = pagetype.replace(e, '')
      })
      this.$router.push({
        path: this.$_generateURL(pagetype, newid),
        query: this.$route.query
      })
    }
  },
  watch: {
    '$store.getters.getValidAccess': {
      handler: function () {
        this.fetchData(this.$store.state.accessType.reduce((accum, v) => accum.concat(this.$store.getters.getValidAccess[v] || []), []))
      },
      deep: true
    }
  },
  created () {
    this.fetchData(this.$store.state.accessType.reduce((accum, v) => accum.concat(this.$store.getters.getValidAccess[v] || []), []))
  }
}
</script>

<style lang="stylus" scoped>
.oneline
  white-space nowrap
  overflow hidden
</style>
