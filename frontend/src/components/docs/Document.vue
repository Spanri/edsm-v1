<template>
	<div id="document">
		<div v-if="refresh">
			<h3>Загружается...</h3>
			<svg id="Layer_1" width="80px" style="enable-background:new 0 0 30 30;" version="1.1" viewBox="0 0 30 30" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
				<path style="fill:#41A6F9;" d="M15,4C8.9,4,4,8.9,4,15s4.9,11,11,11s11-4.9,11-11S21.1,4,15,4z M21.7,16.8c-0.1,0.4-0.5,0.6-0.9,0.5l-5.6-1.1  c-0.2,0-0.4-0.2-0.6-0.3C14.2,15.7,14,15.4,14,15c0,0,0,0,0,0l0.2-8c0-0.5,0.4-0.8,0.8-0.8c0.4,0,0.8,0.4,0.8,0.8l0.1,6.9l5.2,1.8  C21.6,15.8,21.8,16.3,21.7,16.8z"/>
			</svg>
		</div>
		<div v-else>
			<div class="buttons">				
				<button v-if="doc.status == 0 && doc.user.id == this.$store.getters.getProfile.id" @click="editDoc()">РЕДАКТИРОВАТЬ ИНФОРМАЦИЮ О ФАЙЛЕ</button>
				<button v-if="doc.status == 0 && doc.user.id == this.$store.getters.getProfile.id" @click="isRepeatSign=true">ИЗМЕНИТЬ ФАЙЛ/ПЕРЕЗАПУСТИТЬ ЦЕПОЧКУ ПОДПИСЕЙ</button>
			</div>
			<div class="document2Colon">
				<div>
					<preview :typeFile="type"></preview>
					<button style="margin-top:20px;margin-left:6px;background: rgb(243, 92, 92);" v-if="this.$store.getters.getProfile.is_staff || (doc.status == 0 && (doc.doc.common != true || doc.user.id == this.$store.getters.getProfile.id))" @click="deleteDoc()">УДАЛИТЬ</button>
				</div>
				<div style="margin-left:25px;margin-top:0px;">
					<h3 class="header">
						{{title}}
						<svg v-if="doc.doc.common" width="20px" fill="#347090" style="margin-left:5px;" enable-background="new 0 0 24 24" id="Layer_1" version="1.0" viewBox="0 0 24 24" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
							<title>Общий доступ</title>
							<g><path d="M9,9c0-1.7,1.3-3,3-3s3,1.3,3,3c0,1.7-1.3,3-3,3S9,10.7,9,9z M12,14c-4.6,0-6,3.3-6,3.3V19h12v-1.7C18,17.3,16.6,14,12,14z   "/></g><g><g><circle cx="18.5" cy="8.5" r="2.5"/></g><g><path d="M18.5,13c-1.2,0-2.1,0.3-2.8,0.8c2.3,1.1,3.2,3,3.2,3.2l0,0.1H23v-1.3C23,15.7,21.9,13,18.5,13z"/></g></g><g><g><circle cx="18.5" cy="8.5" r="2.5"/></g><g><path d="M18.5,13c-1.2,0-2.1,0.3-2.8,0.8c2.3,1.1,3.2,3,3.2,3.2l0,0.1H23v-1.3C23,15.7,21.9,13,18.5,13z"/>
							</g></g><g><g><circle cx="5.5" cy="8.5" r="2.5"/></g><g><path d="M5.5,13c1.2,0,2.1,0.3,2.8,0.8c-2.3,1.1-3.2,3-3.2,3.2l0,0.1H1v-1.3C1,15.7,2.1,13,5.5,13z"/></g></g>
						</svg>
					</h3>
					<p v-if="doc.doc.cancel_description" style="color: red">
						Ваш документ отказались подписывать. Посмотрите комментарий отказа и 
						нажмите кнопку "Запустить цепочку подписей снова". Выберите в появившемся 
						окне новый документ (необязательно) и нажмите "Подтвердить", чтобы запустить 
						цепочку подписей.
					</p>
					<p v-if="doc.doc.cancel_description">Комментарий отказа: {{doc.doc.cancel_description}}</p>
					<p v-if="error" style="color: red">{{error}}</p>
					<table class="aboutDoc">
						<thead><tr><th></th><th></th></tr></thead>
						<tbody>
							<tr>
								<td>Регистрационный номер</td>
								<td>{{doc.reg}}</td>
							</tr>
							<tr>
								<td>Владелец</td>
								<td>{{doc.user.profile.full_name}} ({{doc.user.email}})</td>
							</tr>
							<tr>
								<td>Картотека</td>
								<td>{{doc.doc.file_cabinet.name}}</td>
							</tr>
							<tr>
								<td>Дата добавления</td>
								<td>{{doc.doc.date}}</td>
							</tr>
							<tr>
								<td>Описание</td>
								<td>{{ doc.doc.description }}</td>
							</tr>
							<tr>
								<td>Размер файла</td>
								<td>{{Math.round(doc.doc.size/1024/1024 * 1000) / 1000}} Мб</td>
							</tr>
							<tr>
								<td>Файл</td>
								<td>
									<button v-if="doc.doc.size/1024/1024 < 25" @click="viewDoc()">СМОТРЕТЬ</button>
									<button @click="download()">СКАЧАТЬ</button>
								</td>
							</tr>
							<tr>
								<td>Подпись</td>
								<td>
									<button @click="checkSign()">ПРОВЕРИТЬ НА ДОСТОВЕРНОСТЬ</button>
									<button @click="downloadSign()">СКАЧАТЬ ПОДПИСЬ</button>
									<button v-if="doc.status == 2" @click="isConfirm = true">ПОДПИСАТЬ/ОТКЛОНИТЬ</button>
									<br>
									{{doc.doc.signature}}
								</td>
							</tr>
						</tbody>
					</table>
					<div v-if="checkSignature" class="checkSignature">
						<p>{{checkSignatureResult}}</p>
						<div class="confirmButtons">
							<div></div>
							<button @click="checkSignature=false;checkSignatureResult=''">ОК</button>
							<div></div>
						</div>
					</div>
					<div v-if="isConfirm" class="confirm">
						<div style="display: grid;grid-template-columns: auto max-content;">
							<div></div>
							<svg @click="isConfirm = false" style="margin-right: 10px;cursor: pointer;margin-top: 7px;" height="22px" viewBox="0 0 33 33" width="22px" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
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
							<button @click="addSignature()">ПОСТАВИТЬ ПОДПИСЬ</button>
							<br>
						</div>
						<p v-if="errorAddSign" style="color: red;text-align: center;padding: 5px;width:100%">{{errorAddSign}}</p>
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
					<div v-if="isRepeatSign" class="confirm">
						<div style="display: grid;grid-template-columns: auto max-content;">
							<div></div>
							<svg @click="isRepeatSign = false;fileRepeat='';titleRepeatFile=''" style="margin-right: 10px;cursor: pointer;margin-top: 7px;" height="22px" viewBox="0 0 33 33" width="22px" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
								<g id="Cancel" stroke="black" stroke-width="1">
									<path clip-rule="evenodd" d="M16,0C7.163,0,0,7.163,0,16c0,8.836,7.163,16,16,16   c8.836,0,16-7.163,16-16C32,7.163,24.836,0,16,0z M16,30C8.268,30,2,23.732,2,16C2,8.268,8.268,2,16,2s14,6.268,14,14   C30,23.732,23.732,30,16,30z" 
										fill="#121313" fill-rule="evenodd"/>
									<path clip-rule="evenodd" d="M22.729,21.271l-5.268-5.269l5.238-5.195   c0.395-0.391,0.395-1.024,0-1.414c-0.394-0.39-1.034-0.39-1.428,0l-5.231,5.188l-5.309-5.31c-0.394-0.396-1.034-0.396-1.428,0   c-0.394,0.395-0.394,1.037,0,1.432l5.301,5.302l-5.331,5.287c-0.394,0.391-0.394,1.024,0,1.414c0.394,0.391,1.034,0.391,1.429,0   l5.324-5.28l5.276,5.276c0.394,0.396,1.034,0.396,1.428,0C23.123,22.308,23.123,21.667,22.729,21.271z" 
										fill="#121313" fill-rule="evenodd"/>
								</g>
							</svg>
						</div>
						<p style="margin:0">
							Загрузите новый файл (необязательно) и нажмите "ПЕРЕЗАПУСТИТЬ".
						</p>
						<input 
							type="file"
							id="file"
							name="file"
							class="cancelFile"
							@change="onFileChangeRepeat">
						<input 
							v-if="titleRepeatFile"
							type="text"
							v-model="titleRepeatFile" 
							placeholder="Имя файла"
							style="margin-top:15px"
							class="code">
						<p style="padding-top:0;padding-bottom:0;">{{repeatP}}</p>
						<div class="confirmButtons">
							<div></div>
							<button @click="repeatSignatures()">ПЕРЕЗАПУСТИТЬ</button>
							<div></div>
						</div>
					</div>
				</div>
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
	DOC_SIGNATURE_CHECK,
	DOC_SIGNATURE_CANCEL,
	DOC_SIGNATURE_AGAIN,
	DOC_DELETE, 
	DOC_DOWNLOAD,
	DOC_DOWNLOAD_SIGN,
	path
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
			doc: {
				status: '',
				user: {
					profile: {
						full_name: ''
					}
				},
				doc: {
					id: '',
					title: '',
					size: '',
					file_cabinet: {
						name: ''
					},
					common: '',
					description: '',
					date: '',
					signature: '',
				}
			},
			title: '',
			type: '',
			fileWithSignature: 'ddd',
			fileRepeat: '',
			error: '',
			errorConfirm: '',
			errorAddSign: '',
			isConfirm: false,
			isCancelSign: false,
			isRepeatSign: false,
			titleRepeatFile: '',
			typeRepeatFile: '',
			checkSignature: false,
			checkSignatureResult: '',
			confirm: '',
			confirmFromApp: '',
			cancelCause: '',
			cancelFile: '',
			refresh: '',
			repeatP: '',
        }
	},
	created() {
		this.refresh = true;
		this.$store.dispatch(DOCS_REQUEST)
		.then(s => {
			if (!this.$store.getters.getDoc(this.id)) {
				this.$router.push('/404');
				return;
			}
			this.doc = this.$store.getters.getDoc(this.id);
			let typeFile = this.doc.doc.title.split('.');
			this.type = typeFile[typeFile.length-1];
			this.title = this.doc.doc.title.replace("." + this.type, "");
			this.type = this.type.toLowerCase();
			this.refresh = false;
		})
	},
	methods: {
		viewDoc() {
			try{
				this.error = "Открывается..."
				this.$store.dispatch(DOC_DOWNLOAD, this.doc.doc.id)
				.then((response) => {
					let url = '';
					let path2 = path + '/' + response.file;
					if(this.type != "jpg" && this.type != "jpeg" && this.type != "png" && this.type != "pdf"){
						url = "https://docs.google.com/viewerng/viewer?url=" + path2;  
					} else {
						url = path2;
					}
					window.open(url, "_blank");
					this.error = "Открылось!";
					setTimeout(() => {
						this.error = '';
					}, 5000);
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
		download(){
			this.error = "Скачивается..."
			let title = this.doc.doc.title
			this.$store.dispatch(DOC_DOWNLOAD, this.doc.doc.id)
			.then((response) => {
				const link = document.createElement('a');
				link.href = path + '/' + response.file;
				link.setAttribute('download', title);
				document.body.appendChild(link);
				link.click();
				this.error = 'Скачано!';
				setTimeout(() => {
					this.error = '';
				}, 5000);
			})
			.catch(err => {
				console.log(err)
				this.error = 'Ошибка. Что-то пошло не так.';
			});
		},
		downloadSign(){
			this.error = "Скачивается..."
			let title = this.doc.doc.title
			this.$store.dispatch(DOC_DOWNLOAD_SIGN, this.doc.doc.id)
			.then((response) => {
				const link = document.createElement('a');
				link.href = path + '/' + response.file;
				link.setAttribute('download', title);
				document.body.appendChild(link);
				link.click();
				this.error = 'Скачано!';
				setTimeout(() => {
					this.error = '';
				}, 5000);
			})
			.catch(err => {
				console.log(err)
				this.error = 'Ошибка. Что-то пошло не так.';
			});
		},
		editDoc(){
			this.$router.push('/document/' + this.id + '/edit');
		},
		confirmCode(){
			// функция отправки кода подтверждения
			this.confirmFromApp = "1234";
			this.isConfirm = true;
			this.isPreConfirm = false;
		},
		cancelSign(){
			this.error = 'Документ отклоняется...'
			let d = {
				cancel_description: this.cancelCause
			}
			if (this.cancelFile) d.cancel_file = this.cancelFile;
			this.$store.dispatch(DOC_SIGNATURE_CANCEL, {
					id: this.id,
					data: d
				})
				.then(resp => {
					this.refresh = true;
					this.$store.dispatch(DOCS_REQUEST)
					.then(r => {
						this.doc = this.$store.getters.getDoc(this.id);
						this.error = 'Документ отклонен. Через несколько секунд вы перейдете на главную страницу.'
						this.isConfirm = false;
						this.confirmFromApp = '';
						this.confirm = '';
						this.refresh = false;
						setTimeout(() => {
							this.error = '';
							this.$router.push('/documents/all');
						}, 5000);
					})
				})
				.catch(err=>{
					console.log(err)
					this.isConfirm = false;
					this.confirm = '';
					this.error = 'Ошибка. Что-то пошло не так.'
				})
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
		onFileChangeRepeat(e) {
			var files = e.target.files || e.dataTransfer.files;
            if (!files.length) return;
            this.fileRepeat = files[0];
			let typeRepeatFile = files[0].name.split('.')
            this.typeRepeatFile = typeRepeatFile[typeRepeatFile.length-1];
            this.titleRepeatFile = files[0].name.replace("." + this.typeRepeatFile, "");
		},
		addSignature(){
			this.errorAddSign = 'Ставим подпись...'
			this.$store.dispatch(DOC_SIGNATURE, {
				id: this.id,
				first: 0
			})
			.then(resp => {
				this.refresh = true;
				this.$store.dispatch(DOCS_REQUEST)
				.then(r => {
					this.doc = this.$store.getters.getDoc(this.id);
					this.error = 'Подпись успешно поставлена!'
					this.isConfirm = false;
					this.confirmFromApp = '';
					this.confirm = '';
					this.errorAddSign = ''
					this.refresh = false;
					setTimeout(() => {
						this.error = '';
					}, 5000);
				})
			})
			.catch(err=>{
				console.log(err)
				this.isConfirm = false;
				this.confirm = '';
				this.error = 'Ошибка. Что-то пошло не так.'
			})
		},
		checkSign(){
			this.error = 'Проверяем...'
			this.$store.dispatch(DOC_SIGNATURE_CHECK, this.id)
			.then(resp => {
				this.checkSignatureResult = resp;
				this.checkSignature = true;
				this.error = ''
			})
		},
		repeatSignatures(){
			this.repeatP = 'Цепочка запускается...'
			// для файла
			let d = '';
            if (this.fileRepeat) { 
				d = new FormData();  
                const newFile = new File(
                    [this.fileRepeat],
                    this.titleRepeatFile+'.'+this.typeRepeatFile,
                    {type: this.fileRepeat.type}
                );             
                d.append('file', newFile);
				d.append('size', this.fileRepeat.size);
				d.append('title', this.titleRepeatFile+'.'+this.typeRepeatFile);
			}
			this.$store.dispatch(DOC_SIGNATURE_AGAIN, {
				data: d,
				id: this.id
			})
				.then(resp => {
					this.refresh = true;
					this.$store.dispatch(DOCS_REQUEST)
					.then(r => {
						this.doc = this.$store.getters.getDoc(this.id);
						this.repeatP = '';
						this.fileRepeat = '';
						this.titleRepeatFile = '';
						this.typeRepeatFile = '';
						this.error = 'Цепочка запущена снова.'
						this.isRepeatSign = false;
						this.refresh = false;
						setTimeout(() => {
							this.error = '';
						}, 5000);
					})
				})
				.catch(err=>{
					console.log(err);
					this.isConfirm = false;
					this.confirm = '';
					this.error = 'Ошибка. Что-то пошло не так.'
				})
		},
		async deleteDoc(){
			let res = await confirm(
				'Вы уверены, что хотите удалить документ?\n'+
				'Примечание: если вы запретите создание этого окна в настройках браузера, вы не сможете удалить документ.', 
				{ title: 'Подтверждение' }
			)
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
#document{
    height: calc(100% - 50px);
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
button{
    margin-top: 5px;
    margin-bottom: 10px;
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
/* Подтверждение */
.confirm, .checkSignature{
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
.confirm p, .checkSignature p{
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
.aboutDoc *{
	max-width: 500px;
	word-wrap: break-word;
}
table, tr{
    border: white 7px solid;
	border-left: 0;
	border-right: 0;
    border-radius: 5px;
}
td{
    padding: 7px 15px;
	background: #d5dbdf;
}
</style>