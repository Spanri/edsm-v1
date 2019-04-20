<template>
    <div class="headerProfileGradient">
        <div class="headerProfile">
            <img class="avatar">
            <div v-if="profile.name">
                <p style="font-size:24px;">{{profile.name}}</p>
                <p>{{profile.position}}</p>
            </div>
        </div>
    </div>
</template>

<script>
import {AUTH_LOGOUT} from '../store/mutation-types'

export default {
	name: 'account',
	computed: {
		profile: function(){
			return this.$store.getters.getProfile
		}
	},
	methods: {
		myDocs() {
			this.$router.push('/profile/')
		},
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
.headerProfileGradient{
	background: radial-gradient(1448.86px at 0% 100%, #ADE0FC 0%, #93ADDF 53.65%, #DFB8FE 100%);
}
.headerProfile{
    max-width: 900px;
	margin: auto;
	color: white;
	font-size: 18px;
	font-family: serif;
	display: grid;
	grid-template-columns: max-content auto;
}
.avatar{
	margin: 10px 60px;
	margin-left: 0;
    width: 100px;
    height: 100px;
	background-color: white;
    border-radius: 50%;
}
</style>