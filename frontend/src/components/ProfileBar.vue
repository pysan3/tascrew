<template>
  <div v-if="isFriend" id="profilebar" class="shadow-sm">
    <div class="container d-flex align-items-center py-3">
      <div class="flex-shrink-1 mx-2">
        <img :src="accessinfo.icon" alt="icon" height="24px" class="px-1">
      </div>
      <div class="mx-3"><b>{{ accessinfo.name }}</b></div>
      <div class="mx-2">{{ accessinfo.description }}</div>
      <div class="mx-2 ml-auto">(FAV☆)</div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      isFriend: false,
      accessinfo: {}
    }
  },
  methods: {
    getFriendDInfo (id) {
      const accessdata = this.$_decodeHashID(id)
      if (accessdata !== undefined) {
        this.accessinfo = this.$_accessInformation(id)
        this.isFriend = accessdata.type === 'user'
        if (this.accessinfo === undefined) this.isFriend = false
      } else this.isFriend = false
    }
  },
  watch: {
    '$route.params.id': function (to) {
      this.getFriendDInfo(to)
    }
  },
  created () {
    this.getFriendDInfo(this.$route.params.id)
  }
}
</script>
