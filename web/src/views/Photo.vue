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
<!--                    <img src="https://magicstyle.fun/_/photo/80910536-c5d2-4a6f-8308-faeac16d6b5b">-->
                    <div class="description"><h3>photo:{{photo.id}}</h3></div>
                </div>
            </div>
        </div>

        <div class="photo-footer">
            <ul class="pagination">
                <li @click="getPhoto(activePage-1)" v-bind:class="{disabled:activePage<=1}"
                    ><a><i class="material-icons">chevron_left</i></a></li>
                <li @click="getPhoto(index)" v-for="index of Math.ceil(total/count)" :key="index"
                    v-bind:class="{active:index==activePage}" class="waves-effect"><a>{{index}}</a></li>
                <li @click="getPhoto(activePage+1)" v-bind:class="{disabled:activePage>=Math.ceil(total/count)}"
                    class="waves-effect"><a><i class="material-icons">chevron_right</i></a></li>
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
            count: 30,
            activePage: 1,
        }),
        created() {
            this.getPhoto()
            this.getCategory()
        },
        methods: {
            getPhoto(page=1) {
                if(page < 1){
                    page = 1
                }
                let maxpage = Math.ceil(this.total/this.count)
                if(page > maxpage) {
                    page = maxpage
                }
                this.activePage = page
                GetPhotoListAPI({"count": this.count, "offset": (page-1)*this.count}).then(resp => {
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
