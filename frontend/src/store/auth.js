import { 
    AUTH_REQUEST, 
    AUTH_ERROR, 
    AUTH_SUCCESS, 
    AUTH_LOGOUT,
    USER_REQUEST
} from './mutation-types'
// import apiCall from '../api/common'
import axios from 'axios'

const state = { 
    token: localStorage.getItem('user-token') || '', 
    status: '',
    hasLoadedOnce: false
}

const getters = {
    isAuthenticated: state => !!state.token,
    authStatus: state => state.status,
}

const actions = {
    [AUTH_REQUEST]: ({commit, dispatch}, user) => {
        return new Promise((resolve, reject) => {
            console.log(user);
            commit(AUTH_REQUEST)
            axios
            .post('http://127.0.0.1:8000/api-token-auth/', {
                "username": user.username,
                "password": "nysha2161"
            })
            .then(response => {
                localStorage.setItem('user-token', response.data.token)
                commit(AUTH_SUCCESS, response)
                dispatch(USER_REQUEST)
                resolve(response)
            })
            .catch(err => {
                commit(AUTH_ERROR, err)
                localStorage.removeItem('user-token')
                reject(err)
            })
            // apiCall({url: 'auth', data: user, method: 'POST'})
            // .then(resp => {
            //     localStorage.setItem('user-token', resp.token)
            //     // Here set the header of your ajax library to the token value.
            //     // example with axios
            //     // axios.defaults.headers.common['Authorization'] = resp.token
            //     commit(AUTH_SUCCESS, resp)
            //     dispatch(USER_REQUEST)
            //     resolve(resp)
            // })
            // .catch(err => {
            //     commit(AUTH_ERROR, err)
            //     localStorage.removeItem('user-token')
            //     reject(err)
            // })
        })
    },
    [AUTH_LOGOUT]: ({commit, dispatch}) => {
        return new Promise((resolve, reject) => {
            commit(AUTH_LOGOUT)
            localStorage.removeItem('user-token')
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
        state.hasLoadedOnce = true
    },
    [AUTH_ERROR]: (state) => {
        state.status = 'error'
        state.hasLoadedOnce = true
    },
    [AUTH_LOGOUT]: (state) => {
        state.token = ''
    }
}

export default {
    state,
    getters,
    actions,
    mutations,
}