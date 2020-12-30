<template>
    <div id="Photo">
        <nav-menu></nav-menu>
        <div v-if="!page.hidden" class="filter">
            <div class="categorys">
                <span class="name">标签: </span>
                <span class="category" v-bind:class="{labelpick: page.label==null}" @click="page.label=null;updateQuery()">全部</span>
                <span v-for="(cat, index) in category" :key="index" class="category" v-bind:class="{labelpick: page.label===cat}" @click="page.label=cat;updateQuery()">{{cat}}</span>
            </div>
        </div>

        <div class="show">
            <div class="item" v-for="(photo, index) in photos" :key="index">
                <div class="card">
                    <a class="mark" @click="gotoDetail(photo.id)"></a>
                    <img :src="photo.img_path">
                    <div class="description">
<!--                        <p style="font-size: 5px">photo:{{photo.id}}</p>-->
                    </div>
                    <div class="options">
                        <a class="waves-effect waves-light btn"><i class="material-icons left">favorite_border</i>点赞</a>
                        <a :href="photo.img_path" class="waves-effect waves-light btn"><i class="material-icons left">cloud_queue</i>下载</a>
                    </div>
                </div>
            </div>
        </div>

        <div class="photo-footer">
            <div v-if="total" class="pagination">
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
            <li @click="page.hidden = !page.hidden"><a class="btn-floating red"><i class="material-icons">{{page.hidden ?  'unfold_more':'unfold_less' }}</i></a></li>
            <li><a class="btn-floating yellow darken-1"><i class="material-icons">cloud_upload</i></a></li>
            <li onclick="$('.tap-target').tapTarget('open')"><a class="btn-floating green"><i class="material-icons">info</i></a></li>
            <li><a class="btn-floating blue" href="#top"><i class="material-icons">expand_less</i></a></li>
          </ul>
        </div>

        <!--        hidden info-->
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
                hidden: true,
                label: null,
                search: '',
                curPage: 1,
                selected: {
                    selected: 12,
                    options: [
                        {'text': '06 条/页', value: 6},
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
            window.jQuery(document).ready(function(){
                window.jQuery('.fixed-action-btn').floatingActionButton();
                window.jQuery('.tap-target').tapTarget({
                    direction: 'top',
                });
            });
        },
        created() {
            this.getQueryAndInitParam()
            this.getCategory()
            this.getPhoto()
        },
        methods: {
            getPhoto() {
                const count = this.page.selected.selected
                const offset = (this.page.curPage-1) * count
                let data = {'count': count, 'offset': offset}

                if (this.page.label != null) {
                    data['category'] = this.page.label
                }

                if (this.page.search != null) {
                    data['search'] = this.page.search
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
            getQueryAndInitParam() {
                if (this.$route.query.page != null) {
                    this.page.curPage = this.$route.query.page
                }
                if (this.$route.query.count != null) {
                    this.page.selected.selected = this.$route.query.count
                }
                if (this.$route.query.label != null) {
                    this.page.label = this.$route.query.label
                }
                if (this.$route.query.search != null) {
                    this.page.search = this.$route.query.search
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
                let queryDict = {'page': page, count: count}

                if (this.page.label!=null) {
                    queryDict['label'] = this.page.label
                }
                this.$router.replace({
                    path: '/photo',
                    query: queryDict,
                })
                location.reload()
            },
            gotoDetail(id) {
                this.$router.push({name: 'detail', params: {id: id}})
            }
        }
    }
</script>
