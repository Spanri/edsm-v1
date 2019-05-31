import { 
    DOCS_REQUEST,
    DOCS_FILTER,
    DOCS_FILTER_SUCCESS,
    DOCS_FILE_CABINET_CREATE,
    DOCS_FILE_CABINET_EDIT,
    DOCS_FILE_CABINET_DELETE,
    DOC_FOLDER_PAGE,
    DOC_FOLDER_PAGE_PROFILE,
    DOC_UPLOAD,
    DOC_DELETE,
    DOC_SIGNATURE,
    DOC_REQUEST_SUCCESS,
    DOCS_FILE_CABINETS,
    DOCS_FILE_CABINET,
    DOCS_SUCCESS,
    path,
} from './mutation-types'
import Vue from 'vue'
import axios from 'axios'

const state = {
    docs: [],
    docsFiltering: [],
    fileCabinets: [],
    fileCabinet: ''
}

const getters = {
    getDocsOld: state => state.docs,
    getDocs: state => state.docsFiltering,
    getDoc: (state) => i => {
        return state.docs.filter(d => d.doc.id == i)[0]
    },
    getFileCabinets: state => state.fileCabinets,
    getFileCabinet: state => state.fileCabinet,
}

const actions = {
    [DOCS_REQUEST]: ({commit, dispatch, rootState}) => {
        return new Promise((resolve, reject) => {
            axios
            .get(path + '/api/users/' + rootState.user.profile.id + '/notif/', {
                headers: { Authorization: "Token " + rootState.auth.token }
            })
            .then(resp => {
                try {
                    resp.data.forEach(d => {
                        d.full_name = d.user.profile.full_name
                        d.title = d.doc.title;
                        d.date_doc = d.doc.date;
                    });
                    commit(DOCS_SUCCESS, resp.data);
                    dispatch(DOCS_FILTER)
                    resolve(resp.data);
                } catch (err) {
                    console.log(err)
                }
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
    [DOCS_FILTER]: ({ commit, dispatch, rootState }) => {
        return new Promise((resolve, reject) => {
            axios
            .get(path + '/api/docs/fileCabinets')
            .then(res => {
                commit(DOCS_FILE_CABINETS, res.data)
                if (rootState.doc.fileCabinet == '') commit(DOCS_FILE_CABINET, res.data[0]);
                let d = rootState.doc.docs.filter(r => r.doc.fileCabinet.id == rootState.doc.fileCabinet.id)
                commit(DOCS_FILTER_SUCCESS, d)
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
    [DOCS_FILE_CABINET_CREATE]: ({ commit, dispatch, rootState }, name) => {
        return new Promise((resolve, reject) => {
            axios
                .post(path + '/api/docs/fileCabinets', {
                    name: name
                }, {
                    headers: { Authorization: "Token " + rootState.auth.token }
                })
                .then(res => {
                    dispatch(DOCS_FILTER)
                    resolve(res)
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
    [DOCS_FILE_CABINET_EDIT]: ({ commit, dispatch, rootState }, data) => {
        return new Promise((resolve, reject) => {
            axios
                .patch(path + '/api/docs/fileCabinets/' + data.id, {
                    name: data.name
                }, {
                    headers: { Authorization: "Token " + rootState.auth.token }
                })
                .then(res => {
                    dispatch(DOCS_FILTER)
                    resolve(res)
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
    [DOCS_FILE_CABINET_DELETE]: ({ commit, dispatch, rootState }, data) => {
        return new Promise((resolve, reject) => {
            axios
                .delete(path + '/api/docs/fileCabinets/' + data.id, {
                    headers: { Authorization: "Token " + rootState.auth.token }
                })
                .then(res => {
                    dispatch(DOCS_FILTER)
                    resolve(res)
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
    // РЕШИТЬ, ДОБАВЛЯТЬ ЛИ ПРАВА
    [DOC_UPLOAD]: ({commit, dispatch, rootState}, data) => {
        return new Promise((resolve, reject) => {
            console.log(data)
            axios
                .post(path + '/api/docs/i',
                    data.d, { headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                })
                .then(resp => {
                    if(data.signature_request) {
                        data.signature_request.forEach((s, i) => {
                            console.log(s)
                            axios
                                .post(path + '/api/users/notif', {
                                    doc_id: resp.data.id,
                                    user_id: s.id,
                                    status: i == 0 ? 2 : 1,
                                    // is_owner: false,
                                    // is_signature_request: true,
                                    queue: i,
                                    // is_queue: i==0 ? true : false
                                })
                                .catch(err => {
                                    try {
                                        reject(err.response.request.response)
                                    } catch (error) {
                                        reject(err)
                                    }
                                })
                        })
                        data.show_request.forEach(s => {
                            console.log(s)
                            axios
                                .post(path + '/api/users/notif', {
                                    doc_id: resp.data.id,
                                    user_id: s.id,
                                    status: 5,
                                    // is_owner: false,
                                    // is_signature_request: false
                                })
                                .catch(err => {
                                    try {
                                        reject(err.response.request.response)
                                    } catch (error) {
                                        reject(err)
                                    }
                                })
                        })
                        dispatch(DOCS_REQUEST)
                        resolve(resp.data)
                    }
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
    [DOC_SIGNATURE]: ({ commit, dispatch, rootState }, id) => {
        return new Promise((resolve, reject) => {
            axios
                .get(path + '/api/docs/add_signature/' + id + '/')
                .then(resp => {
                    resolve(resp.data)
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
    [DOC_DELETE]: ({ commit, dispatch, rootState }, id) => {
        return new Promise((resolve, reject) => {
            axios
                .delete(path + '/api/docs/i/' + id)
                .then(resp => {
                    resolve(resp.data)
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
    // [DOC_REQUEST]: ({commit, dispatch}, id) => {
    //     return new Promise((resolve, reject) => {
    //         // axios
    //         // .post(`http://127.0.0.1:8000/api/docs`, {
    //         //     "id" : id
    //         // })
    //         // .then(response => {
    //         //     commit(DOCS_SUCCESS, response)
    //         // })
    //         // .catch(resp => {
    //         //     commit(DOC_ERROR)
    //         // })
    //         let response =
    //         {
    //             "id": 1,
    //             "owner_id": 1,
    //             "title": "Файл1",
    //             "file": "http://localhost:8000/uVyuTHdBDN8.jpg",
    //             "description": "gngfnfghjhg fdg terte t",
    //             "date": "2019-05-12",
    //             "common": true,
    //             "signature": null
    //         };
    //         response.owner_name = response.user.profile.full_name
    //         response.title = response.doc.title;
    //         resolve(response)
    //     })
    // },
}

const mutations = {
    [DOCS_SUCCESS]: (state, resp) => {
        Vue.set(state, 'docs', resp)
    },
    [DOCS_FILTER_SUCCESS]: (state, resp) => {
        Vue.set(state, 'docsFiltering', resp)
    },
    [DOCS_FILE_CABINETS]: (state, resp) => {
        Vue.set(state, 'fileCabinets', resp)
    },
    [DOCS_FILE_CABINET]: (state, resp) => {
        Vue.set(state, 'fileCabinet', resp)
    },
    [DOC_REQUEST_SUCCESS]: (state, resp) => { 
        state.doc.push(resp)
    },
    [DOC_FOLDER_PAGE]: (state, resp) => {
        Vue.set(state, 'page', resp)
    },
    [DOC_FOLDER_PAGE_PROFILE]: (state, resp) => {
        Vue.set(state, 'pageProfile', resp)
    },
}

export default {
    state,
    getters,
    actions,
    mutations,
}