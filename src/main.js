// eslint-disable-next-line
/* eslint-disable */ 
// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'  //axiosを使う場合、main.jsでimportする。

Vue.config.productionTip = false
Vue.prototype.$axios = axios  //axiosを使う場合、main.jsでこの行の追記が必要

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})