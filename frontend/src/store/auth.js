import { 
    AUTH_REQUEST,
    AUTH_TOKEN,
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
}

const getters = {
    token: state => state.token,
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
            .then(async response => {
                const token = response.data.token;
                await commit(AUTH_TOKEN, response.data);
                localStorage.setItem('user-token', token);
                axios.defaults.headers.common['Authorization'] = token;
                await dispatch(USER_REQUEST);
                await commit(DOCS_FILE_CABINET, '');
                await commit(DOCS_SUCCESS, '');
                await dispatch(DOCS_REQUEST);
                resolve(response);
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
    [AUTH_LOGOUT]: (state) => {
        state.token = ''
        state.profile = {}
    },
}

export default {
    state,
    getters,
    actions,
    mutations,
}