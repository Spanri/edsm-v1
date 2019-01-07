import Vue from 'vue'
import Vuex from 'vuex'
import { Note } from '../api/notes'
import {
	ADD_NOTE,
	REMOVE_NOTE,
	SET_NOTES
} from './mutation-types.js'

Vue.use(Vuex)

// Состояние
const state = {
	  session: false,
}

// Геттеры
const getters = {
	session: state => state.session  
}

// Мутации
const mutations = {
	session (state, session) { state.session = session },
}

// Действия
const actions = {
	createNote ({ commit }, noteData) {
		Note.create(noteData).then(note => {
			commit(ADD_NOTE, note)
		})
	},
	deleteNote ({ commit }, note) {
		Note.delete(note).then(response => {
			commit(REMOVE_NOTE, note)
		})
	},
	getNotes ({ commit }) {
		Note.list().then(notes => {
			commit(SET_NOTES, { notes })
		})
	}
}

export default new Vuex.Store({
	state,
	getters,
	actions,
	mutations
})