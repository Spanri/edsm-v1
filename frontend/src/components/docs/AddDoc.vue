<template>
	<div id="addDoc">
		<h3 class="header">ДОБАВЛЕНИЕ ДОКУМЕНТА</h3>
        <div class="addDoc2Colon">
            <div class="img">
                <preview v-if="typeFile" :typeFile="typeFile"></preview>
                <img v-else :src="'https://img.icons8.com/wired/512/000000/document.png'">
            </div>
            <div style="margin-left:25px">
                <form @submit.prevent="addDoc">
                    <input 
                        type="file"
                        id="file"
                        name="file"
                        @change="onFileChange">
                    <p>Имя файла</p>
                    <input
                        required
                        v-model="title"
                        type="text"
                        placeholder="Введите имя"
                        autocomplete = usernameNew
                        class="filename"
                    />
                    <p>Приставка к регистрационному номеру</p>
                    <select v-model="reg">
                        <option v-for="(regC,i) in regs" :key="i" :value="regC">{{regC.name}}</option>
                    </select>
                    <p>Картотека</p>
                    <select v-model="file_cabinet">
                        <option v-for="(fileC,i) in fileCabinets" :key="i" :value="fileC">{{fileC.name}}</option>
                    </select>
                    <div style="border: 1px solid #347090;border-radius:3px;padding:15px;margin-top:10px">
                        <p style="margin-top:0px">Запросить подпись. Порядок выбранных пользователей можно менять перетаскиванием.</p>
                        <draggable v-model="selectedUsers">
                            <div v-for="user in selectedUsers" :key="user.id" class="selectedUserWithCancel">
                                <p class="selectedUser">{{user.full_name}} - {{user.position}}</p>
                                <svg class="deleteSelectedUser" @click="deleteSelectedUser(1, user)" height="21px" viewBox="0 0 31 32" width="22px" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                                    <g id="Cancel" stroke="#347090" stroke-width="1">
                                        <path clip-rule="evenodd" d="M16,0C7.163,0,0,7.163,0,16c0,8.836,7.163,16,16,16   c8.836,0,16-7.163,16-16C32,7.163,24.836,0,16,0z M16,30C8.268,30,2,23.732,2,16C2,8.268,8.268,2,16,2s14,6.268,14,14   C30,23.732,23.732,30,16,30z" 
                                            fill="#121313" fill-rule="evenodd"/>
                                        <path clip-rule="evenodd" d="M22.729,21.271l-5.268-5.269l5.238-5.195   c0.395-0.391,0.395-1.024,0-1.414c-0.394-0.39-1.034-0.39-1.428,0l-5.231,5.188l-5.309-5.31c-0.394-0.396-1.034-0.396-1.428,0   c-0.394,0.395-0.394,1.037,0,1.432l5.301,5.302l-5.331,5.287c-0.394,0.391-0.394,1.024,0,1.414c0.394,0.391,1.034,0.391,1.429,0   l5.324-5.28l5.276,5.276c0.394,0.396,1.034,0.396,1.428,0C23.123,22.308,23.123,21.667,22.729,21.271z" 
                                            fill="#121313" fill-rule="evenodd"/>
                                    </g>
                                </svg>
                            </div>
                        </draggable>
                        <select v-model="selectedUser">
                            <option v-for="(user) in users" :key="user.id" :value="user">{{user.full_name}} - {{user.position}}</option>
                        </select>
                        <button type="button" @click="addUser(1)">ДОБАВИТЬ</button> <br>
                    </div>
                    <div style="border: 1px solid #347090;border-radius:3px;padding:15px;margin-top:10px">
                        <p style="margin-top:0">
                            Пользователи, у которых были запрошены подписи, могут просматривать документ. 
                            Ниже можно указать дополнительных пользователей, которые не должны подписывать документ, 
                            но могут его просматривать. Порядок выбранных пользователей можно менять перетаскиванием.
                        </p>
                        <draggable v-model="selectedUsers2">
                            <div v-for="user in selectedUsers2" :key="user.id" class="selectedUserWithCancel">
                                <p class="selectedUser">{{user.full_name}} - {{user.position}}</p>
                                <svg class="deleteSelectedUser" @click="deleteSelectedUser(2, user)" height="21px" viewBox="0 0 31 32" width="22px" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                                    <g id="Cancel" stroke="#347090" stroke-width="1">
                                        <path clip-rule="evenodd" d="M16,0C7.163,0,0,7.163,0,16c0,8.836,7.163,16,16,16   c8.836,0,16-7.163,16-16C32,7.163,24.836,0,16,0z M16,30C8.268,30,2,23.732,2,16C2,8.268,8.268,2,16,2s14,6.268,14,14   C30,23.732,23.732,30,16,30z" 
                                            fill="#121313" fill-rule="evenodd"/>
                                        <path clip-rule="evenodd" d="M22.729,21.271l-5.268-5.269l5.238-5.195   c0.395-0.391,0.395-1.024,0-1.414c-0.394-0.39-1.034-0.39-1.428,0l-5.231,5.188l-5.309-5.31c-0.394-0.396-1.034-0.396-1.428,0   c-0.394,0.395-0.394,1.037,0,1.432l5.301,5.302l-5.331,5.287c-0.394,0.391-0.394,1.024,0,1.414c0.394,0.391,1.034,0.391,1.429,0   l5.324-5.28l5.276,5.276c0.394,0.396,1.034,0.396,1.428,0C23.123,22.308,23.123,21.667,22.729,21.271z" 
                                            fill="#121313" fill-rule="evenodd"/>
                                    </g>
                                </svg>
                            </div>
                        </draggable>
                        <select v-model="selectedUser2">
                            <option v-for="(user) in users" :key="user.id" :value="user">{{user.full_name}} - {{user.position}}</option>
                        </select>
                        <button type="button" @click="addUser(2)">ДОБАВИТЬ</button> <br>
                    </div>
                    <div style="height:15px;"></div>
                    <p>Описание</p>
                    <textarea
                        v-model="description" 
                        placeholder="Опишите документ"
                    ></textarea>
                    <p></p> Общий доступ <input type="checkbox" name="common" true-value="1"  false-value="0" v-model="common">
                    <div style="height:35px;"></div>
                    <button type="submit" :class="{disabled: this.disable}" style="margin-bottom:50px;">СОЗДАТЬ</button> <br>
                </form>
                <p v-if="error" style="color: red"> {{ error }} </p>
            </div>
        </div>
	</div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import axios from 'axios'
import { DOC_UPLOAD, DOC_UPDATE, USERS_EMAILS, DOCS_REGS } from '../../store/mutation-types';
import Preview from '../addit/Preview';
import draggable from 'vuedraggable'

export default {
    name: 'account',
    components: { Preview, draggable, },
    data () {
		return {
            title: '',
            typeFile: false,
            description: '',
            selectedUser: '',
            selectedUsers: [],
            selectedUser2: '',
            selectedUsers2: [],
            selectedUsers20: [],
            users: [],
            common: 0,
            selfSignature: 0,
            error: null,
            file:'',
            disable: true,
            reg: '',
            fileCabinets: [],
            file_cabinet: '',
		}
    },
    created(){
        this.$store.dispatch(USERS_EMAILS)
        .then(resp=>{
            this.users = resp.filter(r => r.id != this.$store.getters.getProfile.id)
        })
        this.fileCabinets = this.$store.getters.getFileCabinets;
        this.file_cabinet = this.$store.getters.getFileCabinet;
        this.$store.dispatch(DOCS_REGS)
    },
    computed: {
        regs(){
            return this.$store.getters.getRegs;
        },
    },
    methods: {
        onFileChange(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length) return;
            this.file = files[0];
            let typeFile = files[0].name.split('.')
            this.typeFile = typeFile[typeFile.length-1];
            this.title = files[0].name.replace("." + this.typeFile, "");
            this.file = files[0];
            this.disable = false;
        },
        blobToFile(theBlob, fileName) {
            theBlob.lastModifiedDate = new Date();
            theBlob.name = fileName;
            return theBlob;
        },
        addUser(num){
            if (num == 1){
                if(this.selectedUser != '') {
                    this.selectedUsers.push(this.selectedUser);
                    this.users = this.users.filter(el => {
                        return el != this.selectedUser;
                    });
                    this.selectedUser = '';
                }
            } else if(num == 2) {
                if(this.selectedUser2 != '') {
                    this.selectedUsers2.push(this.selectedUser2);
                    this.users = this.users.filter(el => {
                        return el != this.selectedUser2;
                    });
                    this.selectedUser2 = '';
                }
            }
        },
        deleteSelectedUser(i, item){
            if(i==1){
                this.selectedUsers = this.selectedUsers.filter(el => {
                    return el != item;
                });
            } else if(i==2){
                this.selectedUsers2 = this.selectedUsers2.filter(el => {
                    return el != item;
                });
            }
            this.users.push(item);
        },
        addDoc(){
            this.disable = true;
            this.error = "Загружается..."
            var d = new FormData();
            // для файла
            if (this.file) {   
                const newFile = new File(
                    [this.file],
                    this.title+'.'+this.typeFile,
                    {type: this.file.type}
                );          
                d.append('file', newFile);
                d.append('size', this.file.size);
            }
            d.append('user_id', this.$store.getters.getProfile.id);
            if (this.title) d.append('title', this.title+'.'+this.typeFile);
            if (this.description) d.append('description', this.description);
            if (this.file_cabinet) d.append('file_cabinet_id', this.file_cabinet.id);
            if (this.reg) d.append('reg_id', this.reg.id);
            d.common = this.common ? d.append('common', true) : d.append('common', false);
            let dd = { d }
            if (this.selectedUsers) dd.signature_request = this.selectedUsers;
            if (this.selectedUsers2) dd.show_request = this.selectedUsers2;
            dd.selfSignature = this.selfSignature;
            this.$store.dispatch(DOC_UPLOAD, dd)
			.then((resp) => {
                this.error = "Загружено!"
                this.$router.push({
                    name: 'document',
                    params: { id: resp.doc.id.toString() }
                })
            })
            .catch(e => {
                console.log(e)
                this.disable = false;
				this.error = 'Ошибка. Что-то пошло не так.';
			})
        },
    }
}
</script>

<style scoped>
#addDoc{
    height: 100%;
	width: 100%;
    max-width: 900px;
    margin: 0 auto;
	background: white;
    padding: 25px;
    padding-bottom: 0;
}
.header{
    margin-top: 0;
	margin-bottom: 30px;
}
/* Поля ввода */
.filename, textarea{
	border: 0;
	margin: 0 auto;
    padding: 10px;
    font-size: 13.5px;
    min-width: 900px;
    max-width: 900px;
    background: rgb(223, 243, 253);
}
select{
    margin-right: 10px;
    padding: 6px;
    font-size: 13.5px;
    min-width: 250px;
}
.selectedUser{
    display:inline-block;
    margin: 0;
    padding:0;
    vertical-align:top;
    font-weight: 400;
}
.selectedUserWithCancel{
    background: rgb(223, 243, 253);
    margin-top: 10px;
    margin-bottom: 10px;
    padding: 5px;
    display: grid;
    grid-template-columns: 1fr auto;
    grid-template-rows: auto;
}
.selectedUserWithCancel:hover{
    background: rgb(223, 243, 253);
    cursor: pointer;
}
.deleteSelectedUser{
    padding: 0px;
    padding-left: 5px;
}
/**/
form > p{
    margin-bottom: 5px;
}
/**/
.addDoc2Colon{
    display: grid;
    grid-template-columns: max-content auto;
}
/**/
img{
    width: 110px;
}
/**/

/**/
.disabled{
    pointer-events: none;
    background: rgb(133, 133, 133);
}
</style>