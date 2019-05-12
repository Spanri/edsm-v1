<template>
    <div class="adm">
        <form @submit.prevent="addDoc" style="margin-bottom:80px">
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
            <p v-if="error" style="color:red">{{error}}</p>
        </form>
        <p>Настройка прав пользователей</p>
        <table>
            <thead>
                <tr>
                    <th v-for="(col,j) in columns" :key="j">
                        {{col.name}}
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(entry,j) in filteredEvents" :key="j">
                    <td v-for="(key,i) in columns" :key="i">
                        {{entry[key.code]}}
                        <svg v-if="key.code=='is_staff'" @click="entry[key.code]=!entry[key.code];editStaff(entry)" class="editStaff" width="42" height="22" xmlns="http://www.w3.org/2000/svg">
                            <g>
                                <path id="svg_2" d="m9.27039,21.301735l21.915211,0c5.075562,0 9.204388,-4.656818 9.204388,-10.381443s-4.128826,-10.381445 -9.204388,-10.381445l-21.915211,0c-5.07556,0 -9.204386,4.65682 -9.204386,10.381445s4.128826,10.381443 9.204386,10.381443zm0,-19.774178l21.915211,0c4.59211,0 8.327774,4.213385 8.327774,9.392735s-3.735664,9.392735 -8.327774,9.392735l-21.915211,0c-4.592112,0 -8.327778,-4.213383 -8.327778,-9.392735s3.735666,-9.392735 8.327778,-9.392735z"/>
                                <path id="svg_3" v-if="!entry[key.code]" d="m10.851694,17.103909c3.539827,0 6.419889,-2.827057 6.419889,-6.301741s-2.880062,-6.301731 -6.419889,-6.301731s-6.419897,2.827055 -6.419897,6.301731s2.880064,6.301741 6.419897,6.301741zm0,-11.495476c2.917307,0 5.291121,2.33012 5.291121,5.193735s-2.373814,5.193739 -5.291121,5.193739s-5.291124,-2.330116 -5.291124,-5.193739s2.373245,-5.193735 5.291124,-5.193735z"/>
                                <path id="svg_8" v-if="entry[key.code]" d="m28.549137,17.339874c3.539829,0 6.419888,-2.827057 6.419888,-6.301739s-2.880058,-6.301733 -6.419888,-6.301733s-6.419895,2.827055 -6.419895,6.301733s2.880062,6.301739 6.419895,6.301739zm0,-11.495476c2.917309,0 5.291119,2.33012 5.291119,5.193737s-2.37381,5.193737 -5.291119,5.193737s-5.291126,-2.330116 -5.291126,-5.193737s2.373245,-5.193737 5.291126,-5.193737z"/>
                            </g>
                        </svg>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import {AUTH_SIGNUP, USER_ALL_EMAILS, USER_UPDATE_STAFF} from '../../store/mutation-types'

export default {
    name: 'adm',
    data () {
        return {
            self_id: this.$store.getters.getProfile.id,
            users: [],
            email: '',
            is_staff: false,
            error: '',
            columns: [
                {
                    name: 'Пользователь',
                    code: 'name'
                },
                {
                    name: 'Email',
                    code: 'email'
                },
                {
                    name: 'Администратор',
                    code: 'is_staff'
                },
            ],
        }
    },
    created(){
        this.$store.dispatch(USER_ALL_EMAILS)
        .then(resp=>{
            console.log(resp)
            this.users = resp
        })
    },
    computed: {
        filteredEvents() {
            return this.users.filter(
                user => this.self_id != user.id
            )
        }
    },
    methods: {
        addUser(){
            let reg = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,24}))$/
            let isVaid = (this.email == "") ? "" : (reg.test(this.email));
            if (isVaid == false) {
                this.error = 'Неправильный email.'
            } else {
                this.error = 'Пользователь создается...'
                this.$store.dispatch(AUTH_SIGNUP, { email: this.email, is_staff: this.is_staff })
                .then((resp) => {
                    this.error = 'Пользователь создан. Пароль пользователя: ' + resp
                })
                .catch(err=>{
                    this.error = 'Пользователь не создан. Такой пользователь уже существует.'
                });
            }
        },
        editStaff(user){
            this.$store.dispatch(USER_UPDATE_STAFF, {
                token: this.$store.getters.token,
                id: user.id,
                is_staff: user.is_staff
            })
            .catch(err=>{
                this.error = 'Ошибка. Что-то пошло не так.'
            })
        },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* Основное */
.adm{
    margin-left: 15px;
    padding: 45px;
    padding-top: 0;
    padding-left: 60px;
}
/* Поле ввода */
.adm input[type="email"]{
	border: 0;
	margin: 0;
    height: 35px;
    padding-left: 15px;
	padding-right: 15px;
    min-width: 350px;
    background: rgb(223, 243, 253);
}
/* Кнопка СОЗДАТЬ ПОЛЬЗОВАТЕЛЯ */
.adm button{
	border: 0;
    margin-top: 15px;
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
/**/
.adm table {
    border-collapse: collapse;
}
.adm table, .adm th, .adm td{
    border: #64b2db 2px solid;
    border-radius: 5px;
}
.adm th{
    background: rgb(223, 243, 253);
}
.adm td, .adm th{
    padding: 7px 15px;
}
.adm .arrow{
    display: inline-block;
}
.adm .editStaff{
    fill: #64b2db;
    vertical-align: text-bottom;
    text-align: right;
}
.adm .editStaff:hover{
    cursor: pointer;
    fill: #347090;
}
</style>