import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Auth from '@/components/Auth'
import Profile from '@/components/profile/Profile'
import EditProfile from '@/components/profile/EditProfile'
import Grid from '@/components/addit/Grid'
import Adm from '@/components/profile/Adm'
import Document from '@/components/docs/Document'
import EditDocument from '@/components/docs/EditDocument'
import AddDoc from '@/components/docs/AddDoc'
import NotFound from '@/components/NotFound'
import Help from '@/components/Help'
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
	base: '/app',
	routes: [
		{
			path: '/',
			// name: 'home',
			component: Home,
			children: [
				{
					path: '',
					redirect: '/documents/all',
				},
				{
					path: 'documents/:id',
					meta: { title: 'Главная, СЭД МТУСИ' },
					component: Grid,
					props: {
						columns: [
							{ key: 'reg', title: '№' },
							{ key: 'title', title: 'НАЗВАНИЕ' },
							{ key: 'full_name', title: 'ВЛАДЕЛЕЦ' },
							{ key: 'date_doc', title: 'ДАТА ДОБАВЛЕНИЯ' },
						],
					}
				},
			],
			beforeEnter: ifAuthenticated,
		},
		{
			path: '/auth',
			name: 'auth',
			meta: { title: 'Вход, СЭД МТУСИ' },
			component: Auth,
			beforeEnter: ifNotAuthenticated,
		},
		{
			path: '/help',
			name: 'help',
			meta: { title: 'Помощь, СЭД МТУСИ' },
			component: Help,
		},
		{
			path: '/addDoc',
			name: 'addDoc',
			meta: { title: 'Добавить документ, СЭД МТУСИ' },
			component: AddDoc,
			beforeEnter: ifAuthenticated,
		},
		{
			path: '/document/:id',
			name: 'document',
			meta: { title: 'Документ, СЭД МТУСИ' },
			component: Document,
			props: true,
			beforeEnter: ifAuthenticated,
		},
		{
			path: '/document/:id/edit',
			name: 'editDocument',
			meta: { title: 'Редактировать документ, СЭД МТУСИ' },
			component: EditDocument,
			props: true,
			beforeEnter: ifAuthenticated,
		},
		{
			path: '/profile',
			redirect: '/profile/notif',
			component: Profile,
			children: [
				{
					path: 'notif',
					name: 'notif',
					meta: { title: 'Уведомления, СЭД МТУСИ' },
					component: Grid,
					props: {
						id: "notif",
						columns: [
							{ key: 'initiator', title: 'ИНИЦИАТОР'},
							{key: 'title', title: 'ДОКУМЕНТ' },
							{key: 'message', title: 'СООБЩЕНИЕ'},
							{key: 'date_notif', title: 'ДАТА'},
							{key: 'file_cabinet', title: 'КАРТОТЕКА' },
						],
					}
				},
				{
					path: 'edit',
					meta: { title: 'Редактировать профиль, СЭД МТУСИ' },
					component: EditProfile
				},
				{
					path: 'adm',
					meta: { title: 'Администрирование профилей, СЭД МТУСИ' },
					component: Adm,
					beforeEnter: ifAdm,
				},
			],
			beforeEnter: ifAuthenticated,
		},
		{
			path: '/404',
			meta: { title: 'Страница не найдена, СЭД МТУСИ' },
			component: NotFound
		},
		{
			path: '*',
			redirect: '/404',
		},
	]
})

router.beforeEach((to, from, next) => {
	document.title = to.meta.title
	next()
})

export default router
