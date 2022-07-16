<template>
  <div id="app">
    <upload v-model="picture" />
    <img :src="picture" />
    {{picture}}
  </div>
</template>

<script>
import Upload from './components/Upload.vue'

export default {
  name: 'app',
  components: {
    Upload
  },
  data () {
    return {
      picture: null
    }
  }
}
</script>

<style>
* {
  box-sizing: border-box;
}

html {
  font-size: 62.5%;
}

body {
  color: #2c2d30;
  font-size: 1.6rem;
  font-family: "Hiragino Kaku Gothic Pro", "ヒラギノ角ゴ Pro W3", "Meiryo",
    "メイリオ", "Osaka", "MS PGothic", arial, helvetica, clean, sans-serif;
  line-height: 1.5;
}
</style>
