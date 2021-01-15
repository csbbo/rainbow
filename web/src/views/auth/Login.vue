<template>
    <div id="Login">
        <div class="panel">
            <div class="panel-name">登录</div>
            <div class="input-row">
                <i class="material-icons">account_box</i>
                <input v-model="form.username" type="text" placeholder="用户名"/>
            </div>
            <div class="input-row">
                <i class="material-icons">lock</i>
                <input v-model="form.password" type="password" placeholder="密码"/>
            </div>
            <a @click="login()" class="waves-effect waves-light btn-small submit-btn">登录</a>
            <div class="auth-err">{{authErr}}</div>
            <div class="jump"><router-link class="jump-link" to="/regist">还没有账号？去注册</router-link></div>
        </div>
    </div>
</template>

<script>
    import "@/less/auth.less"
    import { LoginAPI } from "@/common/api"
    export default {
        name: "Login",
        data: () => ({
            authErr: '',
            form: {
                username: '',
                password: '',
            }
        }),
        methods: {
            login() {
                this.authErr = '' // 方便看错误信息变化
                if (!(this.form.username && this.form.password)) {
                  this.authErr = '选项不能为空'
                  return
                }
                if (this.form.username.length > 20) {
                    this.authErr = '用户名长度不能超过20个字符串!'
                    return
                }

                const data = {
                    username: this.form.username,
                    password: this.form.password,
                }
                LoginAPI(data).then(resp => {
                    if (resp.err != null) {
                        this.authErr = resp.msg
                        return
                    }
                    this.$router.push('/photo')
                })
            }
        },
    }
</script>
