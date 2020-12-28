<template>
    <div id="PhotoDetail">
        <nav-menu></nav-menu>

        <div class="show-img">
            <img :src="photo.img_path">
        </div>

        <div class="description">
            <div class="createday">2021-01-01</div>
            <div class="name"></div>
            <div class="description">雪中的蓝山雀和大山雀，法国北孚日地区自然公园 (© Michel Rauch/Minden Pictures)</div>
            <div class="copyright"></div>
        </div>

        <div class="function">
            <a class="waves-effect waves-light btn">点赞</a>
            <a class="waves-effect waves-light btn">下载</a>
        </div>

        <div class="info">
            <div class="download">下载数：</div>
        </div>
    </div>
</template>

<script>
    import '@/less/photodetail.less'
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