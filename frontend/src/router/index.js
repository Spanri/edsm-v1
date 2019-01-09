import Vue from 'vue'
import Router from 'vue-router'
import Main from '@/components/Main'
import Auth from '@/components/Auth'

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
	  next()
	  return
	}
	next('/login')
}

const router = new Router({
	mode: 'history',
	routes: [
		{
			path: '/',
			name: 'main',
			component: Auth,
		},
		{
			path: '/auth',
			name: 'auth',
			component: Main,
			beforeEnter: ifNotAuthenticated,
		},
		{
			path: '/account',
			name: 'account',
			component: UserPanel,
			beforeEnter: ifAuthenticated,
		}
	]
})

// router.beforeEach((to, from, next) => {
// 	console.log(router.app.$auth.isAuthenticated());
// 	if(!sessionStorage.getItem('session')){
// 		sessionStorage.setItem('session', router.app.$auth.isAuthenticated() ? true : false)
// 	}
// })

export default router