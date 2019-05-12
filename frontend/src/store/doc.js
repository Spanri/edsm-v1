import { 
    DOCS_REQUEST,
    DOC_SUCCESS,
    DOC_FOLDER_SUCCESS,
    DOC_FOLDER_REQUEST,
    DOC_FOLDER_UPDATE,
    DOC_FOLDER_UPDATE_SUCCESS,
    DOC_ERROR,
    DOC_UPLOAD,
    DOC_UPLOAD_SUCCESS,
    DOC_REQUEST,
    DOC_REQUEST_SUCCESS,
    DOCS_SUCCESS,
    path,
} from './mutation-types'
import Vue from 'vue'
import axios from 'axios'

const state = {
    docs: [],
    doc: {},
    folder: [],
}

const getters = {
    getDocs: state => state.docs,
    getDoc: state => state.doc,
    getFolder: state => state.folder,
}

const actions = {
    [DOCS_REQUEST]: ({commit, dispatch}, id) => {
        // axios
        // .post(`http://127.0.0.1:8000/doc/docsRequest`, {
        //     "id" : id
        // })
        // .then(response => {
        //     commit(DOCS_SUCCESS, response)
        // })
        // .catch(resp => {
        //     commit(DOC_ERROR)
        // })
        let response = [
            { 
                id: 1,
                'Номер': 'Chuck Norris1', 
                'Название': Infinity,
                'Инициатор': 'dfg11',
                'Столбец': 'dfg'
            },
            { 
                id: 2,
                'Номер': 'Bruce Lee', 
                'Название': 9000,
                'Инициатор': 'dfkkkg',
                'Столбец': 'dfg'
            },
            { 
                id: 3,
                'Номер': 'Jackie Chan', 
                'Название': 7000,
                'Инициатор': 'dbbbfg',
                'Столбец': 'dfg'
            },
            { 
                id: 4,
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
        // .get(`http://127.0.0.1:8000/doc/folderRequest`)
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
        // .post(`http://127.0.0.1:8000/doc/folderUpdate`, {
        //     "newFolder": newFolder
        // })
        // .then(response => {
        //     commit(DOC_SUCCESS, response)
        // })
        // .catch(resp => {
        //     commit(DOC_ERROR)
        // })
        commit(DOC_FOLDER_UPDATE_SUCCESS, newFolder)
        console.log("Сделан UPDATE.")
    },
    [DOC_UPLOAD]: ({commit, dispatch}, data) => {
        // axios
        // .post(`http://127.0.0.1:8000/doc/upload`, {
        //     "file": data.file,
        //     "image": data.image,
        //     "description": data.description,
        //     "common": data.common
        // })
        // .then(response => {
        //     commit(DOC_SUCCESS, data)
        // })
        // .catch(resp => {
        //     commit(DOC_ERROR)
        // })
        commit(DOC_SUCCESS)
        let response = '1234';
        return response;
    },
    [DOC_REQUEST]: ({commit, dispatch}, id) => {
        // axios
        // .post(`http://127.0.0.1:8000/doc/request`, {
        //     "id" : id
        // })
        // .then(response => {
        //     commit(DOC_SUCCESS, response)
        // })
        // .catch(resp => {
        //     commit(DOC_ERROR)
        // })
        let response = {
            id: 1,
            image: '',
            title: 'Chuck Norris1', 
            description: 'Infinity',
            common: true,
        };
        commit(DOC_SUCCESS)
        return response;
    },
}

const mutations = {
    [DOCS_REQUEST]: (state) => {
        state.status = 'loading'
    },
    [DOCS_SUCCESS]: (state, resp) => {
        state.status = 'success'
        Vue.set(state, 'doc', resp)
    },
    [DOC_SUCCESS]: (state) => {
        state.status = 'success'
    },
    [DOC_FOLDER_SUCCESS]: (state, resp) => {
        state.status = 'success'
        Vue.set(state, 'folder', resp)
    },
    [DOC_UPLOAD_SUCCESS]: (state) => {
        state.status = 'success'
    },
    [DOC_REQUEST_SUCCESS]: (state, resp) => {
        state.status = 'success'
        state.doc.push(resp)
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