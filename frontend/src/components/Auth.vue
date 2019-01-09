<template>
	<div class="main">
		<form class="login" @submit.prevent="login">
			<h1>Вход</h1>
			<label>Логин</label>
			<input 
				required
				v-model="username" 
				type="text" 
				placeholder="Введите логин"
				class="search-box"
			/> <br>
			<label>Пароль</label>
			<input 
				required 
				v-model="password" 
				type="password" 
				placeholder="Введите пароль"
				class="search-box"
			/> <br>
			<button type="submit">Войти</button>
		</form>
		<hr>
		<form class="signup" @submit.prevent="signup">
			<h1>Регистрация</h1>
			<label>Придумайте логин</label>
			<input 
				required
				v-model="usernameNew" 
				type="text" 
				placeholder="Введите логин"
				class="search-box"
			/> <br>
			<label>Придумайте пароль</label>
			<input 
				required 
				v-model="passwordNew" 
				type="password" 
				placeholder="Введите пароль"
				class="search-box"
			/> <br>
			<label>Повторите пароль</label>
			<input 
				required 
				v-model="password2New" 
				type="password" 
				placeholder="Повторите пароль"
				class="search-box"
			/> <br>
			<button type="submit">Зарегистрироваться</button>
			<p>{{error}}</p>
		</form>
	</div>
</template>

<script>
import {AUTH_REQUEST} from '../store/mutation-types'

export default {
	name: 'main',
	data () {
		return {
			error: ''
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
		signup() {
			const { usernameNew, passwordNew, password2New } = this;
			var checkUsernameValid = /[a-zA-Z0-9]+$/i;
			if (!checkUsernameValid.test(usernameNew)) {
				this.error = "Логин должен быть 6 и больше символов и состоять из английских букв";
			} else if (!checkUsername(usernameNew)) {
				this.error = "Такой пользователь уже зарегестрирован.";
			} else if (passwordNew != password2New) {
				this.error = "Пароли не совпадают.";
			} else {
				this.$store.dispatch(AUTH_REQUEST, { username, password })
				.then(() => {
					this.$router.push('/');
				});
			}
		},
		checkUsername(user) {
			// Проверяет, есть ли уже такой юзер.
			// Если да, false, иначе true
		}
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
.main > *{
	text-align: center;
}
.login > *, .signup > * {
	margin: 5px;
}
.search-box{
    background:#a8c1d8;
    border: 0;
    color: #3e5468;
    font-size: 15px;
}
</style>
