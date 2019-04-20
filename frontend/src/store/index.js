import Vue from 'vue'
import Vuex from 'vuex'
import user from './user'
import auth from './auth'

Vue.use(Vuex)
import createPersistedState from 'vuex-persistedstate'
const debug = process.env.NODE_ENV !== 'production'

export default new Vuex.Store({
	modules: {
		user,
		auth,
	},
	strict: debug,
	plugins: [createPersistedState()],
})