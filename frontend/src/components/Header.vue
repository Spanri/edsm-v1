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
                    <img>
                    <p>Tasks</p>
                </div>
                <div class="messages">
                    <img>
                    <p>Mess</p>
                </div>
                <button
                    class="registr"
                    v-if="!authenticated"
                    @click="login()">
                    Log In
                </button>
                <div v-else>
                    <img 
                        :src="userPicture"
                        class="profile-img"
                        alt="Профиль"
                        @click="searchMethod()"
                    >
                    <span class="text-muted font-weight-light px-2">{{userName}}</span>
                    <button type="button" class="registr" @click="logout()">Log out</button>
                </div>
                
            </div>
        </div>
    </div>
</template>

<script>
import AuthService from '../auth/auth2'

const auth = new AuthService()

export default {
    name: 'Header',
    data () {
        return {
            search: '',
            msg: 'Welcome to Your Vue.js App',
            // ses: this.$auth.authenticated,
            auth,
      		authenticated: auth.authenticated
        }
	},
	created () {
		auth.authNotifier.on('authChange', authState => {
			this.authenticated = authState.authenticated
		})
		auth.renewSession()
	},
    computed: {
        reg(){
            return sessionStorage.getItem('session') == "true" ? true : false;
            //return this.$auth.isAuthenticated() ? true : false;
        },
        userPicture(){
            if(this.$auth.isAuthenticated()){
                return $auth.user.picture;
            }
            else {
                return 'https://pp.userapi.com/c851524/v851524410/85b88/2TnUyrh5azw.jpg?ava=1';
            }
        },
        userName(){
            if(this.$auth.isAuthenticated()){
                return this.$auth.user.name;
            }
            else {
                console.log(this.$auth.isAuthenticated());
                return 'Нет имени';
            }
        }
    },
    methods: {
        searchMethod(){
            console.log(this.search);
        },
		login () {
			auth.login()
		},
		logout () {
			auth.logout()
		}
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
.header-right > .tasks, .header-right > .messages, .header-right > .registr{
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
