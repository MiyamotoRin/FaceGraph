<template>
  <div id="app">
    <header>
      <div class="title-block">Face Graph</div>
    </header>
    <div class="mid-block">
      <upload v-model="picture" />
    </div>
    <footer class="giass">
      <p>©2022 それイけ、つくパンパン</p>
    </footer>
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
  height: 100%;
}

h1 {
  margin: 0%;
}

.title-block {
  color: #ea5455;
  font-size: 40px;
  text-align: center;
  font-weight: bolder;
}

body {
  color: #2c2d30;
  font-size: 1.6rem;
  font-family: "Hiragino Kaku Gothic Pro", "ヒラギノ角ゴ Pro W3", "Meiryo",
    "メイリオ", "Osaka", "MS PGothic", arial, helvetica, clean, sans-serif;
  line-height: 1.5;
  margin: 0%;
  height:100%;
}

.mid-block {
  max-width: 100%;
  background-color: #f07b3f;
}

.proc-photo {
  max-width: 50%;
  display: block;
}

header {
  background-color: #2d4059;
  padding: 0px;
}

footer {
  color: #ea5455;
  font-size: 10px;
  text-align: center;
  background-color: #2d4059;
  padding: 20px;
}

</style>
