<template>
	<div class="main">
		<form class="login" @submit.prevent="login">
			<h1>Sign in</h1>
			<label>User name</label>
			<input required v-model="username" type="text" placeholder="Snoopy"/>
			<label>Password</label>
			<input required v-model="password" type="password" placeholder="Password"/>
			<hr/>
			<button type="submit">Login</button>
		</form>
	</div>
</template>

<script>
import {AUTH_REQUEST} from '../store/mutation-types'

export default {
	name: 'main',
	data () {
		return {

		}
	},
	computed: {

	},
	methods: {
		login() {
			const { username, password } = this;
			this.$store.dispatch(AUTH_REQUEST, { username, password })
			.then(() => {
				this.$router.push('/');
			});
		},
	}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.main{
    height: 100%;
	width: 100%;
	background: white;
}
h1{
  	font-weight: normal;
	margin: 20px;
}
</style>
