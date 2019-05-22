<template>
	<div class="mainAuth">
		<div></div>
		<div class="login">
			<div></div>
			<div>
				<div class="auth" v-if="newPassword==0" :style="{ height: boxSize }">	
					<div class="switch">
						<div></div>
						<p style="textDecoration: underline">ВХОД</p>
						<div></div>
					</div>
					<div>
						<p>EMAIL</p>
						<input
							v-validate.immediate="'required_if:!newPassword'"
							v-model="email"
							type="text"
							placeholder="Введите логин"
							class="search-box"
						/>
						<div style="height:15px;"></div>
						<p>ПАРОЛЬ</p>
						<input 
							v-validate.immediate="'required_if:!newPassword'"
							v-model="password" 
							type="password" 
							placeholder="Введите пароль"
							class="search-box"
						/>
						<div style="height:35px;"></div>
						<button type="submit" @click="doLogin()">ВОЙТИ</button> <br>
						<div @click="newPassword=1" class="rememberPassword">
							Забыли пароль?
						</div>
					</div>
				</div>
				<div class="auth" v-if="newPassword==1" :style="{ height: '360px' }">
					<div class="switch">
						<div></div>
						<p style="textDecoration: underline">СМЕНА ПАРОЛЯ - ШАГ 1</p>
						<div></div>
					</div>
					<p style="text-align: center;padding:10px;padding-top:0"> 
						Это страница смены пароля. Чтобы подтвердить свою почту, впишите ее в поле.
						Вам придет код на почту, который следует ввести на следующем шаге.
					</p>
					<p>EMAIL</p>
					<input
						v-validate.immediate="'required_if:!newPassword'"
						v-model="emailForConfirm" 
						type="email"
						placeholder="Введите email"
						class="search-box"
					/>
					<div style="height:25px;"></div>
					<div v-if="!processConfirm">
						<button type="submit" @click="newPassword=0;error=''">ВЕРНУТЬСЯ</button>
						<button type="submit" @click="rememberPassword()">ОТПРАВИТЬ</button>
					</div>
					<div v-if="processConfirm"> 
						<p>Отправляется...</p>
					</div>
				</div>
				<div class="auth" v-if="newPassword==2" :style="{ height: '500px' }">
					<div class="switch">
						<div></div>
						<p style="textDecoration: underline">СМЕНА ПАРОЛЯ - ШАГ 2</p>
						<div></div>
					</div>
					<p style="text-align: center;padding:10px;padding-top:0"> 
						Введите код подтверждения и новый пароль, а также подтвердите его.
					</p>
					<p>КОД ПОДТВЕРЖДЕНИЯ</p>
					<input
						v-validate.immediate="'required_if:!newPassword'"
						v-model="code" 
						type="email"
						placeholder="Введите email"
						class="search-box"
					/>
					<p>НОВЫЙ ПАРОЛЬ</p>
					<input
						v-validate.immediate="'required_if:!newPassword'"
						v-model="password1" 
						type="password"
						placeholder="Введите пароль"
						class="search-box"
					/>
					<p>ПОДТВЕРЖДЕНИЕ ПАРОЛЯ</p>
					<input
						v-validate.immediate="'required_if:!newPassword'"
						v-model="password2"
						type="password"
						placeholder="Подтвердите пароль"
						class="search-box"
					/>
					<div style="height:25px;"></div>
					<button type="submit" @click="newPassword=0;error=''">ВЕРНУТЬСЯ</button>
					<button type="submit" @click="updatePassword()">ПОДТВЕРДИТЬ</button>
				</div>
			</div>
			<p v-if="error" style="color:red;max-width:400px"> {{ error }} </p>
		</div>
		<div></div>
	</div>
</template>

<script>
import {AUTH_REQUEST, USER_CONFIRM_UPDATE_PASSWORD, USER_CHANGE_PASSWORD} from '../store/mutation-types'

export default {
	name: 'main',
	data () {
		return {
			email: null,
			password: null,
			emailForConfirm: null,
			processConfirm: false,
			code: null,
			password1: null,
			password2: null,
			error: null,
			loginStyle1: "underline",
			loginStyle2: "none",
			boxSize: "420px",
			newPassword: 0
		}
	},
	computed: {

	},
	methods: {
		doLogin(e) {
			const { email, password } = this;
			this.$store.dispatch(
				AUTH_REQUEST, { 
					email, 
					password 
				}
			)
			.then(() => {
				this.error = null;
				this.$router.push('/')
			})
			.catch(err => {
				if (err == '{"non_field_errors":["Unable to log in with provided credentials."]}' || err == '{"email":["Enter a valid email address."]}') {
					this.error = "Неверный логин или пароль.";
				} else {
					if(err.length > 200){
						this.error = err.substring(0,200) + "...";
					} else {
						this.error = err;
					}
					console.log(err)
				}
			})
			this.$router.push('/')
		},
		rememberPassword(){
			const { emailForConfirm } = this;
			this.processConfirm = true;
			this.$store.dispatch(
				USER_CONFIRM_UPDATE_PASSWORD, emailForConfirm
			)
			.then((resp) => {
				this.error = null;
				this.processConfirm = false;
				this.newPassword = 2;
			})
			.catch(err => {
				this.processConfirm = false;
				if(err.length > 200){
					if(err.substring(0,39) == "NameError at /rest_auth/password/reset/"){
						this.error = "Такой email не зарегестрирован в системе.";
					} else {
						this.error = err.substring(0,200) + "...";
					}
				} else {
					this.error = err;
				}
			})	
		},
		updatePassword(){
			const { code, password1, password2 } = this;
			if(password1 != password2) {
				this.error = "Пароли не совпадают.";
				return;
			}
			this.error = "Круто клево";
			this.processConfirm = true;
			this.$store.dispatch(
				USER_CHANGE_PASSWORD, {
					uid: code.split('/')[0],
					token: code.split('/')[1],
					password1: password1,
					password2: password2,
				}
			)
			.then((resp) => {
				this.error = null;
				this.processConfirm = false;
				this.newPassword = 0;
			})
			.catch(err => {
				console.log(err)
				if(err=='{"uid":["Invalid value"]}' || err=='{"token":["Invalid value"]}'){
					this.err = "Неверный код."
				} else if(err=='{"new_password2":["This password is too short. It must contain at least 8 characters.","This password is too common.","This password is entirely numeric."]}'){
					this.err = "Слишком короткий пароль."
				} else {
					if(err.length > 200){
						this.error = err.substring(0,200) + "...";
					} else {
						this.error = err;
					}
				}
			})
		}
	}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* Основной экран */
.mainAuth{
	margin: 0 auto;
	height: 100vh;
	display: grid;
    grid-template-columns: auto max-content auto;
}
.mainAuth .login{
	display: grid;
	grid-template-rows: 1fr max-content 2fr;
}
.mainAuth > *{
	text-align: center;
}
.mainAuth .auth{
	width: 400px;
	background: #ADE0FC;
}
/* Кнопки переключения вход и регистрация */
.mainAuth .switch{
	font-size: 26px;
	padding-top: 8px;
	padding-bottom: 8px;
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
/**/
.rememberPassword{
	padding-top: 30px;
	color: #347090;
	font-size: 14px;
}
.rememberPassword:hover{
	cursor: pointer;
}
</style>
