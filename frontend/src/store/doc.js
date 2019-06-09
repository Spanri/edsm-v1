import { 
    DOCS_REQUEST,
    DOC_EDIT_NOTIF,
    DOC_EDIT_NOTIF_IS_READ,
    DOCS_FILTER,
    DOCS_FILTER_SUCCESS,
    DOCS_FILE_CABINET_CREATE,
    DOCS_FILE_CABINET_EDIT,
    DOCS_FILE_CABINET_DELETE,
    DOC_FOLDER_PAGE,
    DOC_FOLDER_PAGE_PROFILE,
    DOC_UPLOAD,
    DOC_DOWNLOAD,
    DOC_DELETE,
    DOC_SIGNATURE,
    DOC_SIGNATURE_CANCEL,
    DOC_SIGNATURE_AGAIN,
    DOC_EDIT,
    DOC_UPDATE,
    DOC_REQUEST,
    DOC_RELOAD,
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
    fileCabinet: '',
    reload: '',
}

const getters = {
    getDocsOld: state => state.docs,
    getDocs: state => state.docsFiltering,
    getDoc: (state) => i => {
        return state.docs.filter(d => d.doc.id == i)[0]
    },
    getFileCabinets: state => state.fileCabinets,
    getFileCabinet: state => state.fileCabinet,
    getReload: state => state.reload,
}

function formatDate(date) {
    date = new Date(date)
    var year = date.getFullYear(),
        month = date.getMonth() + 1, // months are zero indexed
        monthFormatted = month < 10 ? "0" + month : month,
        day = date.getDate(),
        dayFormatted = day < 10 ? "0" + day : day,
        hour = date.getHours(),
        minute = date.getMinutes(),
        minuteFormatted = minute < 10 ? "0" + minute : minute;

    return dayFormatted + "-" + monthFormatted + "-" + year + " " + hour + ":" +
        minuteFormatted;
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
                        if (d.doc.date) d.doc.date = formatDate(d.doc.date);
                        d.date_doc = d.doc.date;
                        d.date_notif = d.date;
                        d.file_cabinet = d.doc.file_cabinet.name;
                        let dd = d.is_read.filter(d0 => {
                            return d0.id == rootState.user.profile.id
                        })
                        let myDoc = d.status == 0 && d.user.id == rootState.user.profile.id
                        d.rowBackg = (dd.length != 0 || myDoc) ? "white" : "#dcdbfc"
                    });
                    let d1 = resp.data.filter(d => {
                        return d.rowBackg == "#dcdbfc"
                    })
                    let d2 = resp.data.filter(d => {
                        return d.rowBackg == "white"
                    })
                    resp.data = d1.concat(d2);
                    // console.log('resp.data', resp.data)
                    commit(DOCS_SUCCESS, resp.data);
                    // dispatch(DOCS_FILTER)
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
    [DOC_REQUEST]: ({ commit, dispatch, rootState }, id) => {
        return new Promise((resolve, reject) => {
            axios
                .get(path + '/api/users/notif/' + id, {
                    headers: { Authorization: "Token " + rootState.auth.token }
                })
                .then(resp => {
                    // let updateId = rootState.doc.docs.findIndex(x => x.id == id);
                    // rootState.doc.docs[updateId] = resp.data;
                    resolve(resp)
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
    [DOC_UPDATE]: ({ commit, dispatch, rootState }, id) => {
        return new Promise((resolve, reject) => {
            axios
                .get(path + '/api/users/notif/' + id, {
                    headers: { Authorization: "Token " + rootState.auth.token }
                })
                .then(resp => {
                    let updateId = rootState.doc.docs.findIndex(x => x.id == id);
                    
                    // resp.data.full_name = resp.data.user.profile.full_name
                    // resp.data.title = resp.data.doc.title;
                    // resp.data.date_doc = resp.data.doc.date;
                    // resp.data.date_notif = resp.data.date;
                    // resp.data.file_cabinet = resp.data.doc.file_cabinet.name;
                    // let dd = resp.data.is_read.filter(d0 => {
                    //     return d0.id == rootState.user.profile.id
                    // })
                    // let myDoc = resp.data.status == 0 && resp.data.user.id == rootState.user.profile.id
                    // resp.data.rowBackg = (dd.length != 0 || myDoc) ? "white" : "#dcdbfc"

                    rootState.doc.docs[updateId] = resp.data;
                    resolve(resp)
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
    [DOC_EDIT_NOTIF]: ({ commit, dispatch, rootState }, data) => {
        return new Promise((resolve, reject) => {
            console.log('data hide', data)
            axios
                .get(path + '/api/users/' + data.user + '/notif/' + data.notif + '/' + data.pk3 +'/', {
                    headers: { Authorization: "Token " + rootState.auth.token }
                })
                .then(resp => {
                    try {
                        dispatch(DOC_UPDATE, resp.data.id)
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
                let d = rootState.doc.docs.filter(r => r.doc.file_cabinet.id == rootState.doc.fileCabinet.id)
                commit(DOCS_FILTER_SUCCESS, d)
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
    [DOC_UPLOAD]: ({commit, dispatch, rootState}, data) => {
        return new Promise((resolve, reject) => {
            axios
                .post(path + '/api/docs/i',
                    data.d, { headers: {
                        'Content-Type': 'multipart/form-data',
                        Authorization: "Token " + rootState.auth.token
                    }
                })
                .then(async resp => {
                    await dispatch(DOC_SIGNATURE, {
                        id: resp.data.doc.id,
                        first: 1
                    })
                    if(data.signature_request.length != 0) {
                        await data.signature_request.forEach((s, i) => {
                            axios
                                .post(path + '/api/users/notif', {
                                    doc_id: resp.data.doc.id,
                                    user_id: s.id,
                                    status: i == 0 ? 2 : 1,
                                    queue: i,
                                })
                                .catch(err => {
                                    try {
                                        reject(err.response.request.response)
                                    } catch (error) {
                                        reject(err)
                                    }
                                })
                        })
                    }
                    if (data.show_request.length != 0) {
                        await data.show_request.forEach(s => {
                            axios
                                .post(path + '/api/users/notif', {
                                    doc_id: resp.data.doc.id,
                                    user_id: s.id,
                                    status: 5,
                                })
                                .catch(err => {
                                    try {
                                        reject(err.response.request.response)
                                    } catch (error) {
                                        reject(err)
                                    }
                                })
                        })
                    }
                    // dispatch(DOC_UPDATE, resp.data.id)
                    await resolve(resp.data)
                })
                .catch(err => {
                    try {
                        reject(err.response.request.response);
                    } catch (error) {
                        reject(err);
                    }
                })
        })
    },
    [DOC_DOWNLOAD]: ({ commit, dispatch, rootState }, id) => {
        return new Promise((resolve, reject) => {
            axios
            .get(path + '/api/docs/download/' + id + '/', {
                headers: { Authorization: "Token " + rootState.auth.token }
            })
            .then((response) => {
                resolve(response.data);
            })
            .catch(err => {
                console.log('response.data')
                try {
                    reject(err.response.request.response);
                } catch (error) {
                    reject(err);
                }
            });
        })
    },
    [DOC_SIGNATURE]: ({ commit, dispatch, rootState }, data) => {
        return new Promise((resolve, reject) => {
            axios
                .get(path + '/api/docs/add_signature/' + data.id + '/' + data.first + '/', {
                    headers: { Authorization: "Token " + rootState.auth.token }
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
    // не работает пока что
    [DOC_SIGNATURE_CANCEL]: ({ commit, dispatch, rootState }, data) => {
        return new Promise((resolve, reject) => {
            axios
                .post(path + '/api/docs/cancel_signature/' + data.id + '/', data.data, {
                    headers: { Authorization: "Token " + rootState.auth.token }
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
    [DOC_SIGNATURE_AGAIN]: ({ commit, dispatch, rootState }, id) => {
        return new Promise((resolve, reject) => {
            console.log(id)
            axios
                .get(path + '/api/docs/signature_again/' + id + '/', {
                    headers: { Authorization: "Token " + rootState.auth.token }
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
    [DOC_DELETE]: ({ commit, dispatch, rootState }, id) => {
        return new Promise((resolve, reject) => {
            axios
                .delete(path + '/api/docs/i/' + id, {
                    headers: { Authorization: "Token " + rootState.auth.token }
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
    [DOC_EDIT]: ({ commit, dispatch, rootState }, data) => {
        return new Promise((resolve, reject) => {
            let id = data.id;
            delete data.id;
            axios
                .patch(path + '/api/docs/i/' + id, data, {
                    headers: { Authorization: "Token " + rootState.auth.token }
                })
                .then(res => {
                    dispatch(DOCS_REQUEST)
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
    [DOC_RELOAD]: (state, resp) => {
        Vue.set(state, 'reload', resp)
    },
}

export default {
    state,
    getters,
    actions,
    mutations,
}