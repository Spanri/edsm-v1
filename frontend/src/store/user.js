import { 
    USER_REQUEST,
    USER_SUCCESS,
    USER_NOTIF_REQUEST,
    AUTH_LOGOUT,
    USER_UPDATE,
    USER_CONFIRM_UPDATE_PASSWORD,
} from './mutation-types'
import Vue from 'vue'
import apiCall from '../api/common'
import axios from 'axios'

const state = {
    profile: {},
    notif: []
}

const getters = {
    getProfile: state => state.profile,
    getNotif: state => state.notif,
    isProfileLoaded: state => !!state.profile.name,
}

const actions = {
    [USER_REQUEST]: ({commit, dispatch, state}, token) => {
        return new Promise((resolve, reject) => {
            axios
            .get('http://127.0.0.1:8000/api/get_user_from_token/', {
                headers: { Authorization: "Token " + token }
            })
            .then(response => {
                commit(USER_SUCCESS, response.data[0])
            })
            .catch(err => {
                reject(err)
                console.log(err)
                dispatch(AUTH_LOGOUT)
            })
        })
    },
    [USER_NOTIF_REQUEST]: ({commit, dispatch}) => {
        return new Promise((resolve, reject) => {
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
        })
    },
    [USER_UPDATE]: ({commit, dispatch}, data) => {
        return new Promise((resolve, reject) => {
            axios
            .get('http://127.0.0.1:8000/api/get_user_from_token/', {
                headers: { Authorization: "Token " + data.token }
            })
            .then(response => {
                console.log(response.data[0].id)
                console.log(data.data)
                axios
                .put('http://127.0.0.1:8000/api/users/'+response.data[0].id, data.data, {
                    headers: { Authorization: "Token " + data.token }
                })
                .then(resp => {
                    commit(USER_SUCCESS, resp.data[0])
                    resolve(resp)
                })
                .catch(err => {
                    reject(err)
                    console.log(err)
                })
            })
            .catch(err => {
                reject(err)
                console.log(err)
            })
        })
    },
    // ПЕРЕДЕЛАТЬ
    [USER_CONFIRM_UPDATE_PASSWORD]: ({commit, dispatch}, email) => {
        return new Promise((resolve, reject) => {
            axios
            .post('http://localhost:8000/api/confirm_update_password/', {
                "email": email
            })
            .then(resp => {
                resolve(resp)
                // axios
                // .put('http://127.0.0.1:8000/api/users/'+response.data[0].id, data.data, {
                //     headers: { Authorization: "Token " + data.token }
                // })
                // .then(resp => {
                //     commit(USER_SUCCESS, resp.data[0])
                //     resolve(resp)
                // })
                // .catch(err => {
                //     reject(err)
                //     console.log(err)
                // })
            })
            .catch(err => {
                reject(err)
                console.log(err)
            })
        })
    },
}

const mutations = {
    [USER_SUCCESS]: (state, resp) => {
        Vue.set(state, 'profile', resp)
    }
}

export default {
    state,
    getters,
    actions,
    mutations,
}