<template>
	<div id="mainAuth">
		<div></div>
		<div class="login">
			<div></div>
			<div>
				<div class="auth" v-if="rememberPassword == false">
					<p class="title">ВХОД</p>
					<div>
						<p>EMAIL</p>
						<input
							v-validate.immediate="'required_if:!newPassword'"
							name="email"
							v-model="email"
							type="text"
							placeholder="Введите логин"
							class="search-box"
							style="width:200px"
						/>
						<div style="height:15px;"></div>
						<p>ПАРОЛЬ</p>
            <div style="background: white;margin: 0 auto; width: 230px;">
              <input
                v-validate.immediate="'required_if:!newPassword'"
                name="password"
                v-model="password"
                :type="passwordFieldType"
                placeholder="Введите пароль"
                class="search-box"
                style="width:166px"
              />
              <button class="showPassword" type="password" @click="switchVisibility()">
                <svg
                  width="16px"
                  stroke="black"
                  enable-background="new 0 0 10 12"
                  id="Editable-line"
                  viewBox="0 0 30 30">
                  <path
                    d="  M16,7C9.934,7,4.798,10.776,3,16c1.798,5.224,6.934,9,13,9s11.202-3.776,13-9C27.202,10.776,22.066,7,16,7z"
                    fill="none"
                    id="XMLID_13_"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-miterlimit="10"
                    stroke-width="2"/>
                  <circle cx="16" cy="16" fill="none" id="XMLID_14_" r="5" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="2"/>
                  <line v-if="passwordFieldType == 'password'" fill="none" id="XMLID_15_" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="2" x1="3" x2="29" y1="3" y2="29"/>
                </svg>
              </button>
            </div>
						<div style="height:35px;"></div>
						<button type="submit" @click="doLogin()">ВОЙТИ</button> <br>
						<div @click="rememberPassword=true" class="rememberPassword">
							Забыли пароль?
						</div>
					</div>
				</div>
				<RememberPassword class="auth" v-if="rememberPassword == true"></RememberPassword>
			</div>
			<p v-if="error" style="color:red;max-width:400px"> {{ error }} </p>
		</div>
	</div>
</template>

<script>
import {
	AUTH_REQUEST,
	ADDIT_REMEMBER_PASSWORD,
	ADDIT_ERROR_AUTH
} from '../store/mutation-types'
import RememberPassword from './addit/RememberPassword';

export default {
	name: 'auth',
	components: { RememberPassword },
	data () {
		return {
			email: null, // почта для авторизации
			password: null, // пароль для авторизации
			passwordFieldType: 'password', // для показывания пароля в виде текста
		}
	},
	created() {
		this.rememberPassword = false;
		this.error = '';
	},
	computed: {
		// для смены пароля
		rememberPassword:{
			get(){
				return this.$store.getters.getRememberPassword;
			},
			set(newValue){
				return this.$store.commit(ADDIT_REMEMBER_PASSWORD, newValue);
			}
		},
		// для ошибок
		error:{
			get(){
				return this.$store.getters.getErrorAuth;
			},
			set(newValue){
				return this.$store.commit(ADDIT_ERROR_AUTH, newValue);
			}
		}
	},
	methods: {
		// для показывания пароля в виде текста
		switchVisibility() {
			this.passwordFieldType = this.passwordFieldType === 'password' ? 'text' : 'password'
		},
		// авторизация
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
		},

	}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* Основной экран */
#mainAuth{
	margin: 0 auto;
	height: 100vh;
	display: grid;
    grid-template-columns: auto max-content auto;
}
#mainAuth > *{
	text-align: center;
}
/* Чтобы посередине окно было */
.login{
	display: grid;
	grid-template-rows: 1fr max-content 2fr;
}
/* Заголовок */
.title{
	font-size: 26px;
	padding-top: 30px;
	padding-bottom: 8px;
}
/* Параметры окна */
.auth{
	width: 400px;
	background: #ADE0FC;
}
/* Кнопка ВОЙТИ, переопределение */
button{
    margin-top: 0;
    margin-bottom: 0;
}
/* Кнопка "Забыли пароль?"*/
.rememberPassword{
	padding-top: 30px;
	padding-bottom: 30px;
	color: #347090;
	font-size: 14px;
}
.rememberPassword:hover{
	cursor: pointer;
}
.showPassword {
  padding: 8px 12px 6px 0;
  margin: 0;
  background: 0;
  border: 0;
}
</style>
