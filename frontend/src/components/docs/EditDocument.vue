<template>
	<div id="editDocument">
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
				<p>Приставка к регистрационному номеру</p>
				<select v-model="reg">
					<option v-for="(regC,i) in regs" :key="i" :value="regC">{{regC.name}}</option>
				</select>
				<p>Картотека</p>
				<select v-model="file_cabinet">
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
import { 
	DOC_EDIT, 
	DOC_UPDATE, 
	DOCS_REQUEST,
	DOCS_REGS,
} from '../../store/mutation-types';
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
			regs: [],
			reg: '',
			fileCabinets: [],
            file_cabinet: '',
        }
	},
	created() {
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
		this.fileCabinets = this.$store.getters.getFileCabinets;
		this.file_cabinet = this.doc.doc.file_cabinet;
		this.$store.dispatch(DOCS_REGS);
		this.regs = this.$store.getters.getRegs;
		this.reg = this.doc.doc.reg;
	},
	methods: {
		editDoc(){
			let d = {
				id: this.id,
				title: this.title + '.' + this.type,
				description: this.description,
				common: this.common,
				file_cabinet_id: this.file_cabinet.id,
				reg_id: this.reg.id
			};
			this.$store.dispatch(DOC_EDIT, d)
			.then(resp => {
				this.$router.push('/document/' + this.id);
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
#editDocument{
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
a{
	color: white;
	text-decoration: none;
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