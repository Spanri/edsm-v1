<template>
	<div class="addDoc">
		<h3 class="header">ДОБАВЛЕНИЕ ДОКУМЕНТА</h3>
        <div class="addDoc2Colon">
            <div>
                <div @click="bigImage = 1">
                    <img :src="image || 'https://img.icons8.com/wired/512/000000/document.png'">
                </div>
                <div v-if="bigImage == 1" @click="bigImage = 0">
                    <img class="bigImage" :src="image">
                    <div class="bigImageBackground"></div>
                </div>
            </div>
            <div style="margin-left:25px">
                <form @submit.prevent="addDoc">
                    <input type="file" id="file" class="inputfile" name="file" @change="onFileChange">
                    <p style="color: red">{{upload}}</p>
                    <p>Имя файла</p>
                    <input 
                        required
                        v-model="title"
                        type="text"
                        placeholder="Введите имя"
                        class="search-box"
                        autocomplete = usernameNew
                    />
                    <p>Запросить подпись:</p>
                    <div>
                        <div v-for="(user) in selectedUsers" :key="user.full_name" style="margin-bottom: 15px">
                            {{user.full_name}}
                            <a class="deleteSelectedUser" @click="deleteSelectedUser(user)">x</a>
                            </div>
                        <select v-model="selectedUser">
                            <option v-for="(user) in users" :key="user.email" :value="user">{{user.full_name}}</option>
                        </select>
                        <button type="button" @click="addUser(1)">ДОБАВИТЬ</button> <br>
                    </div>
                    <p>Пользователи, у которых были запрошены подписи, могут просматривать документ. 
                        Добавить дополнительных пользователей, которые не должны подписывать документ, но могут его просматривать:</p>
                    <div>
                        <div v-for="(user) in selectedUsers2" :key="user.full_name" style="margin-bottom: 15px">
                            {{user.full_name}}
                            <a class="deleteSelectedUser" @click="deleteSelectedUser(user)">x</a>
                            </div>
                        <select v-model="selectedUser2">
                            <option v-for="(user) in users" :key="user.email" :value="user">{{user.full_name}}</option>
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
                    <div style="height:35px;"></div>
                    <button type="submit" :class="{disabled: !this.image}">СОЗДАТЬ</button> <br>
                </form>
                <p v-if="error"> {{ error }} </p>
            </div>
        </div>
	</div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import axios from 'axios'
import { DOC_UPLOAD, DOC_REQUEST, DOCS_REQUEST, USERS_REQUEST } from '../store/mutation-types';

export default {
    name: 'account',
    data () {
		return {
            title: '',
            titleWithoutExt: '', // нигде не используется
            description: '',
            selectedUser: '',
            selectedUsers: [],
            selectedUser2: '',
            selectedUsers2: [],
            users: [],
            common: 0,
            error: null,
            image: false,
            pr: '',
            file:'',
            upload: '',
            bigImage: '',
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
            this.upload = "Загружается..."
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length) return;
            this.file = files[0];
            // console.log(this.file);
            /* Расширение файла */
            let typeFile = files[0].name.split('.')
            typeFile = typeFile[typeFile.length-1];
            /* Проверка на соответствие файлу*/
            let types = ['csv', 'doc', 
                        'xls', 'xlsb', 'xlsx', 'xlt', 'xltx', 
                        'jpg', 'jpeg', 'tif', 'tiff', 'png', 'bmp', 'mdi', 'gif', 'fax', 'ico',
                        'odc', 'odf', 'ppt', 'pptx', 'pdf',
                        'doc', 'docx', 'dot', 'dotx', 'wps', 'wpd', 'txt'];
            if (!types.includes(typeFile.toLowerCase())) {
                this.upload = "Файл с таким расширением загрузить нельзя."
            } else {
                this.image = '';
                /* Имя файла без расширения */
                let titleFile = files[0].name.replace("." + typeFile, "");
                this.titleWithoutExt = titleFile;
                this.title = titleFile + '.' + typeFile;
                // console.log(this.file);
                /* Конвертирование файла в картинку для превью */
                var formData = new FormData();
                formData.append('File', files[0], files[0].name);
                axios
                .post('https://v2.convertapi.com/convert/'
                    + typeFile
                    + '/to/jpg?Secret=ib7pzQhZXO4wvQro&Token=411617234', 
                    formData,
                )
                .then(data => {
                    this.file = files[0];
                    let b64Data = data.data.Files[0].FileData;
                    this.pr = this.dataURItoBlob(b64Data);
                    console.log('f', files[0])
                    console.log('p', this.blobToFile(this.dataURItoBlob(b64Data), files[0].name))
                    this.image = URL.createObjectURL(this.dataURItoBlob(b64Data));
                    this.upload = ""
                });
            }
            
        },
        blobToFile(theBlob, fileName) {
            //A Blob() is almost a File() - it's just missing the two properties below which we will add
            theBlob.lastModifiedDate = new Date();
            theBlob.name = fileName;
            return theBlob;
        },
        /* Конвертирование файла в картинку для превью */
        dataURItoBlob(dataURI) {
            var byteString = atob(dataURI);
            var ab = new ArrayBuffer(byteString.length);
            var ia = new Uint8Array(ab);
            for (var i = 0; i < byteString.length; i++) {
                ia[i] = byteString.charCodeAt(i);
            }
            return new Blob([ab], {type: 'image/png'});
        },
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
        deleteSelectedUser(item){
            this.selectedUsers = this.selectedUsers.filter(function(el){
                return el != item;
            });
            this.users.push(item);
        },
        addDoc(){
            var d = new FormData();
            // для файла
            if (this.file) {   
                const newFile = new File(
                    [this.file], 
                    this.title,
                    {type: this.file.type}
                );             
                d.file = d.append('file', newFile);
            }
            // для превью
            const newPr = new File(
                [this.pr],
                'preview.png',
                {type: 'image/png'}
            );
            d.append('user_id', this.$store.getters.getProfile.id);
            if (this.title) d.append('title', this.title);
            if (this.pr) d.append('preview', newPr);
            if (this.description) d.append('description', this.description);
            d.common = this.common ? d.append('common', true) : d.append('common', false);
            let dd = { d }
            if (this.selectedUsers) dd.signature_request = this.selectedUsers;
            if (this.selectedUsers2) dd.show_request = this.selectedUsers2;
            this.$store.dispatch(DOC_UPLOAD, dd)
			.then((resp) => {
                this.$store.dispatch(DOCS_REQUEST)
                .then(res => {
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
.addDoc textarea, .addDoc input[type="text"] [type]:not([type="checkbox"]){
	border: 0;
	margin: 0 auto;
    padding: 10px;
    min-width: 350px;
    background: rgb(223, 243, 253);;
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
    width: 200px;
}
/* Картинка при увеличении*/
.addDoc .bigImage{
    position: fixed;
    min-width:800px;
    height:auto;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    z-index: 5;
}
.addDoc img{
    cursor: pointer;
}
.addDoc .bigImageBackground{
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