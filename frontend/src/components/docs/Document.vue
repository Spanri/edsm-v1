<template>
	<div class="document">
		<h3 class="header">{{title}}</h3>
		<div class="document2Colon">
			<div>
				<preview :typeFile="type"></preview>
				<button style="margin-top:20px;margin-left:6px;background: rgb(243, 92, 92);" v-if="doc.status == 0" @click="deleteDoc()">УДАЛИТЬ</button>
			</div>
			<div style="margin-left:25px;margin-top:-15px;">
				<div class="buttons">
					<button v-if="doc.doc.size/1024/1024 < 25" @click="viewDoc()">СМОТРЕТЬ ДОКУМЕНТ</button>
					<button v-if="doc.doc.size/1024/1024 < 25" @click="viewSign()">СМОТРЕТЬ ПОДПИСЬ (не работает)</button>
					<br>
					<button @click="download()">СКАЧАТЬ</button>
					<button @click="downloadSign()">СКАЧАТЬ ПОДПИСЬ (не работает)</button>
					<br>
					<button @click="editDoc()">РЕДАКТИРОВАТЬ (не работает)</button>
					<button v-if="doc.status == 2" @click="confirmCode()">ПОДПИСАТЬ</button>
					<button v-if="doc.status == 0" @click="repeatSignatures()">ЗАПУСТИТЬ ЦЕПОЧКУ ПОДПИСЕЙ СНОВА (не работает)</button>
				</div>
				<p v-if="error" style="color: red">{{error}}</p>
				<p>Владелец: {{doc.user.profile.full_name}} ({{doc.user.email}})</p>
				<p>Общий доступ: {{doc.doc.common ? 'да' : 'нет'}} </p>
				<p>Дата добавления: {{doc.doc.date}} </p>
				<p>Описание:</p>
				<p> {{ doc.doc.description }}</p>
				<form v-if="isConfirm" class="confirm" :class="{addHeight: errorConfirm, notAddHeight: !errorConfirm}" @submit.prevent="addSignature">
					<p>Заглушка - код "1234". На ваше мобильное приложение отправлен код подтверждения. Введите его ниже.</p>
					<input 
                        required
                        v-model="confirm"
                        type="text"
                        placeholder="Введите код подтверждения"
                        class="code">
					<div class="confirmButtons">
						<div></div>
						<button @click="addSignature()">ПОДТВЕРДИТЬ</button>
						<button 
							@click="isConfirm = false;confirmFromApp = confirm = '';">
							ОТМЕНИТЬ
						</button>
						<div></div>
					</div>
					<p v-if="errorConfirm" style="color: red;text-align: center;padding: 5px">{{errorConfirm}}</p>
				</form>
			</div>
		</div>
	</div>
</template>

<script>
// import FileReader from 'vue-filereader'
import { mapState } from 'vuex'
import { DOC_REQUEST, DOCS_REQUEST, DOC_SIGNATURE, DOC_DELETE } from '../../store/mutation-types';
import Preview from '../addit/Preview';

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
			errorConfirm: '',
			isConfirm: false,
			confirm: '',
			confirmFromApp: '',
        }
	},
	created() {
		this.$store.dispatch(DOCS_REQUEST)
		this.doc = this.$store.getters.getDoc(this.id);
		let typeFile = this.doc.doc.title.split('.');
		this.type = typeFile[typeFile.length-1];
		this.title = this.doc.doc.title.replace("." + this.type, "");
		this.type = this.type.toLowerCase();
		console.log(this.type)
	},
	methods: {
		viewDoc() {
			try{
				let url = '';
				if(this.type != "jpg" && this.type != "jpeg" && this.type != "png"){
					// if(this.type == "txt") {
					// 	url = "https://docs.google.com/viewerng/viewer?url=" + this.doc.doc.file + ".txt";
					// } else {
					// 	url = "https://docs.google.com/viewerng/viewer?url=" + this.doc.doc.file;  
					// }
					url = "https://docs.google.com/viewerng/viewer?url=" + this.doc.doc.file;  
				} else {
					url = this.doc.doc.file;
				}
				window.open(url, "_blank");
			} catch (e){
				this.error = 'Ошибка. Что-то пошло не так.';
			}
		},
		viewSign(){
			if (this.error == "") {
				this.error = this.doc.doc.signature;
			} else {
				this.error = "";
			}
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
				this.error = '';
			})
			.catch(err => {
				this.error = 'Ошибка. Что-то пошло не так.';
			});
		},
		downloadSign(){
			console.log('downloadSign')
		},
		editDoc(){
			console.log('editDoc')

		},
		confirmCode(){
			// функция отправки кода подтверждения
			this.confirmFromApp = "1234";
			this.isConfirm = true;
		},
		addSignature(){
			if (this.confirm == this.confirmFromApp) {
				this.errorConfirm = 'Ставим подпись...'
				this.$store.dispatch(DOC_SIGNATURE, this.id)
				.then(resp => {
					this.doc.status = 3;
					this.isConfirm = false;
					this.error = 'Подпись успешно поставлена!'
					this.confirmFromApp = '';
					this.confirm = '';
					this.$store.dispatch(DOCS_REQUEST);
				})
				.catch(err=>{
					console.log(err)
					this.error = 'Ошибка. Что-то пошло не так.'
				})
			} else {
				this.errorConfirm = 'Неправильный код подтверждения.';
			}
		},
		repeatSignatures(){
			console.log('repeatSignatures')
		},
		async deleteDoc(){
			let res = await confirm('Вы уверены, что хотите удалить документ?', { title: 'Подтверждение' });
			if (res) {
				this.$store.dispatch(DOC_DELETE, this.id)
				.then(resp => {
					this.$router.push('/documents/all');
				})
				.catch(err=>{
					console.log(err)
					this.error = 'Ошибка. Что-то пошло не так.'
				})
			}
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
.document .confirmButtons{
	display: grid;
    grid-template-columns: 1fr auto auto 1fr;
}
.document .confirmButtons button{
	margin: 10px;
	margin-top: 25px;
}
.document a{
	color: white;
	text-decoration: none;
}
.document button:hover, .document .button:hover{
	cursor: pointer;
}
/* Подтверждение */
.document .confirm{
	position: fixed;
	top: 20%;
	left: calc(50% - 200px);
	margin: 0;
	width: 400px;
	background: rgb(223, 243, 253);
}
.document .notAddHeight{
	height: 240px;
}
.document .addHeight{
	height: 300px;
}
.document .confirm p{
	padding: 20px;
	padding-bottom: 10px;
}
.document .code{
	border: 0;
	margin: 0 auto;
	margin-left: 20px;
	margin-right: 20px;
    padding: 10px;
    font-size: 13.5px;
    width: calc(100% - 60px);
    background: white;
	color: black;
}
</style>