<template>
  <div id="app">
    <header class="sticky-top"><HeaderDefault :is_loggedin="$store.getters.is_loggedin" /></header>
    <div class="desktop"><router-view/></div>
  </div>
</template>

<script>
import HeaderDefault from '@/components/HeaderDefault'
export default {
  name: 'App',
  components: {
    HeaderDefault
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.desktop {
  margin-top: 8px;
}
*[style*="display: none"] {
  display: none !important
}
</style>
