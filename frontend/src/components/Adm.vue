<template>
    <div class="adm">
        <form @submit.prevent="addDoc">
            <p>Email того, кому нужно создать аккаунт</p>
            <input 
                required
                v-model="email"
                type="email" 
                placeholder="Введите email"
            />
            <p style="display: inline-block;"> Администратор</p>
            <input class="checkbox" type="checkbox" name="common" true-value="1"  false-value="0" v-model="is_staff">
            <br>
            <button type="button" @click="addUser">СОЗДАТЬ ПОЛЬЗОВАТЕЛЯ</button> <br>
            <p>{{error}}</p>
        </form>
    </div>
</template>

<script>
import {AUTH_SIGNUP} from '../store/mutation-types'

export default {
    name: 'Menu',
    data () {
        return {
            email: '',
            is_staff: false,
            error: ''
        }
    },
    methods: {
        addUser(){
            this.error = 'Пользователь создается...'
            this.$store.dispatch(AUTH_SIGNUP, { email: this.email, is_staff: this.is_staff })
            .then((resp) => {
                this.error = 'Пользователь создан. Пароль пользователя: ' + resp
            });
        },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* Основное */
.adm{
    margin-left: 15px;
}
.adm *{
    margin: 15px;
}
/* Поле ввода */
.adm input [type]:not([type="checkbox"]){
	border: 0;
	margin: 15px;
    height: 30px;
    padding-left: 15px;
	padding-right: 15px;
    min-width: 350px;
    background: rgb(223, 243, 253);
}
/* Кнопка СОЗДАТЬ ПОЛЬЗОВАТЕЛЯ */
.adm button{
	border: 0;
	border-radius: 5px;
	padding: 8px;
	color: white;
	background-color: #347090;
}
.adm button:hover{
	cursor: pointer;
}
/**/
.adm input[type="checkbox"]{
    height: 15px;
    width: 15px;
    margin: 0;
    vertical-align: middle;
}
</style>