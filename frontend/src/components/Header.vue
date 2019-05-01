<template>
    <div class="background">
        <div class="header">
            <div class="logo" @click="toMain()" title="На главную">
                <img src="https://img.icons8.com/material-outlined/30/FFFFFF/student-center.png">
                <p style="color:white">СЭД МТУСИ</p>
            </div>
            <div></div>
            <div class="header-right">
                <div class="icon" title="Добавить документ" @click="toAddDoc">
                    <div>+</div>
                    <svg fill="white" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="30px" height="30px">
                        <path
                            d="M13.172,2H6C4.9,2,4,2.9,4,4v16c0,1.1,0.9,2,2,2h12c1.1,0,2-0.9,2-2V8.828c0-0.53-0.211-1.039-0.586-1.414l-4.828-4.828 C14.211,2.211,13.702,2,13.172,2z M15,18H9c-0.552,0-1-0.448-1-1v0c0-0.552,0.448-1,1-1h6c0.552,0,1,0.448,1,1v0 C16,17.552,15.552,18,15,18z M15,14H9c-0.552,0-1-0.448-1-1v0c0-0.552,0.448-1,1-1h6c0.552,0,1,0.448,1,1v0 C16,13.552,15.552,14,15,14z M13,9V3.5L18.5,9H13z"/>
                    </svg>
                </div>
                <div class="icon" title="Уведомления" @click="toNotif">
                    <div :style="{ color: notifColor }">{{notif}}</div>
                    <img :src="notifIcon">
                </div>
                <img class="profile" @click="profile()" title="Профиль" src="../assets/profile-img.jpg">       
            </div>
        </div>
    </div>
</template>

<script>
import {AUTH_LOGOUT, DOCS_REQUEST} from '../store/mutation-types'

export default {
    name: 'Header',
    components: {  },
    data () {
        return {
            search: '',
            notif: '',
        }
    },
    created() {
        this.$store.dispatch(DOCS_REQUEST, "notif")
            .then(()=>{
                this.notif = this.$store.getters.getDoc.length;
            });
    },
    computed: {
        notifColor(){
            if (this.notif > 0) {
                return "#ff7373"
            }
            else return "#FFFFFF"
        },
        notifIcon(){
            if (this.notif > 0) {
                return "https://img.icons8.com/material/30/ff7373/bell.png"
            }
            else return "https://img.icons8.com/material/30/FFFFFF/bell.png";
        }
    },
    methods: {
        toMain(){
            this.$router.push('/');
        },
        toNotif(){
            this.$router.push('/profile/notif');
        },
        toAddDoc(){
            this.$router.push('/addDoc');
        },
        profile(){
            this.$router.push('/profile/notif');
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
    /* background-color: #ff7373; */
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
    margin: 10.5px;
    margin-left: 8px;
    margin-right: 20px;
    width: 38px;
    height: 38px;
    border: 0;
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
/**/
.icon{
    font-size: 24px;
    font-weight: 700;
    margin: 12.5px;
    display: grid;
    grid-template-columns: max-content max-content;
}
.icon:hover{
    cursor: pointer;
    color: #7cb0c1;
}
.icon:hover svg{
    fill: #7cb0c1;
}
.icon div{
    padding: 0px;
    margin: 0;
    margin-top: 3px;
    margin-left: 2px;
}
</style>
