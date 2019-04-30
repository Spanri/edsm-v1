<template>
	<div class="profile">
		<headerProfile></headerProfile>
		<div class="mainProfile">
			<div>
				<div class="menuProfile">
					<p @click="notif()">УВЕДОМЛЕНИЯ</p>
					<p @click="edit()">РЕДАКТИРОВАНИЕ ПРОФИЛЯ</p>
					<p v-if="profile.adm" @click="adm()">АДМИНИСТРИРОВАНИЕ ПРОФИЛЕЙ</p>
					<p @click="logout()">ВЫЙТИ</p>
				</div>
			</div>
			<router-view></router-view>
		</div>
	</div>
</template>

<script>
import {AUTH_LOGOUT} from '../store/mutation-types'
import HeaderProfile from '../components/HeaderProfile';

export default {
	name: 'account',
	components: { HeaderProfile },
	computed: {
		profile: function(){
			return this.$store.getters.getProfile
		}
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
	border: #e0e0e0 3px solid;
	border-radius: 5px;
}
.menuProfile *{
	padding: 3px 30px;
}
.menuProfile *:hover{
	cursor: pointer;
	color: #7cb0c1;
}
</style>