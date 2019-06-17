import { 
    AUTH_REQUEST,
    AUTH_TOKEN,
    AUTH_AUTH,
    USER_REQUEST,
    AUTH_LOGOUT,
    AUTH_SIGNUP,
    DOCS_FILE_CABINET,
    DOCS_SUCCESS,
    DOCS_REQUEST,
    path,
} from './mutation-types'
import axios from 'axios'

const state = {
    token: localStorage.getItem('user-token') || '',
    auth: '',
}

const getters = {
    token: state => state.token,
    auth: state => state.auth,
    isAuthenticated: state => !!state.token,
}

const actions = {
    [AUTH_SIGNUP]: ({commit, dispatch, rootState}, data) => {
        return new Promise((resolve, reject) => {
            console.log(data)
            axios
            .post(path + '/api/users/send_invite/', data, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    Authorization: "Token " + rootState.auth.token
                }
            })
            .then(resp => {
                console.log(resp.data);
                resolve(resp.data.password)
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
    [AUTH_REQUEST]: ({commit, dispatch, rootState}, user) => {
        return new Promise((resolve, reject) => {
            axios
            .post(path + '/api/users/get_auth_token/', {
                "email": user.email,
                "password": user.password
            })
            .then(response => {
                const token = response.data.token;
                commit(AUTH_TOKEN, response.data);
                localStorage.setItem('user-token', token);
                axios.defaults.headers.common['Authorization'] = token;
                dispatch(USER_REQUEST)
                .then(() => {
                    commit(DOCS_FILE_CABINET, '');
                    commit(DOCS_SUCCESS, '');
                    dispatch(DOCS_REQUEST)
                    .then(() => {
                        commit(AUTH_AUTH, true);
                        resolve(response);
                    })
                })
            })
            .catch(err => {
                localStorage.removeItem('user-token')
                try {
                    reject(err.response.request.response)
                } catch (error) {
                    reject(err)
                }
            })
        })
    },
    [AUTH_LOGOUT]: ({commit, dispatch}) => {
        return new Promise((resolve, reject) => {
            commit(AUTH_LOGOUT);
            localStorage.removeItem('user-token');
            delete axios.defaults.headers.common['Authorization'];
            resolve();
        })
    }
}

const mutations = {
    [AUTH_TOKEN]: (state, resp) => {
        state.token = resp.token
    },
    [AUTH_AUTH]: (state, resp) => {
        state.auth = resp
    },
    [AUTH_LOGOUT]: (state) => {
        state.token = ''
        state.profile = {}
        state.auth = false
    },
}

export default {
    state,
    getters,
    actions,
    mutations,
}