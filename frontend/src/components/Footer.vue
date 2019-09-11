<template>
	<div class="background">
		<div id="footer">
			<p>МТУСИ, 2019 | <label @click="toHelp()">Помощь</label></p>
		</div>
	</div>
</template>

<script>
export default {
	name: 'Header',
	data () {
		return {
			// msg: 'Welcome to Your Vue.js App'
		}
	},
	methods: {
		toHelp(){
			this.$router.push('/help');
		},
	}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.background{
    background-color: #347090;
    height: 40px;
}
#footer{
    width: 100%;
    max-width: 1400px;
	margin: auto;
    margin-top: 0;
	text-align: center;
}
p{
	margin: 8px;
	color: white;
}
label{
	color: white;
	text-decoration: none;
  text-decoration: underline;
}
label:hover{
	cursor: pointer;
	color: #aaa9f8;
}
</style>
