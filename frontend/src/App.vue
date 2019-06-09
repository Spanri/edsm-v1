<template>
	<div id="app">
		<div v-if="!this.$store.getters.isAuthenticated">
			<Auth></Auth>
		</div>
		<div v-else class="a">
			<Header></Header>
			<router-view></router-view>
			<Footer></Footer>
		</div>
	</div>
</template>

<script>
import Auth from './components/Auth';
import Header from './components/Header';
import Footer from './components/Footer';
import axios from 'axios'
// import {USER_REQUEST} from './store/mutation-types'
      
export default {
	name: 'App',
	components: { Header, Footer, Auth },
	data () {
        return {
			closeButtonSize: "300px auto",
			menuSize: "300px auto",
			marginLeft: 20,
			close: false,
			textClose: "X СВЕРНУТЬ МЕНЮ",
    	}
	},
	created: function () {
		axios.interceptors.response.use(undefined, function (err) {
			return new Promise(function (resolve, reject) {
				if (err.status === 401 && err.config && !err.config.__isRetryRequest) {
				// if you ever get an unauthorized, logout the user
					this.$store.dispatch(AUTH_LOGOUT)
				// you can also redirect to /login if needed !
				}
			throw err;
		});
});
	},
	computed: {
		// login: function() {
		// 	return this.$store.getters.login;
		// },
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
			this.close = !this.close;
		},
    }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css?family=El+Messiri:600|Roboto:300|Spectral&display=swap');
#app{
	font-family: 'Roboto', serif;
	font-weight: 500;
}
.a {
	height: 100vh;
	width: calc(100vw-15px);
	display: grid;
	grid-template-rows: max-content auto max-content;
}
*:hover{
	transition: all 0.2s;
}
router-view{
	overflow-y: auto;
	height: 100vh;
}
@media (max-width: 500px) {
	*{
		font-size: 14px;
	}
}
</style>
