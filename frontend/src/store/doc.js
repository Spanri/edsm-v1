import { 
    DOCS_REQUEST,
    DOC_SUCCESS,
    DOC_FOLDER_SUCCESS,
    DOC_FOLDER_REQUEST,
    DOC_FOLDERS_REQUEST,
    DOC_FOLDERS_UPDATE,
    DOC_FOLDERS_UPDATE_SUCCESS,
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
}

const getters = {
    getDocs: state => state.docs,
    getDoc: (state) => i => {
        return state.docs.filter(
            d => d.doc.id == i && d.is_owner == true
        )[0]
    },
    getFolder: state => state.folder,
}

const actions = {
    [DOCS_REQUEST]: ({commit, dispatch, store, rootState}) => {
        return new Promise((resolve, reject) => {
            axios
            .get('http://127.0.0.1:8000/api/users/all_docs/')
            .then(respCommon => {
                axios
                .get('http://127.0.0.1:8000/api/users/' + rootState.user.profile.id +'/docs/')
                .then(respUser => {
                    let docs = respCommon.data;
                    docs = docs.concat(respUser.data);
                    axios
                        .get(path + '/api/users/' + rootState.user.profile.id + '/notif/')
                        .then(respNotif => {
                            // console.log(respNotif.data)
                            docs = docs.concat(respNotif.data);
                            let docs2 = docs.reduce((acc, c) => {
                                if (acc.map[c.id]) return acc;
                                acc.map[c.id] = true;
                                acc.docs2.push(c);
                                return acc;
                            }, { map: {}, docs2: [] }).docs2;
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
    [DOC_REQUEST]: ({commit, dispatch}, id) => {
        return new Promise((resolve, reject) => {
            // axios
            // .post(`http://127.0.0.1:8000/api/docs`, {
            //     "id" : id
            // })
            // .then(response => {
            //     commit(DOCS_SUCCESS, response)
            // })
            // .catch(resp => {
            //     commit(DOC_ERROR)
            // })
            let response =
            {
                "id": 1,
                "owner_id": 1,
                "title": "Файл1",
                "file": "http://localhost:8000/uVyuTHdBDN8.jpg",
                "description": "gngfnfghjhg fdg terte t",
                "date": "2019-05-12",
                "common": true,
                "signature": null
            };
            response.owner_name = response.user.profile.full_name
            response.title = response.doc.title;
            resolve(response)
        })
    },
    // РЕШИТЬ, ДОБАВЛЯТЬ ЛИ ПРАВА
    [DOC_UPLOAD]: ({commit, dispatch, rootState}, data) => {
        return new Promise((resolve, reject) => {
            console.log(data)
            axios
                .post(path + '/api/docs',
                    data, { headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                })
                .then(resp => {
                    axios
                        .post(path + '/api/users/notif', {
                            doc_id: resp.data.id,
                            user_id: rootState.user.profile.id,
                            is_owner: true,
                            date: new Date().toISOString().slice(0, 10),
                            is_signature_request: true
                        })
                        .then(res => {
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
    [DOCS_SUCCESS]: (state, resp) => {
        Vue.set(state, 'docs', resp)
    },
    [DOC_REQUEST_SUCCESS]: (state, resp) => { 
        state.doc.push(resp)
    },
}

export default {
    state,
    getters,
    actions,
    mutations,
}