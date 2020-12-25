import Vue from 'vue'
import Router from 'vue-router'
import Main from './views/Main'
import Photo from './views/Photo'
import PhotoDetail from './views/PhotoDetail'
import About from './views/About'
import {CheckAuthAPI} from "@/common/api";

Vue.use(Router)

const router = new Router({
    mode: 'history',
    routes: [
        {path: '/', name: 'main', component: Main},
        {path: '/photo', name: 'photo', component: Photo},
        {path: '/detail', name: 'detail', component: PhotoDetail},
        {path: '/about', name: 'about', component: About},
        // {path: '/navmenu', redirect: "/photo", component: NavMenu, children: [
        //         {path: '/photo', name: 'photo', component: Photo},
        //     ]
        // },
        // {path: '/devtest', name: 'devtest', component: DevTest},
        // {path: '/notfound', name: 'notfound', component: PageNoteFound},
        //
        // {path: '/login', name: 'login', component: Login},
        // {path: '/regist', name: 'regist', component: Regist},
        // {path: '/', redirect: "/home", component: NavMenu, children: [
        //         {path: '/home', name: 'home', component: Home},
        //         {path: '/profile', name: 'profile', component: Profile, meta:{requireAuth: true}},
        //         {path: '/write', name: 'write', component: Write, meta:{requireAuth: true}},
        //         {path: '/read', name: 'read', component: Read},
        //     ]
        // },
        // {path:'*',redirect:'/notfound'},
    ]
})

router.beforeEach((to, from, next) => {
    if (to.meta.requireAuth === true){
        CheckAuthAPI().then(resp=>{
            if (resp.ret === 0) {
                next()
            } else {
                next({ path: '/login' })
            }
        }).catch(() => {
            next({path: '/'})
        })
    } else {
        next()
    }
})

export default router