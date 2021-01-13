<template>
    <div id="Login">
        <div class="panel">
            <input type="text" placeholder="username"/>
            <input type="text" placeholder="phone"/>
            <input type="password" placeholder="password"/>
            <a class="waves-effect waves-light btn-small">Button</a>
        </div>
    </div>
</template>

<script>
    import "@/less/auth.less"
    export default {
        name: "Login"
    }
</script>

<style scoped>
    .panel {
        margin: 40px auto auto;
        width: 500px;
    }
    input {
        outline: none !important;
        border: none !important;
    }
</style>