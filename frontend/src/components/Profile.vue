<template>
	<div class="account">
		<div class="account2">
			<h2 v-if="profile.name">
				ОПА {{profile.name}}
			</h2>
			<p>ОПА2 {{profile.name}}</p>
			<p>Это аккаунт.</p>
		</div>
	</div>
</template>

<script>
// import { mapState } from 'vuex'

export default {
	name: 'account',
	computed: {
		// mapState({profile: state => state.user.profile}),
		profile: function(){
			return this.$store.getters.getProfile
		}
	}
}
</script>

<style>
.account{
    height: 100%;
	width: 100%;
	background: white;
}
.account > *{
	padding: 25px;
}
.account2{
	max-width: 900px;
	margin: auto;
}
</style>