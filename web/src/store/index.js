import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)
export const store = {
    state: {
        codeCountDown: 0,
    },
    mutations: {
        ReduceCodeCountDown (state) {
            state.codeCountDown--
        },
        SetCodeCountDown (state, value) {
            state.codeCountDown = value
        }
    }
}
export default new Vuex.Store(store)
