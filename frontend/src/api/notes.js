import { HTTP, API_URL, LOGIN_URL, SIGNUP_URL } from './common'

export const Note = {
	create (config) {
		return HTTP.post('/notes/', config).then(response => {
		return response.data
		})
	},
	delete (note) {
		return HTTP.delete(`/notes/${note.id}/`)
	},
	list () {
		return HTTP.get('/notes/').then(response => {
		return response.data
		})
	}
}