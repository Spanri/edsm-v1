import Vue from 'vue'
import Router from 'vue-router'
import Main from '@/components/Main'
import Auth from '@/components/Auth'
import Profile from '@/components/Profile'
import Document from '@/components/Document'
import NotFound from '@/components/NotFound'
import store from '../store'

Vue.use(Router)

const ifNotAuthenticated = (to, from, next) => {
	if (!store.getters.isAuthenticated) {
	  next()
	  return
	}
	next('/')
}
  
const ifAuthenticated = (to, from, next) => {
	if (store.getters.isAuthenticated) {
		console.log(store.getters.getProfile)
	  next()
	  return
	}
	next('/auth')
}

const router = new Router({
	mode: 'history',
	routes: [
		{
			path: '/',
			// name: 'main',
			component: Main,
			children: [
				{ path: '', component: Profile },
				{ path: 'a', component: Document },
			],
			beforeEnter: ifAuthenticated,
		},
		{
			path: '/auth',
			name: 'auth',
			component: Auth,
			beforeEnter: ifNotAuthenticated,
		},
		{
			path: '/profile',
			name: 'profile',
			component: Profile,
			beforeEnter: ifAuthenticated,
		},
		{ path: '*', component: NotFound }
	]
})

// router.beforeEach((to, from, next) => {
// 	console.log(router.app.$auth.isAuthenticated());
// 	if(!sessionStorage.getItem('session')){
// 		sessionStorage.setItem('session', router.app.$auth.isAuthenticated() ? true : false)
// 	}
// })

export default router