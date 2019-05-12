<template>
	<div class="profile">
		<headerProfile></headerProfile>
		<div class="mainProfile">
			<div>
				<div class="menuProfile">
					<p :class="{active: page==1 ? true : false}" @click="page=1;notif()">УВЕДОМЛЕНИЯ</p>
					<p :class="{active: page==2 ? true : false}" @click="page=2;edit()">РЕДАКТИРОВАНИЕ ПРОФИЛЯ</p>
					<p v-if="getProfile.is_staff" :class="{active: page==3 ? true : false}" @click="page=3;adm()">АДМИНИСТРИРОВАНИЕ ПРОФИЛЕЙ</p>
					<p @click="logout()">ВЫЙТИ</p>
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
            page: 1,
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
/**/
.menuProfile .active{
	text-decoration-line: underline;
}
</style>