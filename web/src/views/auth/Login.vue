<template>
    <div id="Login">
        <div class="panel">
            <div class="panel-name">登录</div>
            <div class="input-row">
                <i class="material-icons">account_box</i>
                <input type="text" placeholder="用户名"/>
            </div>
            <div class="input-row">
                <i class="material-icons">lock</i>
                <input type="password" placeholder="密码"/>
            </div>
            <a class="waves-effect waves-light btn-small submit-btn">登录</a>
            <div class="auth-err">{{authErr}}</div>
            <div class="jump"><router-link class="jump-link" to="/regist">还没有账号？去注册</router-link></div>
        </div>
    </div>
</template>

<script>
    import "@/less/auth.less"
    export default {
        name: "Login",
        data: () => ({
            authErr: '',
        }),
    }
</script>
