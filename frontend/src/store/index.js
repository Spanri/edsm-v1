import Vue from 'vue'
import Vuex from 'vuex'
import user from './user'
import auth from './auth'

Vue.use(Vuex)

const debug = process.env.NODE_ENV !== 'production'

export default new Vuex.Store({
	modules: {
		user,
		auth,
	},
	strict: debug,
})