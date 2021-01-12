<template>
    <div id="PhotoDetail">
        <div class="show-img">
            <img :src="photo.img_path">
        </div>

        <div class="description">
            <div v-if="photo.create_time" class="createday">{{photo.create_time}}</div>
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
    export default {
        name: "PhotoDetail",
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
        }
    }
</script>

<style scoped>

</style>