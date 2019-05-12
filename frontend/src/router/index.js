import Vue from 'vue'
import Router from 'vue-router'
import Main from '@/components/Main'
import Auth from '@/components/Auth'
import Profile from '@/components/profile/Profile'
import EditProfile from '@/components/profile/EditProfile'
import Grid from '@/components/addit/Grid'
import Adm from '@/components/profile/Adm'
import Document from '@/components/Document'
import AddDoc from '@/components/AddDoc'
import NotFound from '@/components/NotFound'
import store from '../store'
import VeeValidate from 'vee-validate';

Vue.use(Router)
Vue.use(VeeValidate);

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
	next('/auth')
}

const ifAdm = (to, from, next) => {
	if (store.getters.getProfile.is_staff) {
		next()
		return
	}
	next('/')
}

const router = new Router({
	mode: 'history',
	routes: [
		{
			path: '/',
			// name: 'main',
			component: Main,
			children: [
				{
					path: '',
					redirect: '/d/all',
				},
				{
					path: 'd/:id',
					component: Grid,
					props: {
						columns: [
							{key: 'title', title: 'Название'},
							{key: 'owner_name', title: 'Владелец'},
							{key: 'date', title: 'Дата добавления'},
						],
					} 
				},
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
			path: '/addDoc',
			name: 'addDoc',
			component: AddDoc,
			beforeEnter: ifAuthenticated,
		},
		{
			path: '/doc/:id',
			name: 'doc',
			component: Document,
			props: true,
			beforeEnter: ifAuthenticated,
		},
		{ 
			path: '/editProfile', 
			name: 'editProfile',
			component: EditProfile, 
			beforeEnter: ifAuthenticated },
		{
			path: '/profile',
			redirect: '/profile/notif',
			component: Profile,
			children: [
				{
					path: 'notif',
					name: 'notif',
					component: Grid,
					props: {
						id: "notif",
						columns: [
							{key: 'user', title: 'Инициатор'},
							{key: 'message', title: 'Сообщение'},
							{key: 'doc', title: 'Документ'},
							{key: 'date', title: 'Дата добавления'},
						],
					} 
				},
				{ path: 'edit', component: EditProfile },
				{ path: 'adm', component: Adm, beforeEnter: ifAdm, },
			],
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