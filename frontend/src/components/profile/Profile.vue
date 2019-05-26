<template>
	<div class="profile">
		<headerProfile></headerProfile>
		<div class="mainProfile">
			<div>
				<div class="menuProfile">
					<div style="margin-top:10px"></div>
					<router-link class="router-link" :to="{ path: '/profile/notif', }">УВЕДОМЛЕНИЯ</router-link>
					<router-link class="router-link" :to="{ path: '/profile/edit', }">РЕДАКТИРОВАНИЕ ПРОФИЛЯ</router-link>
					<router-link v-if="getProfile.is_staff" class="router-link" :to="{ path: '/profile/adm', }">АДМИНИСТРИРОВАНИЕ ПРОФИЛЕЙ</router-link>
					<div style="height:15px;"></div>
					<p class="router-link" @click="logout()">ВЫЙТИ</p>
				</div>
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
            page: '',
		}
	},
	created(){
		this.page = this.$store.getters.getPageProfile;
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

<style>
.profile{
    height: 100%;
	background: white;
}
.profile > *{
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
	font-family: 'El Messiri', sans-serif;
	font-weight: 300;
	border: #e0e0e0 3px solid;
	border-radius: 5px;
}
.menuProfile .router-link{
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
.menuProfile p:hover{
	cursor: pointer;
	color: #7cb0c1;
}
/**/
.menuProfile .router-link-exact-active{
	background: rgb(223, 243, 253);
}
</style>