<template>
	<div id="app">
		<Header></Header>
		<!-- <div class="gradient r">
			<div class="close-button" v-bind:style="{ gridTemplateColumns: closeButtonSize }">
				<p 
					class="close" 
					@click="closeMenu()"
					>{{ textClose }}
				</p>
				<p 
					class="name" 
					v-bind:style="{ marginLeft: marginLeft + 'px' }"
					>ГЛАВНАЯ
				</p>
			</div>
			<div class="main-space" v-bind:style="{ gridTemplateColumns: menuSize }">
				<Menu v-if="closeM == false"></Menu>
				<router-view
					:auth="auth"
					:authenticated="authenticated">
				</router-view>
			</div>
		</div> -->
		<g-signin-button
				v-if="isEmpty(user)"
				:params="googleSignInParams"
				@success="onGoogleSignInSuccess"
				@error="onGoogleSignInError"
          	>
        	<button class="btn btn-block btn-success">
              	Google Signin
        	</button>
        </g-signin-button>
        <user-panel v-else :user="user"></user-panel>
		<!-- <Footer></Footer> -->
		
	</div>
</template>

<script>
import Header from './components/Header';
import Menu from './components/Menu';
import Footer from './components/Footer';
import AuthService from './auth/auth2'
import axios from 'axios'
import UserPanel from '@/components/UserPanel'
const auth = new AuthService()
      
export default {
	name: 'App',
	components: { Header, Footer, Menu, UserPanel },
	data () {
        return {
			closeButtonSize: "300px auto",
			menuSize: "300px auto",
			marginLeft: 20,
			close: false,
			textClose: "X СВЕРНУТЬ МЕНЮ",
			msg: 'Welcome to Your Vue.js App',
			auth,
			authenticated: auth.authenticated,
			user: {},
			googleSignInParams: {
				client_id: '418428102857-0ja9r62ggu43baf67gdfufoj6mjntku0.apps.googleusercontent.com'
			}
    }
  },
//   created () {
//     auth.authNotifier.on('authChange', authState => {
//       this.authenticated = authState.authenticated
//     })
//     auth.renewSession()
//   },
	computed: {
		closeM: function () {
			if(this.close){
				this.menuSize = "100%";
				this.closeButtonSize = "0 100%";
				this.marginLeft = 50;
				this.textClose = "!!!";
				return true;
			}
			else{
				this.menuSize = "300px auto";
				this.closeButtonSize = this.menuSize;
				this.marginLeft = 20;
				this.textClose = "X СВЕРНУТЬ МЕНЮ";
				return false;
			}
		}
	},
    methods: {
        closeMenu() {
			console.log(this.close);
			this.close = !this.close;
			console.log(this.close);
		},
			onGoogleSignInSuccess (resp) {
				
		const token = resp.Zi.access_token
		console.log(token)
		// После успешного входа через Google,
		// отправляем токен доступа на бэкэнд и получаем взамен
		// пользователя и JWT токен
		// P.S. JWT токен в нашем примере не нужен, поэтому его не сохраняем
		axios.post('http://localhost:8000/auth/google/', {
			access_token: token
		})
			.then(resp => {
			this.user = resp.data.user
			})
			.catch(err => {
			console.log(err.response)
			})
		},
		onGoogleSignInError (error) {
		console.log('OH NOES', error)
		},
		isEmpty (obj) {
		return Object.keys(obj).length === 0
		}
    }
}
</script>

<style>
#app {
	height: 100vh;
	width: 100vw;
	display: grid;
	grid-template-rows: max-content auto max-content;
	background: #7cb0c1; /* Old browsers */
    background: -moz-linear-gradient(45deg, #7cb0c1 0%, #b1d887 48%, #f9f88e 100%); /* FF3.6-15 */
    background: -webkit-linear-gradient(45deg, #7cb0c1 0%,#b1d887 48%,#f9f88e 100%); /* Chrome10-25,Safari5.1-6 */
    background: linear-gradient(45deg, #7cb0c1 0%,#b1d887 48%,#f9f88e 100%); /* W3C, IE10+, FF16+, Chrome26+, Opera12+, Safari7+ */
    filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#7cb0c1', endColorstr='#f9f88e',GradientType=1 ); /* IE6-9 fallback on horizontal gradient */
}
.r{
	width: 100%;
	max-width: 1400px;
	margin: auto;
	margin-top: 0;
	margin-bottom: 0;
}
.gradient{
	
}
.main-space{
	height: 100%;
	width: 100%;
	display: grid;
}
.close{
    text-align: center;
    height: 30px;
    margin: 20px;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 15px;
    color: white;
}
.close:hover{
	cursor: pointer;
}
.close-button{
	display: grid;
}
.name{
    height: 30px;
    margin: 20px;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 25px;
    color: white;
}
</style>
