import { 
    DOCS_REQUEST,
    DOC_SUCCESS,
    DOC_FOLDER_SUCCESS,
    DOC_FOLDER_PAGE,
    DOC_FOLDER_PAGE_PROFILE,
    DOC_FOLDERS_REQUEST,
    DOC_FOLDERS_UPDATE,
    DOC_FOLDERS_UPDATE_SUCCESS,
    DOC_ERROR,
    DOC_UPLOAD,
    DOC_SIGNATURE,
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
}

const getters = {
    getDocs: state => state.docs,
    getDoc: (state) => i => {
        return state.docs.filter(d => d.doc.id == i)[0]
    },
}

const actions = {
    [DOCS_REQUEST]: ({commit, dispatch, store, rootState}) => {
        return new Promise((resolve, reject) => {
            axios
            .get(path + '/api/users/' + rootState.user.profile.id + '/notif/')
            .then(respNotif => {
                axios
                    .get(path + '/api/users/' + rootState.user.profile.id +'/docs/')
                .then(respUser => {
                    let docs = respNotif.data;
                    docs = docs.concat(respUser.data);
                    axios
                        .get(path + '/api/users/all_docs/')
                        .then(respCommon => {
                            docs = docs.concat(respCommon.data);
                            let docs2 = docs.reduce((acc, c) => {
                                if (acc.map[c.id]) return acc;
                                acc.map[c.id] = true;
                                acc.docs2.push(c);
                                return acc;
                            }, { map: {}, docs2: [] }).docs2;
                            console.log('docs2', docs2)
                            try {
                                docs2.forEach(d => {
                                    d.full_name = d.user.profile.full_name
                                    d.title = d.doc.title;
                                    d.date_doc = d.doc.date;
                                });
                                resolve(docs2)
                                commit(DOCS_SUCCESS, docs2)
                            } catch (err) {
                                console.log(err)
                            }
                        });
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
    // РЕШИТЬ, ДОБАВЛЯТЬ ЛИ ПРАВА
    [DOC_UPLOAD]: ({commit, dispatch, rootState}, data) => {
        return new Promise((resolve, reject) => {
            console.log(data)
            axios
                .post(path + '/api/docs',
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
                                    message: 'Вас просят подписать документ.',
                                    is_owner: false,
                                    is_signature_request: true,
                                    queue: i,
                                    is_queue: i==0 ? true : false
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
                                    is_owner: false,
                                    is_signature_request: false
                                })
                                .catch(err => {
                                    try {
                                        reject(err.response.request.response)
                                    } catch (error) {
                                        reject(err)
                                    }
                                })
                        })
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
            console.log('id', id)
            axios
                .post(path + '/api/users/notif/add_signature/', {
                    id: id
                })
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