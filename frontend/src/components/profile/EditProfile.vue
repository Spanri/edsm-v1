<template>
	<div id="editProfile">
        <div>
            <img ref="img" :src="image || 'https://img.icons8.com/wired/512/000000/document.png'">
        </div>
        <div style="margin-left:25px">
            <p v-if="error" style="color: red">{{error}}</p>
            <p></p>Получать уведомления на почту<input type="checkbox" name="common" true-value="true"  false-value="false" v-model="is_get_notif_email">
            <p>Выбрать новый аватар</p>
            <input type="file" id="file" class="inputfile" ref="file" name="file" @change="onFileChange" accept="image/*">
            <p>{{upload}}</p>
            <form @submit.prevent="">
                <p>Пароль</p>
                <MaxInput
                    v-model="password1"
                    type="password"
                    placeholder="Введите новый пароль"
                    class="search-box"
                    autocomplete="false"
                    @keyup.native="passwordValidation"
                    :max="50">
                </MaxInput>
                <div v-if="password1">
                    <p>Повторите пароль</p>
                    <MaxInput
                        v-model="password2"
                        type="password"
                        :max="50"
                        placeholder="Повторите пароль"
                        @keyup.native="passwordValidation"
                        class="search-box">
                    </MaxInput>
                    <p v-if="passError" style="color: red;display:inline-block;margin:0;margin-left:5px;">{{passError}}</p>
                </div>
                <p>Имя</p>
                <MaxInput
                    v-model="first_name"
                    type="text"
                    :max="50"
                    placeholder="Введите новое имя"
                    class="search-box">
                </MaxInput>
                <p>Фамилия</p>
                <MaxInput
                    v-model="second_name"
                    type="text"
                    :max="50"
                    placeholder="Введите новую фамилию"
                    class="search-box"
                    @keydown="onKeyDown">
                </MaxInput>
                <p>Отчество</p>
                <MaxInput
                    v-model="patronymic"
                    type="text"
                    :max="50"
                    placeholder="Введите новое отчество"
                    class="search-box">
                </MaxInput>
                <p>Должность</p>
                <MaxInput
                    v-model="position"
                    type="text"
                    :max="200"
                    placeholder="Введите новую должность"
                    class="search-box">
                </MaxInput>
                <div style="height:35px;"></div>
                <button type="button" @click="editProfile()">РЕДАКТИРОВАТЬ</button> <br>
            </form>
        </div>
	</div>
</template>

<script>
import { mapState } from 'vuex'
import axios from 'axios'
import { USER_UPDATE, USER_REQUEST, USER_UPDATE_IMAGE} from '../../store/mutation-types';
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
            is_get_notif_email: '',
            image: '',
            error: '',
            passError: '',
            upload: '',
		}
    },
    created(){
        this.$store.dispatch(USER_REQUEST)
        this.is_get_notif_email = this.$store.getters.getProfile.is_get_notif_email;
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
                this.error = 'Загружаем...'
                var image = new Image();
                var reader = new FileReader();
                var vm = this;

                reader.onload = (e) => {
                    vm.image = e.target.result;
                    this.error = ''
                };
                reader.readAsDataURL(file);
        },
        onKeyDown(evt){
            if (this.second_name.length >= 50) {
                evt.preventDefault();
                return
            }
        },
        passwordValidation(evt){
            if(this.password1 && this.password1 != this.password2) {
                this.passError = 'Пароли не совпадают.'
                return;
            } else {
                this.passError = '';
            }
        },
        editProfile(){
            try {
                if(this.password1 && this.password1 != this.password2) {
                    this.error = 'Форма заполнена неверно.'
                    return;
                } else {
                    this.passError = '';
                }
                this.error = 'Профиль обновляется...'
                if(this.file){
                    var data = new FormData();
                        console.log(data)
                        this.$store.dispatch(USER_UPDATE_IMAGE, {
                            token: this.$store.getters.token,
                            data: this.file
                        })
                        .then(resp => {
                            this.error = 'Данные профиля изменены.';
                            this.image = '';
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
                data.is_get_notif_email = this.is_get_notif_email;
                if(this.first_name) data.profile.first_name = this.first_name;
                if(this.second_name) data.profile.second_name = this.second_name;
                if(this.patronymic) data.profile.patronymic = this.patronymic;
                if(this.position) data.profile.position = this.position;
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
                    setTimeout(() => {
						this.error = '';
					}, 5000);
                })
                .catch(err=>{
                    this.error = 'Ошибка. Что-то пошло не так.'
                })
            } catch (error) {
                console.log(error)
                this.error = 'Ошибка. Что-то пошло не так...'
            }
        },
    }
}
</script>

<style scoped>
#editProfile{
    height: 100%;
	width: 100%;
    max-width: 900px;
    margin: 0 auto;
	background: white;
    padding: 25px;
    padding-top: 0;
    display: grid;
    grid-template-columns: max-content auto;
}
/* Поля ввода */
textarea, [type]:not([type="button"]):not([type="checkbox"]):not([type="file"]){
	border: 0;
	margin: 0 auto;
    height: 30px;
    padding-left: 15px;
	padding-right: 15px;
    min-width: 350px;
    background: rgb(223, 243, 253);
}
/**/
form > p{
    margin-bottom: 5px;
}
/**/
img{
    width: 150px;
    margin: 0 auto;
}
/**/
input[type="checkbox"]{
    width: 15px;
    height: 15px;
    margin-left: 15px;
}
/**/
.disabled{
    pointer-events: none;
    background: rgb(133, 133, 133) !important;
}
</style>