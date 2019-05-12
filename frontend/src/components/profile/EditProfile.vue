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
                <input type="file" id="file" class="inputfile" ref="file" name="file" @change="onFileChange">
                <p>{{upload}}</p>
                <form @submit.prevent="editProfile">
                    <p>Пароль</p>
                    <MaxInput
                        v-model="password1"
                        type="password" 
                        placeholder="Введите имя"
                        class="search-box"
                        autocomplete="false"
                        :max="50">
                    </MaxInput>
                    <div v-if="password1">
                        <p>Повторите пароль</p>
                        <MaxInput
                            v-model="password2"
                            type="password" 
                            :max="50"
                            placeholder="Введите имя"
                            class="search-box">
                        </MaxInput>
                    </div>
                    <p>Имя</p>
                    <MaxInput
                        v-model="first_name"
                        type="text" 
                        :max="50"
                        placeholder="Введите имя"
                        class="search-box">
                    </MaxInput>
                    <p>Фамилия</p>
                    <MaxInput
                        v-model="second_name"
                        type="text" 
                        :max="50"
                        placeholder="Введите фамилию"
                        class="search-box"
                        @keydown="onKeyDown">
                    </MaxInput>
                    <p>Отчество</p>
                    <MaxInput
                        v-model="patronymic"
                        type="text" 
                        :max="50"
                        placeholder="Введите отчество"
                        class="search-box">
                    </MaxInput>
                    <p>Должность</p>
                    <MaxInput
                        v-model="position"
                        type="text" 
                        :max="200"
                        placeholder="Введите отчество"
                        class="search-box">
                    </MaxInput>
                    <div style="height:35px;"></div>
                    <button type="submit">РЕДАКТИРОВАТЬ</button> <br>
                </form>
            </div>
        </div>
	</div>
</template>

<script>
import { mapState } from 'vuex'
import axios from 'axios'
import { USER_UPDATE, USER_UPDATE_IMAGE } from '../../store/mutation-types';
import MaxInput from '@/components/addit/MaxInput'

export default {
    name: 'edirProfile',
    components: { MaxInput },
    data () {
		return {
            password1: '',
            password2: '',
            first_name: '',
            second_name: '',
            patronymic: '',
            position: '',
            image: '',
            error: '',
            upload: '',
		}
    },
    methods: {
        onFileChange(e) {
            this.upload = "Загружается..."
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length) return;
            let formData = new FormData();
            formData.append('profile.photo', files[0]); 
            this.file = formData;
            this.createImage(files[0]);
            this.upload = "";
        },
        createImage(file) {
            var image = new Image();
            var reader = new FileReader();
            var vm = this;

            reader.onload = (e) => {
                vm.image = e.target.result;
            };
            reader.readAsDataURL(file);
        },
        onKeyDown(evt){
            if (this.second_name.length >= 50) {
                evt.preventDefault();
                console.log('keydown');
                return
            }
        },
        editProfile(){
            this.eror = 'Профиль обновляется...'
            try {
                if(this.password1 && this.password1 != this.password2) {
                    this.error = 'Пароли не совпадают.'
                    return;
                } else {
                    this.error = '';
                }
                if(this.file){
                    this.$store.dispatch(USER_UPDATE_IMAGE, {
                        token: this.$store.getters.token, 
                        data: this.file
                    })
                    .then(resp => {
                        // console.log(resp)
                        this.error = 'Данные профиля изменены.';
                        this.file = '';
                    })
                    .catch(err => {
                        console.log(err)
                        this.error = 'Ошибка. Что-то пошло не так.'
                    })
                }
                let data = {
                    profile: {}
                }
                if(this.password1) data.password = this.password1;
                if(this.first_name) data.profile.first_name = this.first_name;
                if(this.second_name) data.profile.second_name = this.second_name;
                if(this.patronymic) data.profile.patronymic = this.patronymic;
                if(this.position) data.profile.position = this.position;
                console.log(data)
                if('first_name' in data.profile || 'password' in data || 'second_name' in data.profile 
                        || 'patronymic' in data.profile || 'position' in data.profile){
                    console.log('data')
                    this.$store.dispatch(USER_UPDATE, {
                        token: this.$store.getters.token,
                        data
                    })
                    .then(resp => {
                        this.error = 'Данные профиля изменены.';
                        this.password1 = '';
                        this.password2 = '';
                        this.first_name = '';
                        this.second_name = '';
                        this.patronymic = '';
                        this.position = '';
                    })
                    .catch(err=>{
                        this.error = 'Ошибка. Что-то пошло не так.'
                    })
                }
            } catch (error) {
                this.eror = 'Ошибка. Что-то пошло не так...'
            }
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