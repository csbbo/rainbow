<template>
    <div id="Regist">
        <div class="panel">
            <div class="panel-name">注册</div>
            <div class="input-row">
                <i class="material-icons">account_box</i>
                <input v-model="form.username" type="text" placeholder="用户名"/>
            </div>
            <div class="input-row">
                <i class="material-icons">email</i>
                <input v-model="form.email" type="email" placeholder="邮箱"/>
            </div>
            <div class="input-row">
                <i class="material-icons">security</i>
                <input v-model="form.captcha" type="text" placeholder="验证码"/>
                <div class="security-code"><a @click="getCode()" :class="{disabled: disable}" class="waves-light btn-small">{{codeMsg}}</a></div>
            </div>
            <div class="input-row">
                <i class="material-icons">lock</i>
                <input v-model="form.password" type="password" placeholder="密码"/>
            </div>
            <a @click="regist()" class="waves-light btn-small submit-btn">注册</a>
            <div class="auth-err">{{authErr}}</div>
            <div class="jump"><router-link class="jump-link" to="/login">已有账号？去登录</router-link></div>
        </div>
    </div>
</template>

<script>
    import "@/less/auth.less"
    import { store } from '@/store/index'
    import { RegistAPI } from "@/common/api"
    export default {
        name: "Regist",
        data: () => ({
            authErr: '',
            codeMsg: '获取验证码',
            disable: false,
            form: {
                username: '',
                email: '',
                captcha: '',
                password: '',
            }
        }),
        created() {
            if (store.state.codeCountDown > 0) {
                this.disable = true
                const interval = setInterval(() => {
                        if (store.state.codeCountDown > 0) {
                        this.codeMsg = "重新发送(" + store.state.codeCountDown + ")";
                  } else {
                        this.codeMsg = "获取验证码";
                        this.disable = false
                        clearInterval(interval)
                  }
                }, 1000)
            }
        },
        methods: {
            getCode(count=120) {
              if (store.state.codeCountDown !== 0) {
                  return
              }
              this.disable = true
              store.mutations.SetCodeCountDown(store.state, count)

                const interval = setInterval(() => {    //貌似函数会在后台执行，所以只要不强刷，切换到别的页面还是会计数
                    if (store.state.codeCountDown > 0) {
                        store.mutations.ReduceCodeCountDown(store.state)
                        if (store.state.codeCountDown > 0) {
                            this.codeMsg = "重新发送(" + store.state.codeCountDown + ")";
                        } else {
                            this.codeMsg = "获取验证码";
                            this.disable = false
                            clearInterval(interval)
                        }
                    }
                }, 1000);
            },
            regist() {
                this.authErr = '' // 方便看错误信息变化
                if (!(this.form.username && this.form.password && this.form.email && this.form.captcha)) {
                  this.authErr = '选项不能为空'
                  return
                }
                if (this.form.username.length > 20) {
                    this.authErr = '用户名长度不能超过20个字符串!'
                    return
                }
                if (!this.form.email.match(/^[^@]+@[^@]+\.[^@]+$/)) {
                  this.authErr = '邮箱格式错误!'
                  return
                }
                if (this.form.captcha.length != 4) {
                    this.authErr = '验证码错误!'
                    return
                }

                const data = {
                    username: this.form.username,
                    password: this.form.password,
                    email: this.form.email,
                    captcha: this.form.captcha,
                }
                RegistAPI(data).then(resp => {
                    if (resp.err != null) {
                        this.authErr = resp.msg
                        return
                    }
                    this.$router.push('/login')
                })
            },
        },
    }
</script>
