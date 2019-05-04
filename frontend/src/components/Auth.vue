<template>
	<div class="mainAuth">
		<div></div>
		<div class="auth" :style="{ height: boxSize }">
			<div class="switch">
				<div></div>
				<p style="textDecoration: underline">ВХОД</p>
				<div></div>
			</div>
			<form
					class="login"
					@submit.prevent="loginMethod();"
					v-if="login">
				<p>EMAIL</p>
				<input
					required
					v-model="email" 
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
		</div>
		<p v-if="error" style="color:red"> {{ error }} </p>
		<div></div>
	</div>
</template>

<script>
import {AUTH_REQUEST, AUTH_SIGNUP} from '../store/mutation-types'

export default {
	name: 'main',
	data () {
		return {
			email: null,
			password: null,
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
		loginMethod(e) {
			const { email, password } = this;
			this.$store.dispatch(
				AUTH_REQUEST, { 
					email, 
					password 
				}
			)
			.then(() => {
				this.error = null;
				// e.preventDefault();
				console.log('signin')
				this.$router.push('/')
				console.log('signin2')
			})
			.catch(err => {
				this.error = "Неправильный Email или Пароль.";
			})
			this.$router.push('/')
		},
		signupMethod(e) {
			const { emailNew, passwordNew, password2New } = this;
			var checkValid = /[a-zA-Z0-9]{6,}/i;
			if (!checkValid.test(emailNew)) {
				this.error = "Логин должен быть 6 и больше символов и состоять из английских букв";
			} else if (!this.checkUsername(emailNew)) {
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
				this.$store.dispatch(
					AUTH_SIGNUP, { 
						email: emailNew, 
						password: passwordNew
					}
				)
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
	font-size: 26px;
	margin-top: 20px;
	margin-bottom: 20px;
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
