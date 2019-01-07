<template>
  	<div class="callback">Callback</div>
</template>

<script>
export default {
	name: 'auth',
	props: ['auth'],
	created () {
		this.auth.handleAuthentication()
	}
}
</script>
