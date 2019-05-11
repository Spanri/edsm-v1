import { 
    USER_REQUEST,
    USER_SUCCESS,
    USER_NOTIF_REQUEST,
    AUTH_LOGOUT,
    USER_UPDATE,
    USER_CONFIRM_UPDATE_PASSWORD,
    USER_CHANGE_PASSWORD,
    USER_ALL_EMAILS,
    USER_UPDATE_STAFF,
    USER_UPDATE_IMAGE,
} from './mutation-types'
import Vue from 'vue'
import axios from 'axios'
import { conditionalExpression } from 'babel-types';

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
                reject(err.response.request.response)
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
                axios
                .patch('http://127.0.0.1:8000/api/users/'+response.data[0].id, data.data, {
                    headers: { Authorization: "Token " + data.token }
                })
                .then(resp => {
                    // console.log(resp)
                    commit(USER_SUCCESS, resp.data)
                    resolve(resp)
                })
                .catch(err => {
                    reject(err)
                })
            })
            .catch(err => {
                reject(err.response.request.response)
                // console.log(err)
            })
        })
    },
    [USER_UPDATE_IMAGE]: ({commit, dispatch, state}, data) => {
        return new Promise((resolve, reject) => {
            console.log(state.token)
            axios
            .patch('http://127.0.0.1:8000/api/users/' + state.profile.id, 
                data.data, { headers: {
                    Authorization: "Token " + data.token,
                    'Content-Type': 'multipart/form-data' 
                }
            })
            .then(resp => {
                resolve(resp)
                commit(USER_SUCCESS, resp.data)
            })
            .catch(err => {
                reject(err.response.request.response)
            })
        })
    },
    [USER_UPDATE_STAFF]: ({commit, dispatch}, data) => {
        return new Promise((resolve, reject) => {
            axios
            .patch('http://127.0.0.1:8000/api/users/'+data.id, {
                "is_staff": data.is_staff
            },{
                headers: { Authorization: "Token " + data.token }
            })
            .catch(err => {
                reject(err.response.request.response)
            })
        })
    },
    [USER_ALL_EMAILS]: ({commit, dispatch, state}, data) => {
        return new Promise((resolve, reject) => {
            axios
            .get('http://127.0.0.1:8000/api/all_emails/')
            .then(response => {
                resolve(response.data)
            })
            .catch(err => {
                reject(err.response.request.response)
            })
        })
    },
    [USER_CONFIRM_UPDATE_PASSWORD]: ({commit, dispatch}, email) => {
        return new Promise((resolve, reject) => {
            axios
            .post('http://localhost:8000/rest_auth/password/reset/', {
                "email": email
            })
            .then(resp => {
                resolve(resp)
            })
            .catch(err => {
                reject(err.response.request.response)
            })
        })
    },
    [USER_CHANGE_PASSWORD]: ({commit, dispatch}, data) => {
        return new Promise((resolve, reject) => {
            console.log(data)
            axios
            .post('http://localhost:8000/rest_auth/password/reset/confirm/', {
                "uid": data.uid,
                "token": data.token,
                "new_password1": data.password1,
                "new_password2": data.password2,
            })
            .then(resp => {
                resolve(resp)
            })
            .catch(err => {
                reject(err.response.request.response)
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