<template>
	<div class="account">
		<div class="account2">
			<p>Не найдено.</p>
		</div>
	</div>
</template>

<script>
import { mapState } from 'vuex'

export default {
    name: 'account',
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