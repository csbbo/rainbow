<template>
    <div id="Photo">
        <div class="filter">
            <div class="categorys">
                <span v-for="(cat, index) in category" :key="index" class="category">{{cat}}</span>
            </div>
        </div>

        <div class="show">
            <div v-for="(photo, index) in photos" :key="index" class="item">
                <div class="card">
                    <img src="http://h2.ioliu.cn/bing/PolarExpress_ZH-CN9522496479_1920x1080.jpg?imageslim">
                    <div class="description">
                        <h3 style="color: #fff">{{photo.id}}</h3>
                    </div>
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
    import { GetPhotoAPI, GetCategoryAPI } from "@/common/api"
    export default {
        name: "Photo",
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
                GetPhotoAPI({"count": this.count, "offset": this.offset}).then(resp => {
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
