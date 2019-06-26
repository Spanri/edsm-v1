import { 
    DOCS_REQUEST,
    DOC_EDIT_NOTIF,
    DOCS_REGS,
    DOCS_REG_CREATE,
    DOCS_REG_EDIT,
    DOCS_REG_DELETE,
    DOCS_REGS_SUCCESS,
    DOCS_FILTER,
    DOCS_FILTER_SUCCESS,
    DOCS_FILE_CABINET_CREATE,
    DOCS_FILE_CABINET_EDIT,
    DOCS_FILE_CABINET_DELETE,
    DOC_UPLOAD,
    DOC_DOWNLOAD,
    DOC_DOWNLOAD_SIGN,
    DOC_DELETE,
    DOC_DELETE_FROM_LOCAL,
    DOC_SIGNATURE,
    DOC_SIGNATURE_CHECK,
    DOC_SIGNATURE_CANCEL,
    DOC_SIGNATURE_AGAIN,
    DOC_SIGNATURE_QUEUE,
    DOC_EDIT,
    DOC_UPDATE,
    DOC_REQUEST,
    ADDIT_RELOAD,
    DOC_REQUEST_SUCCESS,
    DOCS_FILE_CABINETS,
    DOCS_FILE_CABINET,
    DOCS_SUCCESS,
    path,
} from './mutation-types'
import {formatDate} from '../otherFun'
import Vue from 'vue'
import axios from 'axios'

const state = {
    docs: [],
    docsFiltering: [],
    fileCabinets: [],
    regs: [],
    fileCabinet: '',
}

const getters = {
    getDocsOld: state => state.docs,
    getDocs: state => state.docsFiltering,
    getDoc: (state) => i => {
        return state.docs.filter(d => d.doc.id == i)[0]
    },
    getFileCabinets: state => state.fileCabinets,
    getFileCabinet: state => state.fileCabinet,
    getRegs: state => state.regs,
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
                        if (d.initiator != '') {
                            d.initiator = d.initiator.profile.full_name
                        }
                        // d.initiator = d.initiator.profile['id'];
                        if (d.doc.date) d.doc.date = formatDate(d.doc.date);
                        d.date_doc = d.doc.date;
                        if (d.date) d.date = formatDate(d.date);
                        d.date_notif = d.date;
                        d.file_cabinet = d.doc.file_cabinet.name;
                        try{
                            d.reg = d.doc.id + '-' + d.doc.reg.name;
                        }
                        catch(e) {
                            d.reg = d.doc.id
                        }
                        // console.log(d)
                        if (d.date_expire && d.date_expire < new Date()) {
                            console.log(d)
                        }
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
    [DOCS_REGS]: ({ commit, dispatch, rootState }) => {
        return new Promise((resolve, reject) => {
            axios
                .get(path + '/api/docs/regs')
                .then(res => {
                    commit(DOCS_REGS_SUCCESS, res.data)
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
    [DOCS_REG_CREATE]: ({ commit, dispatch, rootState }, name) => {
        return new Promise((resolve, reject) => {
            axios
                .post(path + '/api/docs/regs', {
                    name: name
                }, {
                        headers: { Authorization: "Token " + rootState.auth.token }
                    })
                .then(res => {
                    dispatch(DOCS_REGS)
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
    [DOCS_REG_EDIT]: ({ commit, dispatch, rootState }, data) => {
        return new Promise((resolve, reject) => {
            axios
                .patch(path + '/api/docs/regs/' + data.id, {
                    name: data.name
                }, {
                        headers: { Authorization: "Token " + rootState.auth.token }
                    })
                .then(res => {
                    dispatch(DOCS_REGS)
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
    [DOCS_REG_DELETE]: ({ commit, dispatch, rootState }, data) => {
        return new Promise((resolve, reject) => {
            axios
                .delete(path + '/api/docs/regs/' + data.id, {
                    headers: { Authorization: "Token " + rootState.auth.token }
                })
                .then(res => {
                    dispatch(DOCS_REGS)
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
                    await dispatch(DOC_SIGNATURE, {
                        id: resp.data.doc.id,
                        first: 1
                    })
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
                try {
                    reject(err.response.request.response);
                } catch (error) {
                    reject(err);
                }
            });
        })
    },
    [DOC_DOWNLOAD_SIGN]: ({ commit, dispatch, rootState }, id) => {
        return new Promise((resolve, reject) => {
            axios
                .get(path + '/api/docs/download_sign/' + id + '/', {
                    headers: { Authorization: "Token " + rootState.auth.token }
                })
                .then((response) => {
                    resolve(response.data);
                })
                .catch(err => {
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
    [DOC_SIGNATURE_CHECK]: ({ commit, dispatch, rootState }, id) => {
        return new Promise((resolve, reject) => {
            axios
                .get(path + '/api/docs/' + id + '/check_signature/', {
                    headers: { Authorization: "Token " + rootState.auth.token }
                })
                .then(resp => {
                    resolve(resp.data.check)
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
    [DOC_SIGNATURE_AGAIN]: ({ commit, dispatch, rootState }, data) => {
        return new Promise((resolve, reject) => {
            axios
                .get(path + '/api/docs/signature_again/' + data.id + '/', {
                    headers: {Authorization: "Token " + rootState.auth.token}
                })
                .then(resp => {
                    if(data) {
                        console.log('data', data.data)
                        axios
                        .patch(path + '/api/docs/i/' + data.id, data.data, {
                            headers: { 
                                'Content-Type': 'multipart/form-data',
                                Authorization: "Token " + rootState.auth.token 
                            }
                        })
                        .then(r => {
                            dispatch(DOCS_REQUEST)
                                .then(s => {
                                    resolve(resp.data)
                                })
                        })
                        .catch(err => {
                            try {
                                reject(err.response.request.response)
                            } catch (error) {
                                reject(err)
                            }
                        })
                    } else {
                        dispatch(DOCS_REQUEST)
                            .then(s => {
                                resolve(resp.data)
                            })
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
    [DOC_SIGNATURE_QUEUE]: ({ commit, dispatch, rootState }, id) => {
        return new Promise((resolve, reject) => {
            axios
                .get(path + '/api/docs/signature_queue/' + id + '/', {
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
    [DOC_DELETE_FROM_LOCAL]: ({ commit, dispatch, rootState }, data) => {
        return new Promise((resolve, reject) => {
            axios
                .delete(path + '/api/docs/delete_from_local/' + data.id + '/' + data.type + '/', {
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
    [DOCS_REGS_SUCCESS]: (state, resp) => {
        Vue.set(state, 'regs', resp)
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
    [ADDIT_RELOAD]: (state, resp) => {
        Vue.set(state, 'reload', resp)
    },
}

export default {
    state,
    getters,
    actions,
    mutations,
}