<template>
    <div id="Footer">
        <div v-if="total" class="pagination">
            <a class="waves-effect waves-light btn">上一页</a>
            <span><span>{{current_page}}/{{total/size || pageSize}}</span></span>
              <select style="display: inline-block; width: 85px" class="browser-default">
                <option v-for="option in options" v-bind:key="option" v-bind:value="option.value">{{option.text}}</option>
              </select>
            <a class="waves-effect waves-light btn">下一页</a>
        </div>
        <div class="extra-info">
            <span>Copyright © 2020 Rainbow</span>
        </div>
    </div>
</template>

<script>
    import '@/less/footer.less'
    export default {
        data() {
            return {
                pageSize: 10,
                current_page: 1,
                options: [
                    {'value': 10, 'text': '10条/页'},
                    {'value': 20, 'text': '20条/页'},
                    {'value': 30, 'text': '30条/页'},
                ]
            }
        },
        name: "Footer",
        props: ['total']
    }
</script>

<style scoped>

</style>