import { 
    USER_REQUEST,
    USERS_REQUEST,
    USER_SUCCESS,
    AUTH_LOGOUT,
    USER_UPDATE,
    USER_CONFIRM_UPDATE_PASSWORD,
    USERS_EMAILS,
    USER_CHANGE_PASSWORD,
    USER_UPDATE_OTHER,
    USER_UPDATE_IMAGE,
    USER_PHOTO,
    USER_PHOTO_SUCCESS,
    path,
    DOCS_REQUEST,
} from './mutation-types'
import Vue from 'vue'
import axios from 'axios'

const state = {
    profile: {},
    users: [],
    photo: '',
}

const getters = {
    getProfile: state => state.profile,
    getPhoto: state => state.photo,
    getUsers: state => state.users,
    isProfileLoaded: state => !!state.profile.name,
}

const actions = {
    [USER_REQUEST]: ({commit, dispatch, rootState}) => {
        return new Promise((resolve, reject) => {
            axios
            .get(path + '/api/users/get_user_from_token/', {
                headers: { Authorization: "Token " + rootState.auth.token }
            })
            .then(response => {
                commit(USER_SUCCESS, response.data[0])
                dispatch(USER_PHOTO)
                resolve()
            })
            .catch(err => {
                try {
                    reject(err.response.request.response)
                } catch (error) {
                    reject(err)
                }
                dispatch(AUTH_LOGOUT)
            })
        })
    },
    [USERS_REQUEST]: ({ commit, dispatch, rootState }) => {
        return new Promise((resolve, reject) => {
            axios
                .get(path + '/api/users/i', {
                    headers: { Authorization: "Token " + rootState.auth.token }
                })
                .then(response => {
                    response.data.forEach(r => {
                        r.full_name = r.profile.full_name
                    });
                    resolve(response.data)
                })
                .catch(err => {
                    try {
                        reject(err.response.request.response)
                    } catch (error) {
                        reject(err)
                    }
                })
        })
    },
    [USERS_EMAILS]: ({ commit, dispatch, rootState }) => {
        return new Promise((resolve, reject) => {
            axios
                .get(path + '/api/users/emails/')
                .then(response => {
                    resolve(response.data)
                })
                .catch(err => {
                    try {
                        reject(err.response.request.response)
                    } catch (error) {
                        reject(err)
                    }
                })
        })
    },
    [USER_UPDATE]: ({commit, dispatch}, data) => {
        return new Promise((resolve, reject) => {
            axios
            .get(path + '/api/users/get_user_from_token/', {
                headers: { Authorization: "Token " + data.token }
            })
            .then(response => {
                axios
                .patch(path + '/api/users/i/'+response.data[0].id, data.data, {
                    headers: { Authorization: "Token " + data.token }
                })
                .then(resp => {
                    commit(USER_SUCCESS, resp.data)
                    resolve(resp)
                })
                .catch(err => {
                    try {
                        reject(err.response.request.response)
                    } catch (error) {
                        reject(err)
                    }
                })
            })
            .catch(err => {
                try {
                    reject(err.response.request.response)
                } catch (error) {
                    reject(err)
                }
            })
        })
    },
    [USER_PHOTO]: ({ commit, dispatch, rootState }) => {
        return new Promise((resolve, reject) => {
            axios
                .get(path + '/api/users/' + rootState.user.profile.id + '/photo/', {
                    headers: { Authorization: "Token " + rootState.auth.token }
                })
                .then(resp => {
                    commit(USER_PHOTO_SUCCESS, resp.data.photo)
                    resolve(resp.data.photo)
                })
                .catch(err => {
                    try {
                        reject(err.response.request.response)
                    } catch (error) {
                        reject(err)
                    }
                })
        })
    },
    [USER_UPDATE_IMAGE]: ({commit, dispatch, state}, data) => {
        return new Promise((resolve, reject) => {
            axios
            .patch(path + '/api/users/i/' + state.profile.id, 
                data.data, { headers: {
                    Authorization: "Token " + data.token,
                    'Content-Type': 'multipart/form-data' 
                }
            })
            .then(resp => {
                dispatch(USER_PHOTO)
                resolve(resp)
            })
            .catch(err => {
                try {
                    reject(err.response.request.response)
                } catch (error) {
                    reject(err)
                }
            })
        })
    },
    [USER_UPDATE_OTHER]: ({commit, dispatch, rootState}, data) => {
        return new Promise((resolve, reject) => {
            let id = data.id;
            delete data.id;
            axios
            .patch(path + '/api/users/i/'+ id, data, {
                headers: { Authorization: "Token " + rootState.auth.token }
            })
            .catch(err => {
                try {
                    reject(err.response.request.response)
                } catch (error) {
                    reject(err)
                }
            })
        })
    },
    [USER_CONFIRM_UPDATE_PASSWORD]: ({commit, dispatch}, email) => {
        return new Promise((resolve, reject) => {
            axios
            .post(path + '/api/users/rest_auth/password/reset/', {
                "email": email
            })
            .then(resp => {
                resolve(resp)
            })
            .catch(err => {
                try {
                    reject(err.response.request.response)
                } catch (error) {
                    reject(err)
                }
            })
        })
    },
    [USER_CHANGE_PASSWORD]: ({commit, dispatch}, data) => {
        return new Promise((resolve, reject) => {
            console.log(data)
            axios
            .post(path + '/api/users/rest_auth/password/reset/confirm/', {
                "uid": data.uid,
                "token": data.token,
                "new_password1": data.password1,
                "new_password2": data.password2,
            })
            .then(resp => {
                resolve(resp)
            })
            .catch(err => {
                try {
                    reject(err.response.request.response)
                } catch (error) {
                    reject(err)
                }
            })
        })
    },
}

const mutations = {
    [USER_SUCCESS]: (state, resp) => {
        Vue.set(state, 'profile', resp)
    },
    [USER_PHOTO_SUCCESS]: (state, resp) => {
        resp = resp.replace('\\','/')
        Vue.set(state, 'photo', path + '/' + resp)
    },
}

export default {
    state,
    getters,
    actions,
    mutations,
}