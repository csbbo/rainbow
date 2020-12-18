import Vue from 'vue'
import App from './App.vue'
// import './common/axios'
import router from './router'

Vue.config.productionTip = false

import Materialize from 'materialize-css'
import 'material-design-icons/iconfont/material-icons.css'
import 'materialize-css/dist/css/materialize.min.css'
import 'materialize-css/dist/js/materialize.min.js'
Vue.use(Materialize)


new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
