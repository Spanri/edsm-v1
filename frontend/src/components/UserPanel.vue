<template>
	<div>
		<div class="headline">
		<h1>Your doge profile</h1>
		</div>
		<p v-if="profile.name">
		<strong>Name:</strong> {{profile.title}} {{profile.name}}
		</p>
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
.headline{
	margin-top: 1em;
	display: flex;
}
</style>