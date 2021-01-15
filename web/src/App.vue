<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
import './less/global.less'
import { AuthInfoAPI } from "@/common/api"
import { store } from '@/store/index'
export default {
  name: 'App',
  created() {
    // 在每次刷新时候去请求一下登录状态信息
    AuthInfoAPI().then(resp => {
      if (resp.err === null) {
        store.mutations.SetUsername(store.state, resp.data.username)
      }
    }).catch(() => {
      console.log('auth exception')
    })
  }
}
</script>
