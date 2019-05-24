import { 
    USER_REQUEST,
    USERS_REQUEST,
    USER_SUCCESS,
    AUTH_LOGOUT,
    USER_UPDATE,
    USER_CONFIRM_UPDATE_PASSWORD,
    USER_NOTIF_REQUEST,
    USER_CHANGE_PASSWORD,
    USER_UPDATE_STAFF,
    USER_UPDATE_IMAGE,
    USER_NOTIF_R,
    path,
    DOCS_REQUEST,
} from './mutation-types'
import Vue from 'vue'
import axios from 'axios'

const state = {
    profile: {},
}

const getters = {
    getProfile: state => state.profile,
    isProfileLoaded: state => !!state.profile.name,
}

const actions = {
    [USER_REQUEST]: ({commit, dispatch, rootState}, token) => {
        return new Promise((resolve, reject) => {
            // console.log(rootState.auth)
            axios
            .get(path + '/api/users/get_user_from_token/', {
                headers: { Authorization: "Token " + rootState.auth.token }
            })
            .then(response => {
                commit(USER_SUCCESS, response.data[0])
                dispatch(DOCS_REQUEST)
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
    // ДОБАВИТЬ ЧТОБЫ ТОЛЬКО АДМИН МОГ ТАКОЕ СЛАТЬ
    [USERS_REQUEST]: ({ commit, dispatch }) => {
        return new Promise((resolve, reject) => {
            axios
                .get(path + '/api/users/i')
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
    [USER_NOTIF_REQUEST]: ({commit, dispatch, rootState}) => {
        return new Promise(async (resolve, reject) => {
            let response = await axios.get(path + '/api/users/' + rootState.user.profile.id + '/notif/');
            await response.data.forEach(async (r, i) => {
                r.title = r.doc.title
                r.full_name = r.user.profile.full_name;
                r.date = 'r.message';
            })
            await console.log(response.data)
            await resolve(response.data)
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
                    // console.log(resp)
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
                resolve(resp)
                commit(USER_SUCCESS, resp.data)
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
    [USER_UPDATE_STAFF]: ({commit, dispatch}, data) => {
        return new Promise((resolve, reject) => {
            axios
            .patch(path + '/api/users/i/'+data.id, {
                "is_staff": data.is_staff
            },{
                headers: { Authorization: "Token " + data.token }
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
    // [USER_NOTIF_R]: (state, resp) => {
    //     Vue.set(state, 'r', resp)
    // }
}

export default {
    state,
    getters,
    actions,
    mutations,
}