<template>
	<div class="document">
		<h3 class="header">{{doc.title}}</h3>
		<div class="document2Colon">
			<div>
                <div @click="bigImage = 1" class="imageScale">
                    <img :src="doc.doc.preview || 'https://img.icons8.com/wired/512/000000/document.png'">
                </div>
                <div v-if="bigImage == 1" @click="bigImage = 0">
                    <img class="bigImage" :src="doc.doc.preview || 'https://img.icons8.com/wired/512/000000/document.png'">
                    <div class="bigImageBackground"></div>
                </div>
				<a class="button" :href="this.doc.doc.file" download="FileName">СКАЧАТЬ</a>
				<button @click="editDoc()">РЕДАКТИРОВАТЬ</button> <br v-if="!doc.is_owner && doc.is_signature_request && !doc.is_signature && doc.is_queue">
				<button v-if="doc.status == 2" @click="addSignature()">ПОДПИСАТЬ</button> <br>
				<button v-if="doc.status == 0" @click="repeatSignatures()">ЗАПУСТИТЬ ЦЕПОЧКУ<br>ПОДПИСЕЙ СНОВА</button> <br>
            </div>
			<div style="margin-left:25px">
				<p v-if="error" style="color: red">{{error}}</p>
				<p>Владелец: {{doc.user.profile.full_name}} ({{doc.user.email}})</p>
				<p>Общий доступ: {{doc.doc.common ? 'да' : 'нет'}} </p>
				<p>Дата добавления: {{doc.doc.date}} </p>
				<p>Описание:</p>
				<p> {{ doc.doc.description }}</p>
			</div>
		</div>
	</div>
</template>

<script>
import { mapState } from 'vuex'
import { DOC_REQUEST, DOCS_REQUEST, DOC_SIGNATURE } from '../store/mutation-types';

export default {
	name: 'account',
	props: {
		id: String,
	},
	data () {
        return {
			doc: {},
			bigImage: '',
			image: '',
			error: '',
        }
	},
	created() {
		this.$store.dispatch(DOCS_REQUEST)
		this.doc = this.$store.getters.getDoc(this.id);
		console.log('docs', this.doc)
	},
	methods: {
		download(){
			const path = this.doc.doc.file
			const link = document.createElement('a')
			link.href = path
			link.download = path.substr(path.lastIndexOf('/') + 1);
			document.body.appendChild(link)
			link.click()
			document.body.removeChild(link);
		},
		editDoc(){
			console.log('editDoc')

		},
		async addSignature(){
			console.log('addSignature')
			let res = await confirm('Подтвердите подпись.', { title: 'Подтверждение' })
			if (res) {
				this.$store.dispatch(DOC_SIGNATURE, this.id)
				.then(resp => {
					this.doc.status = 3;
					this.error = 'Подпись успешно поставлена!'
				})
				.catch(err=>{
					console.log(err)
					this.error = 'Ошибка. Что-то пошло не так.'
				})
			}
		},
		repeatSignatures(){
			console.log('repeatSignatures')
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
.document button, .document .button{
	width: 100%;
	border: 0;
	border-radius: 5px;
	padding: 8px;
    margin-top: 5px;
    margin-bottom: 5px;
	color: white;
    font-family: 'Courier New', Courier, monospace;
    font-size: 14px;
	background-color: #347090;
	text-align: center;
}
.document .button{
	width: calc(100% - 16px);
	display: block;
}
.document a{
	color: white;
	text-decoration: none;
}
.document button:hover, .document .button:hover{
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