<template>
	<div class="document">
		<div class="buttons">
			<button v-if="doc.doc.size/1024/1024 < 25" @click="viewDoc()">СМОТРЕТЬ ДОКУМЕНТ</button>
			<button v-if="doc.doc.size/1024/1024 < 25" @click="viewSign()">СМОТРЕТЬ ПОДПИСЬ (не работает)</button>
			<button @click="download()">СКАЧАТЬ</button>
			<button @click="downloadSign()">СКАЧАТЬ ПОДПИСЬ (не работает)</button>
			<button v-if="doc.status == 0 && doc.user.id == this.$store.getters.getProfile.id" @click="editDoc()">РЕДАКТИРОВАТЬ</button>
			<button v-if="doc.status == 2" @click="isPreConfirm = true">ПОДПИСАТЬ/ОТКЛОНИТЬ</button>
			<button v-if="doc.status == 0 && doc.user.id == this.$store.getters.getProfile.id" @click="repeatSignatures()">ЗАПУСТИТЬ ЦЕПОЧКУ ПОДПИСЕЙ СНОВА (не работает)</button>
		</div>
		<div class="document2Colon">
			<div>
				<preview :typeFile="type"></preview>
				<button style="margin-top:20px;margin-left:6px;background: rgb(243, 92, 92);" v-if="this.$store.getters.getProfile.is_staff || (doc.status == 0 && (doc.doc.common != true || doc.user.id == this.$store.getters.getProfile.id))" @click="deleteDoc()">УДАЛИТЬ</button>
			</div>
			<div style="margin-left:25px;margin-top:0px;">
				<h3 class="header">{{title}}</h3>
				<p v-if="error" style="color: red">{{error}}</p>
				<table class="aboutDoc">
					<thead><tr><th></th><th></th></tr></thead>
					<tbody>
						<tr>
							<td>Регистрационный номер</td>
							<td>{{doc.doc.id}}</td>
						</tr>
						<tr>
							<td>Владелец</td>
							<td>{{doc.user.profile.full_name}} ({{doc.user.email}})</td>
						</tr>
						<tr>
							<td>Картотека</td>
							<td>{{doc.doc.fileCabinet.name}}</td>
						</tr>
						<tr>
							<td>Общий доступ</td>
							<td>{{doc.doc.common ? 'да' : 'нет'}}</td>
						</tr>
						<tr>
							<td>Дата добавления</td>
							<td>{{doc.doc.date}}</td>
						</tr>
						<tr>
							<td>Описание</td>
							<td>{{ doc.doc.description }}</td>
						</tr>
					</tbody>
				</table>
				<div v-if="isPreConfirm" class="confirm">
					<div style="display: grid;grid-template-columns: auto max-content;">
						<div></div>
						<svg @click="isPreConfirm = false" style="margin-right: 10px;cursor: pointer;margin-top: 7px;" height="22px" viewBox="0 0 33 33" width="22px" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
							<g id="Cancel" stroke="black" stroke-width="1">
								<path clip-rule="evenodd" d="M16,0C7.163,0,0,7.163,0,16c0,8.836,7.163,16,16,16   c8.836,0,16-7.163,16-16C32,7.163,24.836,0,16,0z M16,30C8.268,30,2,23.732,2,16C2,8.268,8.268,2,16,2s14,6.268,14,14   C30,23.732,23.732,30,16,30z" 
									fill="#121313" fill-rule="evenodd"/>
								<path clip-rule="evenodd" d="M22.729,21.271l-5.268-5.269l5.238-5.195   c0.395-0.391,0.395-1.024,0-1.414c-0.394-0.39-1.034-0.39-1.428,0l-5.231,5.188l-5.309-5.31c-0.394-0.396-1.034-0.396-1.428,0   c-0.394,0.395-0.394,1.037,0,1.432l5.301,5.302l-5.331,5.287c-0.394,0.391-0.394,1.024,0,1.414c0.394,0.391,1.034,0.391,1.429,0   l5.324-5.28l5.276,5.276c0.394,0.396,1.034,0.396,1.428,0C23.123,22.308,23.123,21.667,22.729,21.271z" 
									fill="#121313" fill-rule="evenodd"/>
							</g>
						</svg>
					</div>
					<p style="margin:0">
						Просмотрите документ с помощью кнопок СМОТРЕТЬ ДОКУМЕНТ (если документ меньше 25мб) 
						или СКАЧАТЬ. Примите решение, поставить подпись или отклонить документ.
					</p>
					<div class="signButtons" style="margin-top:5px;">
						<div></div>
						<button @click="isCancelSign = true;isPreConfirm = false;" style="background: rgb(243, 92, 92)">ОТКЛОНИТЬ</button>
						<button @click="confirmCode()">ПОСТАВИТЬ ПОДПИСЬ</button>
						<div></div>
					</div>
				</div>
				<div v-if="isCancelSign" class="confirm" style="height:380px" @submit.prevent="cancelSign">
					<div style="display: grid;grid-template-columns: auto max-content;">
						<div></div>
						<svg @click="isCancelSign = false;" style="margin-right: 10px;cursor: pointer;margin-top: 7px;" height="22px" viewBox="0 0 33 33" width="22px" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
							<g id="Cancel" stroke="black" stroke-width="1">
								<path clip-rule="evenodd" d="M16,0C7.163,0,0,7.163,0,16c0,8.836,7.163,16,16,16   c8.836,0,16-7.163,16-16C32,7.163,24.836,0,16,0z M16,30C8.268,30,2,23.732,2,16C2,8.268,8.268,2,16,2s14,6.268,14,14   C30,23.732,23.732,30,16,30z" 
									fill="#121313" fill-rule="evenodd"/>
								<path clip-rule="evenodd" d="M22.729,21.271l-5.268-5.269l5.238-5.195   c0.395-0.391,0.395-1.024,0-1.414c-0.394-0.39-1.034-0.39-1.428,0l-5.231,5.188l-5.309-5.31c-0.394-0.396-1.034-0.396-1.428,0   c-0.394,0.395-0.394,1.037,0,1.432l5.301,5.302l-5.331,5.287c-0.394,0.391-0.394,1.024,0,1.414c0.394,0.391,1.034,0.391,1.429,0   l5.324-5.28l5.276,5.276c0.394,0.396,1.034,0.396,1.428,0C23.123,22.308,23.123,21.667,22.729,21.271z" 
									fill="#121313" fill-rule="evenodd"/>
							</g>
						</svg>
					</div>
					<p style="margin-top:0">
						Напишите, почему документ отклонен. Вы также можете загрузить исправленный документ 
						(не обязательно). Тот, кто просил вас поставить подпись, сможет просмотреть ваш 
						вариант документа. 
					</p>
					<textarea
						v-model="cancelCause" 
						placeholder="Введите комментарий"
					></textarea>
					<input 
                        type="file"
                        id="file"
                        name="file"
						class="cancelFile"
                        @change="onFileChangeCancel">
					<div class="confirmButtons">
						<div></div>
						<button @click="cancelSign()">ОТКЛОНИТЬ И ОТПРАВИТЬ КОММЕНТАРИЙ</button>
						<div></div>
					</div>
					<p v-if="errorConfirm" style="color: red;text-align: center;padding: 5px">{{errorConfirm}}</p>
				</div>
				<form v-if="isConfirm" class="confirm" :class="{addHeight: errorConfirm, notAddHeight: !errorConfirm}" @submit.prevent="addSignature">
					<div style="display: grid;grid-template-columns: auto max-content;">
						<div></div>
						<svg @click="isConfirm = false;confirmFromApp = '';confirm = '';" style="margin-right: 10px;cursor: pointer;margin-top: 7px;" height="22px" viewBox="0 0 33 33" width="22px" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
							<g id="Cancel" stroke="black" stroke-width="1">
								<path clip-rule="evenodd" d="M16,0C7.163,0,0,7.163,0,16c0,8.836,7.163,16,16,16   c8.836,0,16-7.163,16-16C32,7.163,24.836,0,16,0z M16,30C8.268,30,2,23.732,2,16C2,8.268,8.268,2,16,2s14,6.268,14,14   C30,23.732,23.732,30,16,30z" 
									fill="#121313" fill-rule="evenodd"/>
								<path clip-rule="evenodd" d="M22.729,21.271l-5.268-5.269l5.238-5.195   c0.395-0.391,0.395-1.024,0-1.414c-0.394-0.39-1.034-0.39-1.428,0l-5.231,5.188l-5.309-5.31c-0.394-0.396-1.034-0.396-1.428,0   c-0.394,0.395-0.394,1.037,0,1.432l5.301,5.302l-5.331,5.287c-0.394,0.391-0.394,1.024,0,1.414c0.394,0.391,1.034,0.391,1.429,0   l5.324-5.28l5.276,5.276c0.394,0.396,1.034,0.396,1.428,0C23.123,22.308,23.123,21.667,22.729,21.271z" 
									fill="#121313" fill-rule="evenodd"/>
							</g>
						</svg>
					</div>
					<p style="margin-top:0">Заглушка - код "1234". На ваше мобильное приложение отправлен код подтверждения. Введите его ниже.</p>
					<input 
                        required
                        v-model="confirm"
                        type="text"
                        placeholder="Введите код подтверждения"
                        class="code">
					<div class="confirmButtons">
						<div></div>
						<button type="submit">ПОДТВЕРДИТЬ</button>
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
import { 
	DOC_UPDATE, 
	DOCS_REQUEST,
	DOC_REQUEST,
	DOC_SIGNATURE, 
	DOC_DELETE, 
	DOC_DOWNLOAD 
} from '../../store/mutation-types';
import Preview from '../addit/Preview';

import axios from 'axios'

export default {
	name: 'document',
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
			isPreConfirm: false,
			isConfirm: false,
			isCancelSign: false,
			confirm: '',
			confirmFromApp: '',
			cancelCause: '',
			cancelFile: '',
        }
	},
	created() {
		if (!this.$store.getters.getDoc(this.id)) {
			this.$router.push('/404');
			return;
		}
		this.doc = this.$store.getters.getDoc(this.id);
		let typeFile = this.doc.doc.title.split('.');
		this.type = typeFile[typeFile.length-1];
		this.title = this.doc.doc.title.replace("." + this.type, "");
		this.type = this.type.toLowerCase();
	},
	methods: {
		viewDoc() {
			try{
				this.error = "Открывается..."
				this.$store.dispatch(DOC_DOWNLOAD, this.doc.doc.id)
				.then((response) => {
					let url = '';
					let path = 'https://edms-mtuci.herokuapp.com/' + response.file;
					if(this.type != "jpg" && this.type != "jpeg" && this.type != "png"){
						url = "https://docs.google.com/viewerng/viewer?url=" + path;  
					} else {
						url = path;
					}
					window.open(url, "_blank");
					this.error = "Открылось!";
					setTimeout(() => {
						this.error = '';
					}, 3000);
				})
				.catch(err => {
					console.log(err)
					this.error = 'Ошибка. Что-то пошло не так.';
				});
			} catch (e){
				console.log(e)
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
			this.$store.dispatch(DOC_DOWNLOAD, this.doc.doc.id)
			.then((response) => {
				// console.log(response)
				// console.log('https://edms-mtuci.herokuapp.com/' + response.file)
				axios({
					url: 'https://edms-mtuci.herokuapp.com/' + response.file,
					method: 'GET',
					responseType: 'blob',
				}).then((resp) => {
					const url = window.URL.createObjectURL(new Blob([resp.data]));
					const link = document.createElement('a');
					link.href = url;
					link.setAttribute('download', title);
					document.body.appendChild(link);
					link.click();
					this.error = 'Скачано!';
					setTimeout(() => {
						this.error = '';
					}, 3000);
				})
				.catch(err => {
					console.log(err)
					this.error = 'Ошибка. Что-то пошло не так.';
				});
			})
			.catch(err => {
				console.log(err)
				this.error = 'Ошибка. Что-то пошло не так.';
			});
		},
		downloadSign(){
			console.log('downloadSign')
		},
		editDoc(){
			this.$router.push('/document/'+this.id+'/edit');
		},
		confirmCode(){
			// функция отправки кода подтверждения
			this.confirmFromApp = "1234";
			this.isConfirm = true;
			this.isPreConfirm = false;
		},
		cancelSign(){
			console.log(this.cancelCause)
		},
		onFileChangeCancel(e) {
            // var files = e.target.files || e.dataTransfer.files;
            // if (!files.length) return;
            // this.file = files[0];
            // /* Расширение файла */
            // let typeFile = files[0].name.split('.')
            // this.typeFile = typeFile[typeFile.length-1];
            // this.title = files[0].name.replace("." + this.typeFile, "");
            // this.file = files[0];
            // this.disable = false;
            // console.log(files[0].size/1024/1024 + " мб")
        },
		addSignature(){
			if (this.confirm == this.confirmFromApp) {
				this.errorConfirm = 'Ставим подпись...'
				this.$store.dispatch(DOC_SIGNATURE, {
					id: this.id,
					first: 0
				})
				.then(resp => {
					this.doc.status = 3;
					this.isConfirm = false;
					this.error = 'Подпись успешно поставлена!'
					this.confirmFromApp = '';
					this.confirm = '';
					this.$store.dispatch(DOCS_REQUEST);
					setTimeout(() => {
						this.error = '';
					}, 3000);
				})
				.catch(err=>{
					console.log(err)
					this.isConfirm = false;
					// this.confirmFromApp = '';
					this.confirm = '';
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

<style scoped>
.document{
    height: 100%;
	width: 100%;
    max-width: 900px;
    margin: 0 auto;
	background: white;
    padding: 25px;
}
.header{
    margin-top: 0;
	margin-bottom: 10px;
}
/**/
.document2Colon{
    display: grid;
    grid-template-columns: max-content auto;
	margin-top: 20px;
}
/**/
button, .button{
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
.buttons{
	max-width: 900px;
}
.signButtons{
	display: grid;
    grid-template-columns: 1fr auto auto 1fr;
}
.signButtons button{
	margin: 10px;
	margin-top: 5px;
	margin-bottom: 20px;
}
.confirmButtons{
	display: grid;
    grid-template-columns: 1fr auto 1fr;
}
.confirmButtons button{
	margin: 10px;
	margin-top: 25px;
}
a{
	color: white;
	text-decoration: none;
}
button:hover, .button:hover{
	cursor: pointer;
}
/* Подтверждение */
.confirm{
	position: fixed;
	top: 20%;
	left: calc(50% - 200px);
	margin: 0;
	width: 400px;
	background: rgb(223, 243, 253);
	border: 1px solid #347090;
}
.notAddHeight{
	height: 240px;
}
.addHeight{
	height: 300px;
}
.confirm p{
	padding: 20px;
	padding-bottom: 10px;
	text-align: justify;
}
.code{
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
/* Причина отклонения, комментарий */
textarea{
	border: 0;
	margin: 0 15px;
    padding: 10px;
    font-size: 13.5px;
    min-width: 350px;
	max-width: 350px;
	min-height: 70px;
	max-height: 70px;
    background: white;
}
/* Файл, который загружается при отклонении подписи*/
.cancelFile{
	margin: 15px;
	margin-bottom: 0;
}
/* Таблица */
table {
    border-collapse: collapse;
}
table, tr{
    border: rgb(223, 243, 253) 2px solid;
	border-left: 0;
	border-right: 0;
    border-radius: 5px;
}
td{
    padding: 7px 15px;
}
</style>