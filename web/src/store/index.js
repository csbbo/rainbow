import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)
export const store = {
    state: {
        username: '',
        codeCountDown: 0,
    },
    mutations: {
        SetUsername (state, username) {
            state.username = username
        },
        ReduceCodeCountDown (state) {
            state.codeCountDown--
        },
        SetCodeCountDown (state, value) {
            state.codeCountDown = value
        }
    }
}
export default new Vuex.Store(store)
