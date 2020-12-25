<template>
    <div id="Photo">
        <nav-menu></nav-menu>
        <div v-if="page.showFilter" class="filter">
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
            <div class="pagination">
                <a @click="page.curPage=page.curPage-1<1?1:page.curPage-1;updateQuery()" class="waves-effect waves-light btn">上一页</a>
                <span>{{page.curPage}}/{{Math.ceil(total/page.selected.selected)}}</span>
                  <select @change="updateQuery()" v-model="page.selected.selected" style="display: inline-block; width: 85px" class="browser-default">
                    <option v-for="option in page.selected.options" v-bind:key="option" v-bind:value="option.value">{{option.text}}</option>
                  </select>
                <a @click="page.curPage=(+page.curPage)+(+1);updateQuery()" class="waves-effect waves-light btn">下一页</a>
            </div>
            <div class="extra-info">
                <span>Copyright © 2020 Rainbow</span>
            </div>
        </div>

        <div class="fixed-action-btn">
          <a class="btn-floating btn-large red">
            <i class="large material-icons">mode_edit</i>
          </a>
          <ul>
            <li @click="page.showFilter = !page.showFilter"><a class="btn-floating red"><i class="material-icons">{{page.showFilter ? 'unfold_less' : 'unfold_more' }}</i></a></li>
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
            page: {
                showFilter: false,
                curPage: 1,
                selected: {
                    selected: 12,
                    options: [
                        {'text': '6 条/页', value: 6},
                        {'text': '12 条/页', value: 12},
                        {'text': '24 条/页', value: 24},
                        {'text': '48 条/页', value: 48},
                        {'text': '64 条/页', value: 64},
                    ]
                }
            },
            photos: [],
            total: 0,
            category: [],
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
            this.getQueryAndInitParam()
            this.getPhoto()
            this.getCategory()
        },
        methods: {
            getPhoto() {
                const count = this.page.selected.selected
                const offset = (this.page.curPage-1) * count
                GetPhotoListAPI({'count': count, 'offset': offset}).then(resp => {
                    this.photos = resp.data.items
                    this.total = resp.data.total
                })
            },
            getCategory() {
                GetCategoryAPI().then(resp => {
                    this.category = resp.data.category
                })
            },
            getQueryAndInitParam() {
                if (this.$route.query.page != null) {
                    this.page.curPage = this.$route.query.page
                }
                if (this.$route.query.count != null) {
                    this.page.selected.selected = this.$route.query.count
                }
            },
            updateQuery() {
                let page = this.page.curPage
                if (page < 1) {
                    page = 1
                }
                const maxPage = Math.ceil(this.total/this.page.selected.selected)
                if (page > maxPage) {
                    page = maxPage
                }

                const count = this.page.selected.selected
                this.$router.push({
                    path: '/photo',
                    query: {'page': page, count: count},
                })
                location.reload()
            }
        }
    }
</script>
