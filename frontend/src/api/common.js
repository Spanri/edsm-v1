import axios from 'axios'

export const HTTP = axios.create({
    baseURL: 'http://localhost:8000/'
})

export const API_URL = 'http://localhost:3001/'
export const LOGIN_URL = API_URL + 'sessions/create/'
export const SIGNUP_URL = API_URL + 'users/'