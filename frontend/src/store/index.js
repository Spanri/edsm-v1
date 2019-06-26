import Vue from 'vue'
import Vuex from 'vuex'
import user from './user'
import auth from './auth'
import doc from './doc'
import addit from './addit'

Vue.use(Vuex)
import createPersistedState from 'vuex-persistedstate'
const debug = process.env.NODE_ENV !== 'production'

export default new Vuex.Store({
	modules: {
		user,
		auth,
		doc,
		addit
	},
	strict: debug,
	plugins: [createPersistedState()],
})