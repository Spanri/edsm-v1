<template>
<div id="maing">
	<Menu></Menu>
	<router-view></router-view>
</div>
</template>

<script>
import Menu from '../components/Menu';

export default {
	name: 'auth',
	components: { Menu },
}
</script>

<style scoped>
#maing{
    height: 100%;
	width: 100%;
	background: white;
	display: grid;
    grid-template-columns: min-content auto;
}
.r{
	width: 100%;
	max-width: 1400px;
	margin: auto;
	margin-top: 0;
	margin-bottom: 0;
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
    color: rgb(75, 54, 54);
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
router-view{
	overflow-y: auto;
	height: 100vh;
}
@media (max-width: 500px) {
	.maing{
		grid-template-columns: auto;
		grid-template-rows: min-content auto;
	}
}
</style>
