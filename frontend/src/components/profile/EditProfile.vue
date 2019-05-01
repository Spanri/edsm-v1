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
                        type="text" 
                        placeholder="Введите имя"
                        class="search-box"
                    />
                    <p>ФИО</p>
                    <input
                        v-model="name"
                        type="text" 
                        placeholder="Введите имя"
                        class="search-box"
                    />
                    <p>Пароль</p>
                    <input
                        v-model="password"
                        type="text" 
                        placeholder="Введите имя"
                        class="search-box"
                    />
                    <div v-if="password">
                        <p>Повторите пароль</p>
                        <input
                            v-model="password2"
                            type="text" 
                            placeholder="Введите имя"
                            class="search-box"
                        />
                    </div>
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
            email: '',
            name: '',
            password: '',
            password2: '',
            image: '',
            error: '',
            upload: '',            
		}
    },
    computed: {
		profile: function(){
            //console.log(this.$store.getters.getProfile)
			return this.$store.getters.getProfile
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
                name: this.name,
                image: this.image,
                email: this.email,
                password: this.password
            })
            .then(() => {
                this.error = 'Данные профиля изменены.';
                this.name = '';
                this.image = '';
                this.email = '';
                this.password = '';
                this.password2 = ''; 
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
.editProfile textarea, .editProfile input[type="text"]{
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