<template>
	<div class="editProfile">
		<h3 class="header">РЕДАКТИРОВАНИЕ ПРОФИЛЯ</h3>
        <div class="editProfile2Colon">
            <div>
                <img :src="image || 'https://img.icons8.com/wired/512/000000/document.png'">
            </div>
            <div style="margin-left:25px">
                <p v-if="error" style="color: red">{{error}}</p>
                <p>Выбрать новый аватар</p>
                <input type="file" id="file" class="inputfile" name="file" @change="onFileChange">
                <p>{{upload}}</p>
                <form @submit.prevent="editProfile">
                    <p>Email</p>
                    <input
                        v-model="email"
                        type="email"
                        placeholder="Введите имя"
                        class="search-box"
                    />
                    <p>Пароль</p>
                    <input
                        v-model="password"
                        type="password" 
                        placeholder="Введите имя"
                        class="search-box"
                        autocomplete="false"
                    />
                    <div v-if="password">
                        <p>Повторите пароль</p>
                        <input
                            v-model="password2"
                            type="password" 
                            placeholder="Введите имя"
                            class="search-box"
                        />
                    </div>
                    <p>Имя</p>
                    <input
                        v-model="first_name"
                        type="text" 
                        placeholder="Введите имя"
                        class="search-box"
                    />
                    <p>Фамилия</p>
                    <input
                        v-model="second_name"
                        type="text" 
                        placeholder="Введите фамилию"
                        class="search-box"
                    />
                    <p>Отчество</p>
                    <input
                        v-model="patronymic"
                        type="text" 
                        placeholder="Введите отчество"
                        class="search-box"
                    />
                    <p>Должность</p>
                    <input
                        v-model="position"
                        type="text" 
                        placeholder="Введите отчество"
                        class="search-box"
                    />
                    <div style="height:35px;"></div>
                    <button type="submit" @click="editProfile">РЕДАКТИРОВАТЬ</button> <br>
                </form>
            </div>
        </div>
	</div>
</template>

<script>
import { mapState } from 'vuex'
import axios from 'axios'
import { USER_UPDATE } from '../../store/mutation-types';

export default {
    name: 'account',
    data () {
		return {
            email: this.$store.getters.getProfile.email,
            password: '',
            password2: '',
            first_name: this.$store.getters.getProfile.profile.first_name,
            second_name: this.$store.getters.getProfile.profile.second_name,
            patronymic: this.$store.getters.getProfile.profile.patronymic,
            position: this.$store.getters.getProfile.profile.position,
            image: this.$store.getters.getProfile.profile.image,
            error: '',
            upload: '',
		}
    },
    methods: {
        onFileChange(e) {
            this.upload = "Загружается..."
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length) return;
            this.file = files[0];
            //console.log(this.file);
            this.upload = "";
        },
        editProfile(){
            if(this.password && this.password != this.password2) {
                this.error = 'Пароли не совпадают.'
                return;
            } else {
                this.error = '';
            }
            this.$store.dispatch(USER_UPDATE, {
                email: this.email,
                password: this.password,
                first_name: this.first_name,
                second_name: this.second_name,
                patronymic: this.patronymic,
                position: this.position,
            })
            .then(resp => {
                this.error = 'Данные профиля изменены.';
                this.email = resp.email;
                this.password = resp.password;
                this.first_name = resp.first_name;
                this.second_name = resp.second_name;
                this.patronymic = resp.patronymic;
                this.position = resp.position;
                this.password2 = ''; 
            })
            .catch(err=>{
                this.error = 'Ошибка. Что-то пошло не так.'
            })
        },
    }
}
</script>

<style>
.editProfile{
    height: 100%;
	width: 100%;
    max-width: 900px;
    margin: 0 auto;
	background: white;
    padding: 25px;
}
.editProfile .header{
    margin-top: 0;
	margin-bottom: 30px;
}
/* Поля ввода */
.editProfile textarea, .editProfile [type]:not([type="submit"]):not([type="file"]){
	border: 0;
	margin: 0 auto;
    height: 30px;
    padding-left: 15px;
	padding-right: 15px;
    min-width: 350px;
    background: rgb(223, 243, 253);
}
/* Кнопки ЗАГРУЗИТЬ и СОЗДАТЬ */
.editProfile button, .editProfile input[type="submit"], .fileContainer{
	border: 0;
	border-radius: 5px;
	padding: 8px;
    margin-top: 15px;
    margin-bottom: 15px;
	color: white;
    font-family: 'Courier New', Courier, monospace;
    font-size: 14px;
	background-color: #347090;
}
.editProfile button:hover, .editProfile a:hover{
    cursor: pointer;
}
/**/
.editProfile form > p{
    margin-bottom: 5px;
}
/**/
.editProfile2Colon{
    display: grid;
    grid-template-columns: max-content auto;
}
/**/
.editProfile img{
    width: 150px;
    margin: 0 auto;
}
.addDoc img:hover{
    cursor: pointer;
}
/**/
.addDoc input[type="checkbox"]{
    width: 15px;
    height: 15px;
}
/**/
.addDoc .disabled{
    pointer-events: none;
    background: rgb(133, 133, 133) !important;
}
</style>