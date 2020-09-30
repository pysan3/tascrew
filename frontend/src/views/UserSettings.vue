<template>
  <div id="settings" class="row no-gutters">
    <nav id="sidebar" class="col-3 col-lg-2 d-none d-md-block text-left border-right">
      <h3 class="border-bottom py-3 px-4 m-0">Settings</h3>
      <Searchbar :setting_list="setting_list" />
    </nav>
    <div id="content" class="col-12 col-md-9 col-lg-10">
      <div class="border rounded text-left mb-3 d-md-none">
        <button class="btn btn-dark mx-3 my-1" data-toggle="collapse" data-target="#searchbar-holder" aria-expand="false" aria-controls="searchbar-holder">
          Settings
        </button>
        <div class="collapse" id="searchbar-holder">
          <div class="card card-body border-0 p-0">
            <Searchbar :setting_list="setting_list" />
          </div>
        </div>
      </div>
      <!-- <CalendarAPI v-show="current_menu==='calendarapi'" /> -->
      <component v-for="c of setting_list" :key="c" :is="c" v-show="current_menu===c.toLowerCase()" class="text-left px-3 px-lg-4"/>
    </div>
  </div>
</template>

<script>
import Searchbar from '@/components/SettingsSidebar'
import CalendarAPI from '@/components/CalendarAPI'
import NotFound from '@/views/NotFound'
export default {
  components: {
    Searchbar,
    CalendarAPI,
    NotFound
  },
  data () {
    return {
      setting_list: [
        'CalendarAPI',
        'NotFound'
      ],
      current_menu: this.$route.params.menu
    }
  },
  watch: {
    '$route.params.menu': function (menu) {
      this.current_menu = menu || this.setting_list[0].toLowerCase()
    }
  },
  created () {
    if (!this.$route.params.menu) {
      this.$router.push({
        name: 'usersettings',
        params: { menu: this.setting_list[0].toLowerCase() }
      })
    }
  }
}
</script>

<style lang="stylus" scoped>
.row
  margin 0px
</style>
