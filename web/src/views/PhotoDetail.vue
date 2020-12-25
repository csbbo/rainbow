<template>
    <div class="PhotoDetail">
        <nav-menu></nav-menu>

        <div class="show-img">
            <img :src="photo.img_path">
        </div>

        <div class="description">
            description
        </div>

        <div class="function">
            function
        </div>
    </div>
</template>

<script>
    import NavMenu from "../components/NavMenu";
    import {GetPhotoAPI} from "@/common/api"
    export default {
        name: "PhotoDetail",
        data: () => ({
            page: {

            },

            photo: '',
        }),
        components: {
            "nav-menu": NavMenu
        },
        created() {
            this.getPhoto()
        },
        methods: {
            getPhoto() {
                GetPhotoAPI({id: this.$route.params.id}).then(resp => {
                    this.photo = resp.data
                })
            }
        }
    }
</script>

<style scoped>

</style>