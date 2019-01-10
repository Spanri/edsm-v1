<template>
    <div class="background">
        <div class="header">
            <div class="logo">
                <p style="color:white">CRM-система</p>
                <p style="color:#d4e887">МКиИТ</p>
            </div>
            <div></div>
            <div class="search">
                <input
                    class="search-box"
                    type="text" 
                    v-model="search" 
                    placeholder="Введите что-то..." />
                <img 
                    src="../assets/search.svg"
                    class="search-img"
                    alt="Поиск"
                    @click="searchMethod()"
                >
            </div>
            <div class="header-right">
                <div class="tasks">
                    <p>Tasks</p>
                </div>
                <div class="messages">
                    <p>Mess</p>
                </div>
                <button
                    class="registr"
                    v-if="!isAuthenticated"
                    @click="login()">
                    Вход / Регистрация
                </button>
                <dropdown-menu v-else
                    :options="mainMenuOptions">
                </dropdown-menu>
                
            </div>
        </div>
    </div>
</template>

<script>
import DropdownMenu from './DropdownMenu';
import {AUTH_LOGOUT} from '../store/mutation-types'

export default {
    name: 'Header',
    components: { DropdownMenu },
    data () {
        return {
            search: '',
            mainMenuOptions: [
                "Профиль",
                "component data",
                "component methods",
                "component events",
                "Выйти"
            ],
        }
	},
    computed: {
        isAuthenticated(){ 
            return this.$store.getters.isAuthenticated;
        }
        // userPicture(){

        // },
    },
    methods: {
        searchMethod(){
            console.log(this.search);
        },
		login () {
			this.$router.push('/auth');
		},
		logout () {
			this.$store.dispatch(AUTH_LOGOUT)
			.then(() => {
				this.$router.push('/auth')
			});
        },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.background{
    background-color: #3e5468;
    height: 70px;
}
.header{
    width: 100%;
    max-width: 1400px;
	margin: auto;
    margin-top: 0;
    display: grid;
    grid-template-columns: max-content auto auto max-content;
    color:aliceblue;
}
.header > *{
    margin: 10px;
    padding: 0;
}
.search{
    background: #7cb0c1;
    width: 100%;
    max-width: 400px;
    color: white;
    display: grid;
    grid-template-columns: auto max-content;
    margin: 15px;
}
.search > *{
    margin: 10px;
}
.search-box{
    background:#4c545700;
    border: 0;
    color: white;
    font-size: 15px;
}
.search-box:focus{
    outline: none;
}
.search-img{
    width: 20px;
}
.profile-img{
    margin: 5px;
    width: 40px;
    border-radius: 50%;
}
.search-img:hover{
    cursor: pointer;
}
.header-right{
    display: inline-grid;
    grid-template-columns: repeat(3, max-content);
}
.header-right > .tasks, .header-right > .messages{
    margin: 0px;
    margin-right: 10px;
    margin-left: 10px;
    padding: 0;
}
.logo{
    margin: auto;
    margin-left: 30px;
    font-family: Arial, Helvetica, sans-serif;
    font-weight: 800;
    font-size: 20px;
    text-align: center;
}
.logo > *{
    margin: 2px;
}
.messages{
    display: inline-grid;
    grid-template-columns: repeat(2, max-content);
}
.registr{
    border: 0;
    padding: 7px;
    margin: 7px;
    background-color: #7cb0c1;
    color: white;
}
.registr:hover{
    cursor: pointer;
    background-color: #6393a3;
    transition: background-color .3s ease-out;
}
</style>
