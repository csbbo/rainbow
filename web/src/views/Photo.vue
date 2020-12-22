<template>
    <div id="Photo">
        <nav-menu></nav-menu>
        <div class="filter">
            <div class="categorys">
                <span v-for="(cat, index) in category" :key="index" class="category">{{cat}}</span>
            </div>
        </div>

        <div class="container">
            <div class="item" v-for="(photo, index) in photos" :key="index">
                <div class="card progressive">
                    <a class="mark" href="/photo/BractCloseup_ZH-CN9096611979?force=home_1"></a>
                    <img class="" :src="photo.img_path">
                    <div class="description"><h3>photo:{{photo.id}}</h3></div>
                </div>
            </div>
        </div>

        <div class="photo-footer">
            <ul class="pagination">
                <li class="disabled"><a href="#!"><i class="material-icons">chevron_left</i></a></li>
                <li class="active"><a href="#!">1</a></li>
                <li class="waves-effect"><a href="#!">2</a></li>
                <li class="waves-effect"><a href="#!">3</a></li>
                <li class="waves-effect"><a href="#!">4</a></li>
                <li class="waves-effect"><a href="#!">5</a></li>
                <li class="waves-effect"><a href="#!"><i class="material-icons">chevron_right</i></a></li>
            </ul>
            <div class="extra-info">
                <span> ©2020 七色彩云</span>
            </div>
        </div>
    </div>
</template>

<script>
    import '@/less/photo.less'
    import NavMenu from "../components/NavMenu";
    import { GetPhotoListAPI, GetCategoryAPI } from "@/common/api"
    export default {
        name: "Photo",
        components: {
            "nav-menu": NavMenu
        },
        data: () => ({
            photos: [],
            total: 0,
            category: [],

            offset: 0,
            count: 15,
        }),
        created() {
            this.getPhoto()
            this.getCategory()
        },
        methods: {
            getPhoto() {
                GetPhotoListAPI({"count": this.count, "offset": this.offset}).then(resp => {
                    this.photos = resp.data.items
                    this.total = resp.data.total
                })
            },
            getCategory() {
                GetCategoryAPI().then(resp => {
                    this.category = resp.data.category
                })
            }
        }
    }
</script>
