import { 
    DOC_REQUEST,
    DOC_SUCCESS,
    DOC_FOLDER_SUCCESS,
    DOC_FOLDER_REQUEST,
    DOC_FOLDER_UPDATE,
    DOC_FOLDER_UPDATE_SUCCESS,
    DOC_ERROR
} from './mutation-types'
import Vue from 'vue'
import apiCall from '../api/common'
import axios from 'axios'

const state = {
    doc: [],
    folder: [],
}

const getters = {
    getDoc: state => state.doc,
    getFolder: state => state.folder,
}

const actions = {
    [DOC_REQUEST]: ({commit, dispatch}, id) => {
        // axios
        // .post(`http://127.0.0.1:8000/doc`, {
        //     "id" : id
        // })
        // .then(response => {
        //     commit(DOC_SUCCESS, response)
        // })
        // .catch(resp => {
        //     commit(DOC_ERROR)
        // })
        let response = [
            { 
                'Номер': 'Chuck Norris1', 
                'Название': Infinity,
                'Инициатор': 'dfg11',
                'Столбец': 'dfg'
            },
            { 
                'Номер': 'Bruce Lee', 
                'Название': 9000,
                'Инициатор': 'dfkkkg',
                'Столбец': 'dfg'
            },
            { 
                'Номер': 'Jackie Chan', 
                'Название': 7000,
                'Инициатор': 'dbbbfg',
                'Столбец': 'dfg'
            },
            { 
                'Номер': 'Jet Li', 
                'Название': 8000,
                'Инициатор': 'dvvvfg',
                'Столбец': 'dfg'
            }
        ];
        commit(DOC_SUCCESS, response)
    },
    [DOC_FOLDER_REQUEST]: ({commit, dispatch}) => {
        // axios
        // .get(`http://127.0.0.1:8000/folders`)
        // .then(response => {
        //     commit(DOC_FOLDER_SUCCESS, response)
        // })
        // .catch(resp => {
        //     commit(DOC_ERROR)
        // })
        let response = [
            {title: "ДОКУМЕНТЫ СТУДЕНТОВ", ref: "3"},
            {title: "ДРУГИЕ ДОКУМЕНТЫ", ref: "4"}
        ]
        commit(DOC_FOLDER_SUCCESS, response)
    },
    [DOC_FOLDER_UPDATE]: ({commit, dispatch}, newFolder) => {
        state.folder.push(newFolder);
        // axios
        // .post(`http://127.0.0.1:8000/folders`, {
        //     "newFolder": newFolder
        // })
        // .then(response => {
        //     commit(DOC_FOLDER_UPDATE_SUCCESS, newFolder)
        // })
        // .catch(resp => {
        //     commit(DOC_ERROR)
        // })
        commit(DOC_FOLDER_UPDATE_SUCCESS, newFolder)
        console.log("Сделан UPDATE.")
    }
}

const mutations = {
    [DOC_REQUEST]: (state) => {
        state.status = 'loading'
    },
    [DOC_SUCCESS]: (state, resp) => {
        state.status = 'success'
        Vue.set(state, 'doc', resp)
    },
    [DOC_FOLDER_SUCCESS]: (state, resp) => {
        state.status = 'success'
        Vue.set(state, 'folder', resp)
    },
    [DOC_FOLDER_UPDATE_SUCCESS]: (state, resp) => {
        state.status = 'success'
        state.folder.push(resp)
    },
    [DOC_ERROR]: (state) => {
        state.status = 'error'
    },
}

export default {
    state,
    getters,
    actions,
    mutations,
}