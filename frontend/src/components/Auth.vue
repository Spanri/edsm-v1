<template>
<div class="main">
	<div class="callback">Callback</div>
	<button type="submit" @click="logout()">Logout</button>
</div>
</template>

<script>
import {AUTH_LOGOUT} from '../store/mutation-types'

export default {
	name: 'auth',
	methods: {
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
.main{
    height: 100%;
	width: 100%;
	background: white;
}
</style>
