<template>
	<div class="document">
		<h3 class="header">{{title}}</h3>
		<div class="document2Colon">
			<preview :typeFile="type"></preview>
			<div style="margin-left:25px;margin-top:-15px;">
				<div class="buttons">
					<button v-if="doc.doc.size/1024/1024 < 25" @click="viewDoc()">СМОТРЕТЬ</button>
					<button @click="download()">СКАЧАТЬ</button>
					<a class="button" :href="fileWithSignature" download="FileName">СКАЧАТЬ С ПОДПИСЬЮ</a>
					<button @click="editDoc()">РЕДАКТИРОВАТЬ</button>
					<button v-if="doc.status == 2" @click="addSignature()">ПОДПИСАТЬ (не работает)</button>
					<button v-if="doc.status == 0" @click="repeatSignatures()">ЗАПУСТИТЬ ЦЕПОЧКУ ПОДПИСЕЙ СНОВА (не работает)</button>
				</div>
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
// import FileReader from 'vue-filereader'
import { mapState } from 'vuex'
import { DOC_REQUEST, DOCS_REQUEST, DOC_SIGNATURE } from '../store/mutation-types';
import Preview from '../components/addit/Preview';

import axios from 'axios'

export default {
	name: 'account',
	components: { Preview },
	props: {
		id: String,
	},
	data () {
        return {
			file: '',
			doc: {},
			title: '',
			type: '',
			fileWithSignature: 'ddd',
			error: '',
        }
	},
	created() {
		this.$store.dispatch(DOCS_REQUEST)
		this.doc = this.$store.getters.getDoc(this.id);
		let typeFile = this.doc.doc.title.split('.');
		this.type = typeFile[typeFile.length-1];
		this.title = this.doc.doc.title.replace("." + this.type, "");
		console.log(this.doc)
	},
	methods: {
		viewDoc() {
			let type = this.type.toLowerCase();
			console.log(type);
			let url = '';
			if(type != "jpg" && type != "jpeg" && type != "png"){
				if(type == "txt") {
					url = "https://docs.google.com/viewerng/viewer?url=" + this.doc.doc.file + ".txt";
				} else {
					url = "https://docs.google.com/viewerng/viewer?url=" + this.doc.doc.file;  
				}
			} else {
				url = this.doc.doc.file;
			}
			window.open(url, "_blank");
      	},
		download(){
			this.error = "Скачивается..."
			let title = this.doc.doc.title
			axios({
				url: this.doc.doc.file,
				method: 'GET',
				responseType: 'blob', // important
			}).then((response) => {
				const url = window.URL.createObjectURL(new Blob([response.data]));
				const link = document.createElement('a');
				link.href = url;
				link.setAttribute('download', title); //or any other extension
				document.body.appendChild(link);
				link.click();
				this.error = ""
			});
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
	width: auto;
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
.document .buttons{
	max-width: 600px;
}
.document a{
	color: white;
	text-decoration: none;
}
.document button:hover, .document .button:hover{
	cursor: pointer;
}
</style>