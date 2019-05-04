import { 
    USER_REQUEST, 
    USER_ERROR, 
    USER_SUCCESS,
    USER_NOTIF_REQUEST,
    AUTH_LOGOUT,
    USER_UPDATE
} from './mutation-types'
import Vue from 'vue'
import apiCall from '../api/common'
import axios from 'axios'

const state = { 
    status: '', 
    profile: {},
    notif: []
}

const getters = {
    getProfile: state => state.profile,
    getNotif: state => state.notif,
    isProfileLoaded: state => !!state.profile.name,
}

const actions = {
    [USER_REQUEST]: ({commit, dispatch}) => {
        commit(USER_REQUEST)
        // axios
        // .post('http://127.0.0.1:8000/users', {
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
            email: 'kozlova9v@mail.ru',
            password: '123456', // может не надо? или в хешированном виде
            name:'Городничев Михаил Геннадьевич', 
            position:'Кандидат технических наук, заведующий кафедрой',
            adm: true,
        };
        commit(USER_SUCCESS, response)
    },
    [USER_NOTIF_REQUEST]: ({commit, dispatch}) => {
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
    [USER_UPDATE]: ({commit, dispatch}, data) => {
        let request = {};
        Object.assign(request, 
            data.password ? { password: data.password } : null,
            data.email ? { email: data.email } : null,
            data.name ? { first_name: data.name } : null,
        );  
        axios
        .post('http://127.0.0.1:8000/update/user/', request)
        .then(response => {
            commit(USER_SUCCESS, response)
        })
        .catch(resp => {
            commit(USER_ERROR)
            // if resp is unauthorized, logout, to
            dispatch(AUTH_LOGOUT)
        })
                
        console.log(response);
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