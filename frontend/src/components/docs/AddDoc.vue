<template>
	<div class="addDoc">
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
                    <p style="padding-bottom:10px">Запросить подпись: (не забудьте после выбора в выпадающем меню нажать кнопку "Добавить")</p>
                    <div>
                        <div v-for="(user) in selectedUsers" :key="user.full_name" style="margin-bottom: 15px">
                            {{user.full_name}} - {{user.profile.position}}
                            <a class="deleteSelectedUser" @click="deleteSelectedUser(1, user)">x</a>
                            </div>
                        <select v-model="selectedUser">
                            <option v-for="(user) in users" :key="user.email" :value="user">{{user.full_name}} - {{user.profile.position}}</option>
                        </select>
                        <button type="button" @click="addUser(1)">ДОБАВИТЬ</button> <br>
                    </div>
                    <p style="padding-bottom:10px">Пользователи, у которых были запрошены подписи, могут просматривать документ. 
                        Добавить дополнительных пользователей, которые не должны подписывать документ, но могут его просматривать:</p>
                    <div>
                        <div v-for="(user) in selectedUsers2" :key="user.full_name" style="margin-bottom: 15px">
                            {{user.full_name}} - {{user.profile.position}}
                            <a class="deleteSelectedUser" @click="deleteSelectedUser(2, user)">x</a>
                            </div>
                        <select v-model="selectedUser2">
                            <option v-for="(user) in users" :key="user.email" :value="user">{{user.full_name}} - {{user.profile.position}}</option>
                        </select>

                        <button type="button" @click="addUser(2)">ДОБАВИТЬ</button> <br>
                    </div>
                    <div style="height:15px;"></div>
                    <p>Описание</p>
                    <textarea
                        v-model="description" 
                        placeholder="Опишите документ"
                        class="search-box"
                    ></textarea>
                    <p></p> Общий доступ <input class="checkbox" type="checkbox" name="common" true-value="1"  false-value="0" v-model="common">
                    <p></p> Подписать <input class="checkbox" type="checkbox" name="selfSignature" true-value="1"  false-value="0" v-model="selfSignature">
                    <div style="height:35px;"></div>
                    <button type="submit" :class="{disabled: this.disable}">СОЗДАТЬ</button> <br>
                </form>
                <p v-if="error" style="color: red"> {{ error }} </p>
            </div>
        </div>
	</div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import axios from 'axios'
import { DOC_UPLOAD, DOC_REQUEST, DOCS_REQUEST, USERS_REQUEST } from '../../store/mutation-types';
import Preview from '../addit/Preview';

export default {
    name: 'account',
    components: { Preview },
    data () {
		return {
            title: '',
            typeFile: false,
            description: '',
            selectedUser: '',
            selectedUsers: [],
            selectedUser2: '',
            selectedUsers2: [],
            users: [],
            common: 0,
            selfSignature: 0,
            error: null,
            file:'',
            disable: false
		}
    },
    created(){
        this.$store.dispatch(USERS_REQUEST)
        .then(resp=>{
            this.users = resp.filter(r => r.id != this.$store.getters.getProfile.id)
        })
    },
    methods: {
        onFileChange(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length) return;
            this.file = files[0];
            /* Расширение файла */
            let typeFile = files[0].name.split('.')
            this.typeFile = typeFile[typeFile.length-1];
            this.title = files[0].name.replace("." + this.typeFile, "");
            this.file = files[0];
            // console.log(files[0].size/1024/1024 + " мб")
        },
        blobToFile(theBlob, fileName) {
            //A Blob() is almost a File() - it's just missing the two properties below which we will add
            theBlob.lastModifiedDate = new Date();
            theBlob.name = fileName;
            return theBlob;
        },
        /* Конвертирование файла в картинку для превью */
        // dataURItoBlob(dataURI) {
        //     var byteString = atob(dataURI);
        //     var ab = new ArrayBuffer(byteString.length);
        //     var ia = new Uint8Array(ab);
        //     for (var i = 0; i < byteString.length; i++) {
        //         ia[i] = byteString.charCodeAt(i);
        //     }
        //     return new Blob([ab], {type: 'image/png'});
        // },
        addUser(num){
            if (num == 1){
                const {selectedUser} = this;
                this.selectedUsers.push(selectedUser);
                this.users = this.users.filter(function(el){
                    return el != selectedUser;
                });
            } else if(num == 2) {
                const {selectedUser2} = this;
                this.selectedUsers2.push(selectedUser2);
                this.users = this.users.filter(function(el){
                    return el != selectedUser2;
                });
            }
        },
        deleteSelectedUser(i, item){
            if(i==1){
                this.selectedUsers = this.selectedUsers.filter(function(el){
                    return el != item;
                });
            } else if(i==2){
                this.selectedUsers2 = this.selectedUsers2.filter(function(el){
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
                console.log(this.file.size)
                d.append('size', this.file.size);
            }
            d.append('user_id', this.$store.getters.getProfile.id);
            if (this.title) d.append('title', this.title+'.'+this.typeFile);
            if (this.description) d.append('description', this.description);
            d.common = this.common ? d.append('common', true) : d.append('common', false);
            let dd = { d }
            if (this.selectedUsers) dd.signature_request = this.selectedUsers;
            if (this.selectedUsers2) dd.show_request = this.selectedUsers2;
            dd.selfSignature = this.selfSignature;
            // ДОДЕЛАТЬ С ПОДПИСЬЮ САМОГО ПОЛЬЗОВАТЕЛЯ selfSignature
            this.$store.dispatch(DOC_UPLOAD, dd)
			.then((resp) => {
                this.$store.dispatch(DOCS_REQUEST)
                .then(res => {
                    this.error = "Загружено!"
                    this.$router.push({
                        name: 'document',
                        params: { id: resp.id }
                    })
                })
                .catch(e => {
                    console.log(e)
                })
            })
        },
    }
}
</script>

<style>
.addDoc{
    height: 100%;
	width: 100%;
    max-width: 900px;
    margin: 0 auto;
	background: white;
    padding: 25px;
}
.addDoc .header{
    margin-top: 0;
	margin-bottom: 30px;
}
/* Поля ввода */
.addDoc .filename, .addDoc textarea{
	border: 0;
	margin: 0 auto;
    padding: 10px;
    font-size: 13.5px;
    min-width: 350px;
    background: rgb(223, 243, 253);
}
.addDoc select{
    margin-right: 10px;
    padding: 6px;
    font-size: 13.5px;
    min-width: 250px;
}
/* Кнопки ЗАГРУЗИТЬ и СОЗДАТЬ */
.addDoc button, .addDoc input[type="submit"] [type]:not([type="checkbox"]), .fileContainer{
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
.addDoc button:hover, .addDoc a:hover{
    cursor: pointer;
}
/**/
.addDoc form > p{
    margin-bottom: 5px;
}
/**/
.addDoc2Colon{
    display: grid;
    grid-template-columns: max-content auto;
}
/**/
.addDoc img{
    width: 110px;
}
/**/
.addDoc .deleteSelectedUser{
    border: 0;
	border-radius: 5px;
	padding: 3px;
    padding: 5px;
    padding-top: 2px;
	color: white;
	background-color: #347090;
}
/**/
.addDoc input[type="checkbox"]{
    height: 15px;
}
/**/
.addDoc .disabled{
    pointer-events: none;
    background: rgb(133, 133, 133) !important;
}
</style>