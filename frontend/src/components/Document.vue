<template>
	<div class="document">
		<h3 class="header">{{this.title}}</h3>
		<div class="document2Colon">
			<div>
                <div @click="bigImage = 1" class="imageScale">
                    <img :src="image || 'https://img.icons8.com/wired/512/000000/document.png'">
                </div>
                <div v-if="bigImage == 1" @click="bigImage = 0">
                    <img class="bigImage" :src="image">
                    <div class="bigImageBackground"></div>
                </div>
				<button @click="edith">РЕДАКТИРОВАТЬ</button> <br>
            </div>
			<div style="margin-left:25px">
				<p>Описание:</p>
				{{description}}
				<p>Общий доступ: {{common ? 'да' : 'нет'}} </p>
			</div>
		</div>
	</div>
</template>

<script>
import { mapState } from 'vuex'
import { DOC_REQUEST } from '../store/mutation-types';

export default {
	name: 'account',
	props: {
		id: String,
        data: Object,
	},
	data () {
        return {
			title: '',
			bigImage: '',
			image: '',
			description: '',
			common: ''
        }
	},
	created(){
		console.log(this.id);
		this.$store.dispatch(DOC_REQUEST, this.id)
		.then((resp) => {
			this.title = resp.title,
			this.image = resp.image;
			this.description = resp.description;
			this.common = resp.common;
		})
	},
	methods: {
		edith(){
			console.log('dfgg')
		},
	},
}
</script>

<style>
.document{
    height: 100%;
	width: 100%;
    max-width: 900px;
    margin: 0 auto;
	background: white;
    padding: 25px;
}
.document .header{
    margin-top: 0;
	margin-bottom: 30px;
}
/**/
.document2Colon{
    display: grid;
    grid-template-columns: max-content auto;
}
/**/
.document button{
	border: 0;
	border-radius: 5px;
	padding: 8px;
    margin-top: 15px;
    margin-bottom: 15px;
	color: white;
    font-family: 'Courier New', Courier, monospace;
    font-size: 14px;
	background-color: #347090;
}
.document button:hover{
	cursor: pointer;
}
/**/
.document img{
    width: 200px;
	border: 0.5px solid #347090;
}
/* Картинка при увеличении*/
.document .bigImage{
    position: fixed;
    min-width:400px;
	max-height: 700px;
    height:auto;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    z-index: 5;
}
.document .imageScale:hover{
    cursor: pointer;
}
.document .bigImageBackground{
    position: fixed;
    width:100%;
    height:100%;
    padding: 0;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    margin: 0;
    background-color: #2746578c;
    z-index: 2;
}
</style>