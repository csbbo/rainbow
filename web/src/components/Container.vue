<template>
<div id="Container">
    <nav class="nav-menu">
      <div class="nav-wrapper">
        <ul class="left hide-on-med-and-down">
          <li class="nav-logo" @click="backToHomePage">Rainbow</li>
          <li class="func-item-first"><router-link to="/photo">图片</router-link></li>
          <li class="func-item-first"><router-link to="/upload">上传</router-link></li>
          <li class="func-item"><router-link to="/about">关于</router-link></li>
        </ul>

        <ul class="right hide-on-med-and-down">
          <li v-show="username">
            <!-- Dropdown Trigger -->
            <a class="nav-dropdown-trigger" href="#!" data-target="nav-dropdown-menu">
              <img src="https://avatars1.githubusercontent.com/u/35909137?s=400&u=9dd8afe3ff9acc78ea474b5d54e879ee5a50e75c&v=4" alt="avatar" class="circle">
              <i class="material-icons right">arrow_drop_down</i>
            </a>
          </li>

          <div v-show="username == ''">
            <li><a href="/login">登录</a></li>
            <li><a href="/regist">注册</a></li>
          </div>
        </ul>
      </div>
    </nav>

  <router-view></router-view>
</div>
</template>

<script>
import "@/less/container.less"
// import {LogoutAPI,GetUserAPI} from "@/common/api"
export default {
  name: "NavMenu",
  data: () => ({
    page: {
      search: '',
    },
    username: '',
    imgPath: ''
  }),
  mounted() {
    window.jQuery('.nav-dropdown-trigger').dropdown();
  },
  created() {
    // this.getuser()
  },
  methods: {
    // search() {
    //   if (this.page.search !== '') {
    //     delete this.$route.query.label
    //     this.$router.replace({path: '/photo', query: { ...this.$route.query, search: this.page.search } })
    //     location.reload()
    //   }
    // },
    backToHomePage() {
      this.$router.push("/")
    },
    // logout() {
    //   LogoutAPI().then(resp => {
    //     if (resp.ret !== 0) {
    //       alert(resp.msg)
    //     }
    //     this.$router.push("/")
    //     this.username = ''
    //   })
    // },
    // getuser() {
    //   GetUserAPI().then(resp => {
    //     if (resp.ret !== 0) {
    //       return
    //     }
    //     this.username = resp.data.username
    //     this.imgPath = resp.data.img_path
    //   })
    // }
  }
}
</script>