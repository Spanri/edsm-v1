<template>
	<div class="mainAuth">
		<div></div>
		<div class="auth" :style="{ height: boxSize }">
			<div class="switch">
				<div></div>
				<p 
					@click="login=true;loginStyle1='underline';loginStyle2='none';boxSize='400px'"
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
			<form
					class="login"
					@submit.prevent="loginMethod();"
					v-if="login">
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
				<button type="submit">ВОЙТИ</button> <br>
				<p style="padding:10px">
					<a href="" style="color:#347090;font-size:14px;padding:10px">Забыли пароль?</a>
				</p>
			</form>
			<form 
					class="signup"
					ref="signup"
					v-if="!login">
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
				<button type="button" @click="signupMethod" id="signup">ЗАРЕГИСТРИРОВАТЬСЯ</button>
			</form>
		</div>
		<p v-if="error"> {{ error }} </p>
		<div></div>
	</div>
</template>

<script>
import {AUTH_REQUEST} from '../store/mutation-types'

export default {
	name: 'main',
	data () {
		return {
			username: null,
			password: null,
			usernameNew: null,
			passwordNew: null,
			password2New: null,
			login: true,
			error: null,
			loginStyle1: "underline",
			loginStyle2: "none",
			boxSize: "400px",
		}
	},
	computed: {

	},
	methods: {
		loginMethod() {
			const { username, password } = this;
			this.$store.dispatch(AUTH_REQUEST, { username, password })
			.then(() => {
				this.error = null;
				e.preventDefault();
				console.log('signin')
				this.$router.push('/')
			})
			this.$router.push('/')
		},
		signupMethod(e) {
			const { usernameNew, passwordNew, password2New } = this;
			var checkValid = /[a-zA-Z0-9]{6,}/i;
			if (!checkValid.test(usernameNew)) {
				this.error = "Логин должен быть 6 и больше символов и состоять из английских букв";
			} else if (!this.checkUsername(usernameNew)) {
				this.error = "Такой пользователь уже зарегистрирован.";
			} else if (!checkValid.test(passwordNew)) {
				this.error = "Пароль должен быть 6 и больше символов и состоять из английских букв";
			} else if (passwordNew != password2New) {
				this.error = "Пароли не совпадают.";
			} else {
				this.error = null;
				console.log('signup');
				const elem = this.$refs.signup;
				elem.submit();
				this.$store.dispatch(AUTH_REQUEST, { username: "username", password: "password" })
				.then(() => {
					this.$router.push('/');
				});
			}
			
		},
		go() {
			this.$router.push('/');
		},
		checkUsername(user) {
			// Проверяет, есть ли уже такой юзер.
			// Если да, false, иначе true
			return true;
		},
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
.mainAuth .auth{
	height: 400px;
	background: #ADE0FC;
}
/* Кнопки переключения вход и регистрация */
.mainAuth .switch{
	font-size: 18px;
	margin-top: 20px;
	margin-bottom: 20px;
	display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
}
.mainAuth .switch p:hover{
	cursor: pointer;
}
/* Кнопки ВОЙТИ и ЗАРЕГЕСТРИРОВАТЬСЯ */
.mainAuth button{
	border: 0;
	border-radius: 5px;
	padding: 8px;
	color: white;
	background-color: #347090;
}
.mainAuth button:hover{
	cursor: pointer;
}
/* Поля ввода */
.mainAuth input{
	border: 0;
	height: 30px;
	margin: 0 auto;
	padding-left: 15px;
	padding-right: 15px;
}
</style>
