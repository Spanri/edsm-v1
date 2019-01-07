<template>
	<div class="background">
		<div class="footer">
			<div></div>
			<a href="">О кафедре</a>
			<a href="">Что-то</a>
			<div></div>
		</div>
	</div>
</template>

<script>
export default {
	name: 'Header',
	data () {
		return {
		msg: 'Welcome to Your Vue.js App'
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
.footer{
    width: 100%;
    max-width: 1400px;
	margin: auto;
    margin-top: 0;
	display: grid;
    grid-template-columns: auto max-content max-content auto;
	text-align: center;
}
a{
	margin: 10px;
	text-decoration: none;
	color: white;
}
a:hover{
	color: #b1d887;
}
</style>