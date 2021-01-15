import Vue from 'vue'
import Router from 'vue-router'
import store from '@/store/index'

import TestCss from './views/TestCss'
import Main from './views/Main'
import Container from "./components/Container";
import Login from "./views/auth/Login"
import Regist from "./views/auth/Regist"
import Photo from './views/Photo'
import PhotoDetail from './views/PhotoDetail'
import UploadPhoto from './views/UploadPhoto'
import About from './views/About'
import NotFound from './views/404'
// import {CheckAuthAPI} from "@/common/api";

Vue.use(Router)

const router = new Router({
    mode: 'history',
    routes: [
        {path: '/test', name: 'testcss', component: TestCss},
        {path: '/', name: 'main', component: Main},
        {path: '/container', redirect: '/photo', component: Container, children: [
                {path: '/login', name: 'login', component: Login},
                {path: '/regist', name: 'regist', component: Regist},

                {path: '/photo', name: 'photo', component: Photo},
                {path: '/detail/:id', name: 'detail', component: PhotoDetail},
                {path: '/upload', name: 'upload', component: UploadPhoto, meta: {requireAuth: true}},
                {path: '/about', name: 'about', component: About},
                {path: '/404', name: '404', component: NotFound},
            ]
        },
        // {path:'*',redirect:'/404'},
    ]
})

router.beforeEach((to, from, next) => {
    if (to.meta.requireAuth === true){
        if (store.state.username !== '') {
            next()
        } else {
            next({ path: '/login' })
        }
        // CheckAuthAPI().then(resp=>{
        //     if (resp.ret === 0) {
        //         next()
        //     } else {
        //         next({ path: '/login' })
        //     }
        // }).catch(() => {
        //     next({path: '/'})
        // })
    } else {
        next()
    }
})

export default router