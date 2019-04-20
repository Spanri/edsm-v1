import { 
    USER_REQUEST, 
    USER_ERROR, 
    USER_SUCCESS,
    AUTH_LOGOUT
} from './mutation-types'
import Vue from 'vue'
import apiCall from '../api/common'
import axios from 'axios'

const state = { 
    status: '', 
    profile: {} 
}

const getters = {
    getProfile: state => state.profile,
    isProfileLoaded: state => !!state.profile.name,
}

const actions = {
    [USER_REQUEST]: ({commit, dispatch}) => {
        commit(USER_REQUEST)
        // axios
        // .post('http://127.0.0.1:8000/api-token-verify/', {
        //     "token" : state.token
        // })
        // .then(response => {
        //     commit(USER_SUCCESS, response)
        // })
        // .catch(resp => {
        //     commit(USER_ERROR)
        //     // if resp is unauthorized, logout, to
        //     dispatch(AUTH_LOGOUT)
        // })
        let response = {
            name:'Городничев Михаил Геннадьевич', 
            position:'Кандидат технических наук, заведующий кафедрой',
            adm: true,
        };
        commit(USER_SUCCESS, response)
    },
}

const mutations = {
    [USER_REQUEST]: (state) => {
        state.status = 'loading'
    },
    [USER_SUCCESS]: (state, resp) => {
        state.status = 'success'
        Vue.set(state, 'profile', resp)
    },
    [USER_ERROR]: (state) => {
        state.status = 'error'
    },
    [AUTH_LOGOUT]: (state) => {
        state.profile = {}
    }
}

export default {
    state,
    getters,
    actions,
    mutations,
}