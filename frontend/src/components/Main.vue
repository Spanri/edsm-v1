<template>
<div class="main">
	<!-- <div class="gradient r">
		<div class="close-button" v-bind:style="{ gridTemplateColumns: closeButtonSize }">
			<p 
				class="close" 
				@click="closeMenu()"
				>{{ textClose }}
			</p>
			<p 
				class="name" 
				v-bind:style="{ marginLeft: marginLeft + 'px' }"
				>ГЛАВНАЯ
			</p>
		</div>
		<div class="main-space" v-bind:style="{ gridTemplateColumns: menuSize }">
			<Menu v-if="closeM == false"></Menu>
			
		</div> 
	</div> -->
	<!-- <h2>User {{ this.$route.params.id }}</h2> -->
	<p>Current route name: {{ this.$route.name }}</p>
	<button type="submit" @click="logout()">Logout</button>
	<router-view></router-view>
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
.r{
	width: 100%;
	max-width: 1400px;
	margin: auto;
	margin-top: 0;
	margin-bottom: 0;
}
.main-space{
	height: 100%;
	width: 100%;
	display: grid;
}
.close{
    text-align: center;
    height: 30px;
    margin: 20px;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 15px;
    color: rgb(75, 54, 54);
}
.close:hover{
	cursor: pointer;
}
.close-button{
	display: grid;
}
.name{
    height: 30px;
    margin: 20px;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 25px;
    color: white;
}
</style>
