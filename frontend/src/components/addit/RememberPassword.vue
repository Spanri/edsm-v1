<template>
    <div id="rememberPassword">
        <div v-if="newPassword==1">
            <p class="title">СМЕНА ПАРОЛЯ - ШАГ 1</p>
            <p class="text" style="">
                Это страница смены пароля. Чтобы подтвердить свою почту, впишите ее в поле.
                Вам придет код на почту, который следует ввести на следующем шаге.
            </p>
            <p>EMAIL</p>
            <input
                v-validate.immediate="'required_if:!newPassword'"
                name="email2"
                v-model="emailForConfirm"
                type="email"
                placeholder="Введите email"
                class="search-box"
            />
            <div style="height:25px;"></div>
            <div v-if="!processConfirm">
                <button type="submit" @click="rememberP=false;error=''">ВЕРНУТЬСЯ</button>
                <button type="submit" @click="rememberPassword()" style="margin-left:5px;">ОТПРАВИТЬ</button>
            </div>
            <div v-if="processConfirm">
                <p style="padding: 20px;">Отправляется...</p>
            </div>
        </div>
        <div v-if="newPassword==2">
            <p class="title">СМЕНА ПАРОЛЯ - ШАГ 2</p>
            <p class="text">
                Введите код подтверждения и новый пароль. Подтвердите пароль.
            </p>
            <p>КОД ПОДТВЕРЖДЕНИЯ</p>
            <input
                v-validate.immediate="'required_if:!newPassword'"
                name="code"
                v-model="code"
                type="email"
                placeholder="Введите email"
                class="search-box"
            />
            <p>НОВЫЙ ПАРОЛЬ</p>
            <input
                v-validate.immediate="'required_if:!newPassword'"
                name="password1"
                v-model="password1"
                type="password"
                placeholder="Введите пароль"
                class="search-box"
            />
            <p>ПОДТВЕРЖДЕНИЕ ПАРОЛЯ</p>
            <input
                v-validate.immediate="'required_if:!newPassword'"
                name="password2"
                v-model="password2"
                type="password"
                placeholder="Подтвердите пароль"
                class="search-box"
            />
            <div style="height:25px;"></div>
            <button type="submit" @click="rememberP=false;error=''">ВЕРНУТЬСЯ</button>
            <button type="submit" @click="updatePassword()" style="margin-left:5px;">ПОДТВЕРДИТЬ</button>
        </div>
    </div>
</template>

<script>
import {
	USER_CONFIRM_UPDATE_PASSWORD,
    USER_CHANGE_PASSWORD,
    ADDIT_REMEMBER_PASSWORD,
    ADDIT_ERROR_AUTH,
} from '../../store/mutation-types'

export default {
    name: 'rememberPassword',
    props: {
        typeFile: { type: String, default: ""},
    },
    data () {
		return {
			emailForConfirm: null, // для шага 1, подтверждение почты
			processConfirm: false, // для показа процесса обработки
			code: null, // поле для кода подтверждения
			password1: null, // поле для нового пароля
			password2: null, // поле для подтверждения нового пароля
			newPassword: 1, // для смены пароля
		}
    },
    computed: {
		// для возвращения на страницу авторизации
		rememberP:{
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
        // шаг 1, проверка почты и отправление на нее письма
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
        // шаг 2, смена пароля
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
				this.rememberP = false;
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

<style scoped>
/* Заголовки */
.title{
	font-size: 26px;
	padding-top: 30px;
	padding-bottom: 22px;
    margin: 0;
}
.text{
    text-align: center;
    padding: 15px;
    padding-top: 0;
    padding-bottom: 5px;
    margin: 0;
}
button{
    margin-top: 5px;
    margin-bottom: 25px;
}
</style>
