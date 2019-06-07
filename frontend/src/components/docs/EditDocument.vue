<template>
	<div class="editDocument">
		<div class="document2Colon">
			<div>
				<preview :typeFile="type"></preview>
			</div>
			<form @submit.prevent="editDoc" style="margin-left:25px;margin-top:-15px;">
				<p v-if="error" style="color: red">{{error}}</p>
				<p>Название</p>
				<input
					v-model="title"
					type="text"
					placeholder="Введите название"
					class="code">
				<p>Картотека</p>
				<select v-model="fileCabinet">
					<option v-for="(fileC,i) in fileCabinets" :key="i" :value="fileC">{{fileC.name}}</option>
				</select>
				<p>Описание</p>
				<textarea
					v-model="description" 
					placeholder="Введите описание"
				></textarea>
				<p></p> Общий доступ <input type="checkbox" true-value="true" false-value="false" v-model="common">
				<div style="height:35px;"></div>
				<button type="submit">РЕДАКТИРОВАТЬ</button> <br>
			</form>
		</div>
	</div>
</template>

<script>
// import FileReader from 'vue-filereader'
import { mapState } from 'vuex'
import { DOCS_REQUEST, DOC_EDIT } from '../../store/mutation-types';
import Preview from '../addit/Preview';

import axios from 'axios'

export default {
	name: 'editDocument',
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
			description: '',
			common: false,
			error: '',
			fileCabinets: [],
            fileCabinet: '',
        }
	},
	created() {
		this.$store.dispatch(DOCS_REQUEST)
		if (!this.$store.getters.getDoc(this.id)) {
			this.$router.push('/documents/all');
		}
		this.doc = this.$store.getters.getDoc(this.id);
		let typeFile = this.doc.doc.title.split('.');
		this.type = typeFile[typeFile.length-1];
		this.title = this.doc.doc.title.replace("." + this.type, "");
		this.type = this.type.toLowerCase();
		this.description = this.doc.doc.description;
		this.common = this.doc.doc.common;
		// this.$store.dispatch(USERS_EMAILS)
        // .then(resp=>{
        //     this.users = resp.filter(r => r.id != this.$store.getters.getProfile.id)
        //     console.log(this.users)
        // })
        this.fileCabinets = this.$store.getters.getFileCabinets;
        this.fileCabinet = this.doc.doc.fileCabinet;
	},
	methods: {
		editDoc(){
			let d = {
				id: this.id,
				title: this.title + '.' + this.type,
				description: this.description,
				common: this.common,
				fileCabinet_id: this.fileCabinet.id
			};
			this.$store.dispatch(DOC_EDIT, d)
			.then(resp => {
				this.$store.dispatch(DOCS_REQUEST)
				.then(r => {
					this.$router.push('/document/' + this.id);
				})
				.catch(err => {
					console.log(err)
					this.error = 'Что-то пошло не так.'
				})
			})
			.catch(err => {
				console.log(err)
				this.error = 'Что-то пошло не так.'
			})
		},
	},
}
</script>

<style scoped>
.editDocument{
    height: 100%;
	width: 100%;
    max-width: 900px;
    margin: 0 auto;
	background: white;
    padding: 25px;
}
.header{
    margin-top: 0;
	margin-bottom: 30px;
}
/**/
.document2Colon{
    display: grid;
    grid-template-columns: max-content auto;
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
a{
	color: white;
	text-decoration: none;
}
button:hover, .button:hover{
	cursor: pointer;
}
/* Поля ввода */
input[type="text"]{
	border: 0;
	margin: 0 auto;
    height: 30px;
    padding-left: 15px;
	padding-right: 15px;
    min-width: 350px;
    background: rgb(223, 243, 253);
}
textarea{
	border: 0;
	margin: 0 auto;
    padding: 10px;
    font-size: 13.5px;
    min-width: 350px;
    background: rgb(223, 243, 253);
}
/* Картотека */
select{
    margin-right: 10px;
    padding: 6px;
    font-size: 13.5px;
    min-width: 250px;
}
</style>