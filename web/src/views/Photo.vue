<template>
    <div id="Photo">
        <div v-if="category.length > 0" class="filter">
            <div class="categorys">
                <span class="name">标签: </span>
                <span class="category" v-bind:class="{labelpick: page.label==null}" @click="page.label=null;getPhoto()">全部</span>
                <span v-for="(cat, index) in category" :key="index" class="category" v-bind:class="{labelpick: page.label===cat}" @click="page.label=cat;getPhoto(cat, null)">{{cat}}</span>
            </div>
        </div>

        <div class="show">
            <div class="item" v-for="(photo, index) in photos" :key="index">
                <div class="card">
                    <router-link class="mark" :to="'/detail/'+photo.id"></router-link>
                    <img :src="photo.img_path">
                    <div class="mark-content">
                        <div class="content-item" v-if="photo.name">{{photo.name}}</div>

                        <div class="content-item" v-if="photo.location"><i class="material-icons">location_on</i><span>{{photo.location}}</span></div>
                        <div class="content-item" v-if="photo.watch_count"><i class="material-icons">remove_red_eye</i><span>{{photo.watch_count}}</span></div>
                        <div class="content-item" v-if="photo.thumb_count"><i class="material-icons">thumb_up</i><span>{{photo.thumb_count}}</span></div>
                        <div class="content-item" v-if="photo.download_count"><i class="material-icons">cloud_download</i><span>{{photo.download_count}}</span></div>
                    </div>
                    <div class="options">
                        <a @click="thumbPhoto(photo.id)" class="waves-effect waves-light btn"><i class="material-icons left">favorite_border</i>点赞</a>
                        <a @click="downloadPhoto(photo.id)" class="waves-effect waves-light btn"><i class="material-icons left">cloud_queue</i>下载</a>
                    </div>
                </div>
            </div>
        </div>

        <footer-page v-if="photos"></footer-page>
        <preloader v-else></preloader>

        <!-------------------------------分割线---------------------------------->
        <!--hover menu-->
        <div class="fixed-action-btn">
          <a class="btn-floating btn-large red">
            <i class="large material-icons">mode_edit</i>
          </a>
          <ul>
            <li><a class="btn-floating yellow darken-1"><i class="material-icons">cloud_upload</i></a></li>
            <li onclick="$('.tap-target').tapTarget('open')"><a class="btn-floating green"><i class="material-icons">info</i></a></li>
            <li><a class="btn-floating blue" href="#top"><i class="material-icons">expand_less</i></a></li>
          </ul>
        </div>

        <!--hidden info-->
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
    import '@/common/utils'
    import Footer from "../components/Footer";
    import Preloader from "../components/Preloader";
    import { GetPhotoListAPI, GetCategoryAPI, DownloadPhotoAPI, ThumbPhotoAPI } from "@/common/api"
    window.$ = window.jQuery = require('jquery');
    export default {
        name: "Photo",
        components: {
            "footer-page": Footer,
            "preloader": Preloader,
        },
        data: () => ({
            page: {
                label: null,
            },
            photos: null,
            total: 0,
            category: [],
        }),
        mounted() {
            window.jQuery(document).ready(function(){
                window.jQuery('.fixed-action-btn').floatingActionButton();
                window.jQuery('.tap-target').tapTarget({
                    direction: 'top',
                });
            });
        },
        created() {
            this.getCategory()
            this.getPhoto()
        },
        methods: {
            getPhoto(category, search, count=18, offset=0) {
                const data = {
                    category: category,
                    search: search,
                    count: count,
                    offset: offset,
                }
                GetPhotoListAPI(data).then(resp => {
                    this.photos = resp.data.items
                    this.total = resp.data.total
                })
            },
            getCategory() {
                GetCategoryAPI().then(resp => {
                    this.category = resp.data.category
                })
            },
            downloadPhoto(id) {
                DownloadPhotoAPI({id: id})
                .then(response => {
                  let fileName = response.headers['content-disposition'].split('=')
                  fileName = fileName[fileName.length - 1]
                  fileName = decodeURIComponent(fileName)
                  fileName = fileName.replace(/"/g, '')
                  this.common.download(response.data, fileName)
                })
                .catch(err => {
                  this.$notify.error(err)
                })
            },
            thumbPhoto(id) {
                ThumbPhotoAPI(id).then(resp => {
                    if (resp.err != null) {
                        alert(resp.msg)
                    }
                })
            }
        }
    }
</script>
