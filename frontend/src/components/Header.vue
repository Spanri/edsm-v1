<template>
    <div class="background">
        <div class="header">
            <div class="logo" @click="toMain()">
                <svg width="30px" height="30px">
                    <circle cx="15" cy="15" r="15" fill="white"/>
                </svg>
                <p style="color:white">СЭД МТУСИ</p>
            </div>
            <div></div>
            <div class="header-right">
                <div class="add">
                    <p>Add</p>
                </div>
                <div class="messages">
                    <p>Mess</p>
                </div>
                <div class="profile" @click="profile()">
                    <img >  
                </div>        
            </div>
        </div>
    </div>
</template>

<script>
import {AUTH_LOGOUT} from '../store/mutation-types'

export default {
    name: 'Header',
    components: {  },
    data () {
        return {
            search: '',
        }
	},
    computed: {
        // userPicture(){

        // },
    },
    methods: {
        toMain(){
            this.$router.push('/');
        },
        profile(){
            this.$router.push('/profile');
        },
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

<style scoped>
/* Фон */
.background{
    background-color: #347090;
    height: 60px;
}
/* Основной стиль */
.header{
    width: 100%;
    height: 60px;
    max-width: 1400px;
	margin: auto;
    margin-top: 0;
    display: grid;
    grid-template-columns: auto auto max-content;
    color:white;
}
/* Логотип */
.logo{
    margin: 14px;
    margin-left: 30px;
    font-size: 24px;
    text-align: center;
    display: grid;
    grid-template-columns: max-content max-content;
}
.logo > *{
    margin: 0;
    margin-right: 10px;
}
.logo > p{
    margin: 0;
    margin-top: 3px;
}
.logo:hover{
    cursor: pointer;
}
/* Добавить документ, уведомления, профиль */
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
.header-right p{
    padding: 5px;
}
/* Профиль */
.profile{
    margin: 12.5px;
    width: 35px;
    height: 35px;
    background-color: white;
    border-radius: 50%;
}
.profile:hover{
    cursor: pointer;
    box-shadow: 0px 0px 10px 0px white;
}
/* Уведомления */
.messages{
    display: inline-grid;
    grid-template-columns: repeat(2, max-content);
}
/*  */
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
