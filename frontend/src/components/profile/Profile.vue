<template>
	<div id="profile">
		<div class="mainProfile">
			<div v-if="closeMenu" style="background:#ADE0FC;height:300px" @click="closeMenu = false" class="openCloseMenuButton">
				<svg class="openCloseMenuButton" fill="#347090" enable-background="new 0 0 96 96" height="26px" viewBox="0 0 96 96" width="26px" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
					<path d="M12,52h62.344L52.888,73.456c-1.562,1.562-1.562,4.095-0.001,5.656c1.562,1.562,4.096,1.562,5.658,0l28.283-28.284l0,0  c0.186-0.186,0.352-0.391,0.498-0.609c0.067-0.101,0.114-0.21,0.172-0.315c0.066-0.124,0.142-0.242,0.195-0.373  c0.057-0.135,0.089-0.275,0.129-0.415c0.033-0.111,0.076-0.217,0.099-0.331C87.973,48.525,88,48.263,88,48l0,0  c0-0.003-0.001-0.006-0.001-0.009c-0.001-0.259-0.027-0.519-0.078-0.774c-0.024-0.12-0.069-0.231-0.104-0.349  c-0.039-0.133-0.069-0.268-0.123-0.397c-0.058-0.139-0.136-0.265-0.208-0.396c-0.054-0.098-0.097-0.198-0.159-0.292  c-0.146-0.221-0.314-0.427-0.501-0.614L58.544,16.888c-1.562-1.562-4.095-1.562-5.657-0.001c-1.562,1.562-1.562,4.095,0,5.658  L74.343,44L12,44c-2.209,0-4,1.791-4,4C8,50.209,9.791,52,12,52z"/>
				</svg>
			</div>
			<div v-if="!closeMenu">
				<headerProfile></headerProfile>
				<div class="menuProfile">
					<div style="margin-top:10px"></div>
					<router-link class="router-link" :to="{ path: '/profile/notif', }">УВЕДОМЛЕНИЯ</router-link>
					<router-link class="router-link" :to="{ path: '/profile/edit', }">РЕДАКТИРОВАНИЕ ПРОФИЛЯ</router-link>
					<router-link v-if="getProfile.is_staff" class="router-link" :to="{ path: '/profile/adm', }">АДМИНИСТРИРОВАНИЕ</router-link>
					<div style="height:15px;"></div>
					<p class="router-link" @click="logout()">ВЫЙТИ</p>
				</div>
				<p @click="closeMenu = true" class="openCloseMenuButton" style="margin-top:10px">Скрыть меню</p>
			</div>
			<router-view></router-view>
		</div>
	</div>
</template>

<script>
import {AUTH_LOGOUT} from '../../store/mutation-types'
import HeaderProfile from './HeaderProfile';
import { mapGetters } from 'vuex'

export default {
	name: 'profile',
	components: { HeaderProfile },
	data () {
		return {
			closeMenu: false,
		}
	},
	computed: {
		...mapGetters({
			getProfile: 'getProfile'
		})
  	},
	methods: {
		notif() {
			this.$router.push('/profile/notif')
		},
		edit() {
			this.$router.push('/profile/edit')
		},
		adm() {
			this.$router.push('/profile/adm')
		},
		logout() {
			this.$store.dispatch(AUTH_LOGOUT)
			.then(() => {
				this.$router.push('/auth')
			});
		}
	}
}
</script>

<style scoped>
#profile{
    height: 100%;
	background: white;
}
#profile > *{
	padding: 25px 50px;
}
.mainProfile{
	max-width: 1440px;
	margin: auto;
	display: grid;
	grid-template-columns: max-content auto;
}
/**/
.menuProfile{
	font-family: 'PT+Sans+Narrow', sans-serif;
	font-weight: 300;
	border: #e0e0e0 3px solid;
	border-radius: 5px;
}
.router-link{
	padding: 10px 20px;
	margin-top: 5px;
	margin-bottom: 5px;
	text-decoration: none;
	color: black;
	width: calc(100% - 40px);
	margin-left: 0;
	margin-right: 0;
	display: block;
}
.router-link:hover{
	cursor: pointer;
	color: #7cb0c1;
}
/**/
.router-link-exact-active{
	background: rgb(223, 243, 253);
}
/**/
.openCloseMenuButton{
    margin: 5px;
}
.openCloseMenuButton:hover, .openCloseMenuButton:hover *{
    cursor: pointer;
	color: #7cb0c1;
	fill: #7cb0c1;
}
@media (max-width: 500px) {
	.mainProfile{
		grid-template-columns: auto;
		grid-template-rows: min-content auto;
		padding: 0;
	}
}
</style>