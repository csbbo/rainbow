<template>
    <div id="PhotoDetail">
        <div v-if="photo" class="show-img">
            <img :src="photo.img_path">
        </div>

        <preloader v-else></preloader>

        <div class="description">
            <div v-if="photo.create_time" class="createday">{{photo.create_time | formatDate}}</div>
            <div v-if="photo.name" class="name">{{photo.name}}</div>
            <div v-if="photo.description" class="desc">{{photo.description}}</div>
            <div v-if="photo.copyright" class="copyright">{{photo.copyright}}</div>
        </div>

<!--        <div class="function">-->
<!--            <div class="download">下载：{{photo.download_num}}</div>-->
<!--            <div class="download">点赞：{{photo.thumb_num}}</div>-->
<!--            <div class="download">查看：{{photo.watch_num}}</div>-->
<!--            <a class="waves-effect waves-light btn">点赞</a>-->
<!--            <a class="waves-effect waves-light btn">下载</a>-->
<!--        </div>-->
    </div>
</template>

<script>
    import '@/less/photodetail.less'
    import {GetPhotoAPI} from "@/common/api"
    import {formatDate} from "@/common/filter"
    import Preloader from "../components/Preloader";
    export default {
        name: "PhotoDetail",
        components: {
            "preloader": Preloader,
        },
        data: () => ({
            page: {

            },

            photo: '',
        }),
        created() {
            this.getPhoto()
        },
        methods: {
            getPhoto() {
                GetPhotoAPI({id: this.$route.params.id}).then(resp => {
                    this.photo = resp.data
                })
            }
        },
        filters: {
            formatDate: formatDate
        },
    }
</script>

<style scoped>

</style>