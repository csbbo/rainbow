<template>
<div id="NavMenu">
    <!-- Dropdown Structure -->
    <ul id="nav-dropdown-menu" class="dropdown-content">
      <li><a href="/profile"><i class="material-icons">account_circle</i>个人信息</a></li>
      <li><a href="/write"><i class="material-icons">free_breakfast</i>写文章</a></li>
      <li class="divider"></li>
      <li><a href="/"><i class="material-icons">home</i>首页</a></li>
      <li><a href="#!"><i class="material-icons">settings</i>设置</a></li>
<!--      <li @click="logout"><a href="#!"><i class="material-icons">exit_to_app</i>退出</a></li>-->
    </ul>

    <nav class="nav-menu">
      <div class="nav-wrapper">
        <ul class="left hide-on-med-and-down">
          <li class="nav-logo" @click="backToHomePage">七色彩云</li>
          <li>
            <input class="global-search" type="text" placeholder="搜索"/>
          </li>
          <li class="search-icons"><i class="material-icons">search</i></li>
          <li class="func-item-first"><a href="/photo">图片</a></li>
          <li class="func-item"><a href="/about">关于</a></li>
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
import "@/less/navmenu.less"
// import {LogoutAPI,GetUserAPI} from "@/common/api"
export default {
  name: "NavMenu",
  data: () => ({
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