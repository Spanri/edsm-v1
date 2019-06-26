import {
    ADDIT_RELOAD,
    ADDIT_REMEMBER_PASSWORD,
    ADDIT_ERROR_AUTH,
    path,
} from './mutation-types'
import { formatDate } from '../otherFun'
import Vue from 'vue'
import axios from 'axios'

const state = {
    reload: '',
    rememberPassword: false,
    errorAuth: '',
}

const getters = {
    getReload: state => state.reload,
    getRememberPassword: state => state.rememberPassword,
    getErrorAuth: state => state.errorAuth,
}

const actions = {

}

const mutations = {
    [ADDIT_RELOAD]: (state, resp) => {
        Vue.set(state, 'reload', resp)
    },
    [ADDIT_REMEMBER_PASSWORD]: (state, resp) => {
        Vue.set(state, 'rememberPassword', resp)
    },
    [ADDIT_ERROR_AUTH]: (state, resp) => {
        Vue.set(state, 'errorAuth', resp)
    },
}

export default {
    state,
    getters,
    actions,
    mutations,
}