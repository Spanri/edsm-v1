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
                    <img src="https://img.icons8.com/ios/30/FFFFFF/document-filled.png">
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
import {AUTH_LOGOUT, DOC_REQUEST} from '../store/mutation-types'

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
        this.$store.dispatch(DOC_REQUEST, "notif")
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
.icon div{
    padding: 0px;
    margin: 0;
    margin-top: 3px;
    margin-left: 2px;
}
</style>
