<template>
  <ul id="settings_sidebar" class="nav flex-column nav-pills pl-3 pr-3 pr-md-0 py-2">
    <!-- <li class="col-12" @click="$router.push('/settings/calendarapi')">Calendar API Setting</li> -->
    <li v-for="(n, index) in setting_list.map(x => x.toLowerCase())" :key="n" class="nav-item" @click="$router.push(`/usersettings?menu=${n}`)">
      <a class="btn-light" :class="`rounded-0 nav-link ${is_active(n, index)}`" style="border-top-left-radius: .25rem!important; border-bottom-left-radius: .25rem!important;">
        {{ $t(`Settings.${n}`) }}
      </a>
    </li>
  </ul>
</template>

<script>
export default {
  props: [
    'setting_list',
    'current_menu'
  ],
  methods: {
    is_active (n, index) {
      if ((this.$route.params.menu || index) && this.$route.params.menu !== n) {
        return ''
      } else {
        return 'active'
      }
    }
  }
}
</script>
