import { 
    AUTH_REQUEST, 
    AUTH_ERROR, 
    AUTH_SUCCESS, 
    AUTH_LOGOUT,
    USER_REQUEST,
    AUTH_LOGIN
} from './mutation-types'
// import apiCall from '../api/common'
import axios from 'axios'

const state = { 
    token: localStorage.getItem('user-token') || '', 
    status: '',
    // login: false,
    // hasLoadedOnce: false
}

const getters = {
    isAuthenticated: state => !!state.token,
    authStatus: state => state.status,
    // login: state => state.login
}

const actions = {
    [AUTH_REQUEST]: ({commit, dispatch}, user) => {
        return new Promise((resolve, reject) => {
            commit(AUTH_REQUEST)
            // axios
            // .post('http://127.0.0.1:8000/api-token-auth/', {
            //     "email": user.email,
            //     "password": "nysha2161"
            // })
            // .then(response => {
            //     const token = response.data.token
            //     localStorage.setItem('user-token', token)
            //     axios.defaults.headers.common['Authorization'] = token
            //     commit(AUTH_SUCCESS, response)
            //     dispatch(USER_REQUEST)
            //     resolve(response)
            // })
            // .catch(err => {
            //     commit(AUTH_ERROR, err)
            //     localStorage.removeItem('user-token')
            //     reject(err)
            // })
            let response = {token:'ea135929105c4f29a0f5117d2960926f'};
            localStorage.setItem('user-token', response.token);
            axios.defaults.headers.common['Authorization'] = response.token
            commit(AUTH_SUCCESS, response)
            dispatch(USER_REQUEST)
        })
    },
    [AUTH_LOGOUT]: ({commit, dispatch}) => {
        return new Promise((resolve, reject) => {
            commit(AUTH_LOGOUT)
            localStorage.removeItem('user-token')
            delete axios.defaults.headers.common['Authorization']
            resolve()
        })
    }
}

const mutations = {
    [AUTH_REQUEST]: (state) => {
        state.status = 'loading'
    },
    [AUTH_SUCCESS]: (state, resp) => {
        state.status = 'success'
        state.token = resp.token
    },
    [AUTH_ERROR]: (state) => {
        state.status = 'error'
    },
    [AUTH_LOGOUT]: (state) => {
        state.token = ''
    },
}

export default {
    state,
    getters,
    actions,
    mutations,
}