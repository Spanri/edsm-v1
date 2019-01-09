<template>
	<div class="account">
		<div class="account2">
			<h2 v-if="profile.name">
				{{profile.title}} {{profile.name}}
			</h2>
			<p>Это аккаунт.</p>
		</div>
	</div>
</template>

<script>
import { mapState } from 'vuex'

export default {
    name: 'account',
    computed: mapState({profile: state => state.user.profile})
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