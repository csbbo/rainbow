<template>
<div id="Container">
    <nav class="nav-menu">
      <div class="nav-wrapper">
        <ul class="menu-left left hide-on-med-and-down">
          <li class="nav-logo" @click="backToHomePage">Rainbow</li>
          <li class="func-item-first"><router-link to="/photo">图片</router-link></li>
          <li class="func-item-first"><router-link to="/upload">上传</router-link></li>
          <li class="func-item"><router-link to="/about">关于</router-link></li>
        </ul>

        <ul class="menu-right right hide-on-med-and-down">
<!--          <li v-show="username">-->
<!--            &lt;!&ndash; Dropdown Trigger &ndash;&gt;-->
<!--            <a class="nav-dropdown-trigger" href="#!" data-target="nav-dropdown-menu">-->
<!--              <img src="https://avatars1.githubusercontent.com/u/35909137?s=400&u=9dd8afe3ff9acc78ea474b5d54e879ee5a50e75c&v=4" alt="avatar" class="circle">-->
<!--              <i class="material-icons right">arrow_drop_down</i>-->
<!--            </a>-->
<!--          </li>-->
          <!-- Dropdown Trigger -->
          <li v-show="username"><a class="dropdown-trigger" href="#!" data-target="dropdown1">Dropdown<i class="material-icons right">arrow_drop_down</i></a></li>

          <div v-show="!username">
            <li><router-link to="/login">登录</router-link></li>
            <li><router-link to="/regist">注册</router-link></li>
          </div>
        </ul>
      </div>
    </nav>

    <!-- Dropdown Structure -->
    <ul id="dropdown1" class="dropdown-content">
      <li><a href="#!">one</a></li>
      <li><a href="#!">two</a></li>
      <li class="divider"></li>
      <li @click="logout()"><a href="#!">注销</a></li>
    </ul>

  <router-view></router-view>
</div>
</template>

<script>
import "@/less/container.less"
import { store } from '@/store/index'
window.$ = window.jQuery = require('jquery');
import { LogoutAPI, AuthInfoAPI } from "@/common/api"
export default {
  name: "NavMenu",
  data: () => ({
    // page: {
    //   search: '',
    // },
    username: '',
    // imgPath: ''
  }),
  mounted() {
    window.jQuery(document).ready(function(){
        window.jQuery(".dropdown-trigger").dropdown();
    });
  },
  created() {
    this.auth()
  },
  methods: {
    backToHomePage() {
      this.$router.push("/")
    },
    logout() {
      LogoutAPI().then(() => {
        store.mutations.SetUsername(store.state, '')
        this.username = store.state.username
        this.$router.push('/login')
      })
    },
    auth() {
      AuthInfoAPI().then(resp => {
        if (resp.err === null) {
          store.mutations.SetUsername(store.state, resp.data.username)
          this.username = store.state.username
        }
      }).catch(() => {
        console.log('auth exception')
      })
    }
  }
}
</script>