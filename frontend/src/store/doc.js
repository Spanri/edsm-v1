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
import { conditionalExpression } from 'babel-types';

const state = {
    docs: [],
}

const getters = {
    getDocs: state => state.docs,
    getDoc: (state) => i => {
        return state.docs.filter(d => d.id == i)[0]
    },
    getFolder: state => state.folder,
}

function unique(arr) {
    var obj = {};
    for (var i = 0; i < arr.length; i++) {
        var str = arr[i];
        obj[str] = true;
    }
    console.log(Object.keys(obj))
    return Object.keys(obj);
}

function uniqueArray (a) {
    return [...new Set(a.map(o => JSON.stringify(o)))].map(s => JSON.parse(s))
}

const actions = {
    [DOCS_REQUEST]: ({commit, dispatch, store}, id) => {
        return new Promise((resolve, reject) => {
            axios
            .get('http://127.0.0.1:8000/api/users/all_docs/')
            .then(respCommon => {
                axios
                .get('http://127.0.0.1:8000/api/users/'+ id +'/docs/')
                .then(respUser => {
                    let docs = respCommon.data;
                    docs = docs.concat(respUser.data);
                    let docs2 = docs.reduce((acc, c) => {
                        if (acc.map[c.id]) return acc;
                        acc.map[c.id] = true;
                        acc.docs2.push(c);
                        return acc;
                    }, { map: {}, docs2: [] }).docs2;
                    try {
                        docs2.forEach(d => {
                            d.owner_name = d.user.profile.full_name
                            d.title = d.doc.title;
                        });
                        commit(DOCS_SUCCESS, docs2)
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