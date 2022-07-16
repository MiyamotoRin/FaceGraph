<template>
  <div id="app">
    <h1 class="giass">
      <div class="left-block">Face Graph</div>
    </h1>
    <div class="mid-block">
    <upload v-model="picture" />
    <div v-if="picture">
      <img :src="picture" class="proc-photo" />
    </div>
    </div>
    <footer class="giass">
      <p>©2022 それイけ、つくパンパン</p>
    </footer>
  </div>
</template>

<script>
/* eslint-disable */
import Upload from "./components/Upload.vue";

export default {
  name: "app",
  components: {
    Upload,
  },
  data() {
    return {
      picture: null,
    };
  },
};
</script>

<style>
* {
  box-sizing: border-box;
}

html {
  font-size: 62.5%;
}
h1{
    margin:0%;
}

.left-block{
  color: bisque;
  font-size: 40px;
  text-align: center;
}

body {
  color: #2c2d30;
  font-size: 1.6rem;
  font-family: "Hiragino Kaku Gothic Pro", "ヒラギノ角ゴ Pro W3", "Meiryo",
    "メイリオ", "Osaka", "MS PGothic", arial, helvetica, clean, sans-serif;
  line-height: 1.5;
  margin:0%
}
.mid-block{
  width:100%;
  height:700px;
  background-color:bisque;
}
.proc-photo {
  max-width: 50%;
  display: block;
}
.giass {
  background-color: black;
    padding: 20px;
}
footer.giass p {
  color: bisque;
  font-size: 10px;
  text-align: center;
}
</style>
