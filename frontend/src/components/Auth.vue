<template>
	<div class="mainAuth">
		<div></div>
		<div class="auth" :style="{ height: boxSize }">
			<div class="switch">
				<div></div>
				<p 
					@click="login=true;loginStyle1='underline';loginStyle2='none';boxSize='360px'"
					:style="{ textDecoration: loginStyle1 }"
					>ВХОД
				</p>
				<p
					@click="login=false;loginStyle2='underline';loginStyle1='none';boxSize='480px'"
					:style="{ textDecoration: loginStyle2 }"
					>РЕГИСТРАЦИЯ
				</p>
				<div></div>
			</div>
			<form class="login" @submit.prevent="loginMethod" v-if="login">
				<p>ЛОГИН</p>
				<input
					required
					v-model="username" 
					type="text"
					placeholder="Введите логин"
					class="search-box"
				/>
				<div style="height:15px;"></div>
				<p>ПАРОЛЬ</p>
				<input 
					required 
					v-model="password" 
					type="password" 
					placeholder="Введите пароль"
					class="search-box"
				/>
				<div style="height:35px;"></div>
				<button type="submit">ВОЙТИ</button>
				<p>{{error}}</p>
			</form>
			<form class="signup" @submit.prevent="signupMethod" v-if="!login">
				<p>ЛОГИН</p>
				<input 
					required
					v-model="usernameNew" 
					type="text" 
					placeholder="Введите логин"
					class="search-box"
				/>
				<div style="height:15px;"></div>
				<p>ПАРОЛЬ</p>
				<input 
					required 
					v-model="passwordNew" 
					type="password" 
					placeholder="Введите пароль"
					class="search-box"
				/>
				<div style="height:15px;"></div>
				<p>ПОВТОРИТЕ ПАРОЛЬ</p>
				<input 
					required 
					v-model="password2New" 
					type="password" 
					placeholder="Повторите пароль"
					class="search-box"
				/>
				<div style="height:40px;"></div>
				<button type="submit">ЗАРЕГИСТРИРОВАТЬСЯ</button>
				<p>{{error}}</p>
			</form>
		</div>
		<div></div>
	</div>
</template>

<script>
import {AUTH_REQUEST} from '../store/mutation-types'

export default {
	name: 'main',
	data () {
		return {
			login: true,
			loginStyle1: "underline",
			loginStyle2: "none",
			boxSize: "350px",
			error: ''
		}
	},
	computed: {

	},
	methods: {
		loginMethod() {
			const { username, password } = this;
			this.$store.dispatch(AUTH_REQUEST, { username, password })
			.then(() => {
				console.log('sdfgsdfg')
				this.$router.push('/')
			})
			this.$router.push('/')
		},
		signupMethod() {
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
/* Основной экран */
.mainAuth{
	width: 400px;
	margin: 0 auto;
	height: 100vh;
	display: grid;
    grid-template-rows: auto max-content auto;
}
.mainAuth > *{
	text-align: center;
}
.auth{
	height: 400px;
	background: #ADE0FC;
}
/* Кнопки переключения вход и регистрация */
.switch{
	font-size: 18px;
	margin-top: 20px;
	margin-bottom: 20px;
	display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
}
.switch p:hover{
	cursor: pointer;
}
/* Кнопки ВОЙТИ и ЗАРЕГЕСТРИРОВАТЬСЯ */
button{
	border: 0;
	border-radius: 5px;
	padding: 8px;
	color: white;
	background-color: #347090;
}
button:hover{
	cursor: pointer;
}
/* Поля ввода */
input{
	border: 0;
	height: 30px;
	margin: 0 auto;
	padding-left: 15px;
	padding-right: 15px;
}
</style>
