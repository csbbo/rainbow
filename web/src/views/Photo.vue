<template>
    <div id="Photo">
        <nav-menu></nav-menu>
        <div v-if="template.showFilter" class="filter">
            <div class="categorys">
                <span v-for="(cat, index) in category" :key="index" class="category">{{cat}}</span>
            </div>
        </div>

        <div class="show">
            <div class="item" v-for="(photo, index) in photos" :key="index">
                <div class="card">
                    <a class="mark" href="/detail"></a>
                    <img class="" :src="photo.img_path">
                    <div class="description">
<!--                        <p style="font-size: 5px">photo:{{photo.id}}</p>-->
                    </div>
                    <div class="options">
                        <a class="waves-effect waves-light btn"><i class="material-icons left">favorite_border</i>点赞</a>
                        <a class="waves-effect waves-light btn"><i class="material-icons left">cloud_queue</i>下载</a>
                    </div>
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

        <div class="fixed-action-btn">
          <a class="btn-floating btn-large red">
            <i class="large material-icons">mode_edit</i>
          </a>
          <ul>
            <li @click="template.showFilter = !template.showFilter"><a class="btn-floating red"><i class="material-icons">{{template.showFilter ? 'unfold_less' : 'unfold_more' }}</i></a></li>
            <li><a class="btn-floating yellow darken-1"><i class="material-icons">format_quote</i></a></li>
            <li onclick="$('.tap-target').tapTarget('open')"><a class="btn-floating green"><i class="material-icons">info</i></a></li>
            <li><a class="btn-floating blue" href="#top"><i class="material-icons">expand_less</i></a></li>
          </ul>
        </div>

        <div class="fixed-action-btn" style="bottom: 45px; left: 24px; visibility:hidden">
            <a id="menu" class="btn btn-floating cyan"><i class="material-icons">menu</i></a>
        </div>
        <div class="tap-target cyan" data-target="menu">
            <div class="tap-target-content">
                <h5>欢迎来到小破站</h5>
                <p>初次见面，各位漂亮的小哥哥，小姐姐，请多多关照！</p>
                <p><br><br></p>
            </div>
        </div>
    </div>
</template>

<script>
    import '@/less/photo.less'
    import NavMenu from "../components/NavMenu";
    import { GetPhotoListAPI, GetCategoryAPI } from "@/common/api"
    window.$ = window.jQuery = require('jquery');
    export default {
        name: "Photo",
        components: {
            "nav-menu": NavMenu
        },
        data: () => ({
            template: {
                showFilter: false
            },
            photos: [],
            total: 0,
            category: [],

            offset: 0,
            count: 30,
            activePage: 1,
        }),
        mounted() {
            // eslint-disable-next-line no-undef
            $(document).ready(function(){
                // eslint-disable-next-line no-undef
                $('.fixed-action-btn').floatingActionButton();
                // eslint-disable-next-line no-undef
                $('.tap-target').tapTarget({
                    direction: 'top',
                });
            });
        },
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
