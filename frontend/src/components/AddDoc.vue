<template>
	<div class="addDoc">
		<h3 class="header">ДОБАВЛЕНИЕ ДОКУМЕНТА</h3>
        <div class="addDoc2Colon">
            <div>
                <img :src="image">
                <a :href="file"></a>
            </div>
            <div style="margin-left:25px">
                <!-- <iframe id="viewer" :src="pdf" frameborder="0" scrolling="no" width="400" height="600"></iframe> -->
                <form @submit.prevent="addDoc">
                    <input type="file" id="file" name="file" @change="onFileChange">
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
                        <div v-for="(user,i) in selectedUsers" :key="i" style="margin-bottom: 15px">
                            {{user}}
                            <a class="deleteSelectedUser" @click="deleteSelectedUser(user)">x</a>
                            </div>
                        <select v-model="selectedUser">
                            <option v-for="(user,i) in users" :key="i">{{user}}</option>
                        </select>
                        <button type="button" @click="addUser">ДОБАВИТЬ</button> <br>
                    </div>
                    <div style="height:15px;"></div>
                    <p>Описание</p>
                    <textarea
                        v-model="description" 
                        placeholder="Опишите документ"
                        class="search-box"
                    ></textarea>
                    <p></p> Общий доступ <input type="checkbox" name="common" true-value="1"  false-value="0" v-model="common">
                    <div style="height:35px;"></div>
                    <button type="submit" @click="addDoc">СОЗДАТЬ</button> <br>
                </form>
                <p v-if="error"> {{ error }} </p>
            </div>
        </div>
	</div>
</template>

<script>
import { mapState } from 'vuex'

export default {
    name: 'account',
    data () {
		return {
            title: '',
            description: '',
            selectedUser: '',
            selectedUsers: [],
            users: [
                'A1', 'A2', 'A3'
            ],
            common: 0,
            error: null,
            image: "./src/assets/profile-img.jpg",
            file:''
		}
    },
    methods: {
        onFileChange(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length)
                return;
            this.createImage(files[0]);
            let title2 = files[0].name.split('.');
            title2 = title2[title2.length-1];
            title2 = files[0].name.replace("."+title2,"");
            this.title = title2;
            this.file = files[0];
        },
        createImage(file) {
            var image = new Image();
            var reader = new FileReader();
            var vm = this;

            reader.onload = (e) => {
                vm.image = e.target.result;
                this.file = vm.image
            };
            reader.readAsDataURL(file);
        },
        addUser(){
            const {selectedUser} = this;
            this.selectedUsers.push(selectedUser);
            this.users = this.users.filter(function(el){
                return el != selectedUser;
            });
        },
        deleteSelectedUser(item){
            this.selectedUsers = this.selectedUsers.filter(function(el){
                return el != item;
            });
            this.users.push(item);
        },
        addDoc(){

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
.header{
    margin-top: 0;
	margin-bottom: 30px;
}
/* Поля ввода */
.addDoc textarea, .addDoc input[type="text"]{
	border: 0;
	margin: 0 auto;
    padding: 10px;
    min-width: 350px;
    background: #ADE0FC;
}
/* Кнопки ЗАГРУЗИТЬ и СОЗДАТЬ */
.addDoc button, .addDoc input[type="submit"]{
	border: 0;
	border-radius: 5px;
	padding: 8px;
    margin-top: 15px;
    margin-bottom: 15px;
	color: white;
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
/**/
.deleteSelectedUser{
    border: 0;
	border-radius: 5px;
	padding: 3px;
    padding: 5px;
    padding-top: 2px;
	color: white;
	background-color: #347090;
}
/**/
/* .uploadForm {
    outline: 2px dashed grey;  
    outline-offset: -10px;
    background: lightcyan;
    color: dimgray;
    padding: 10px 10px;
    min-height: 200px; 
    position: relative;
    cursor: pointer;
  }

  #file {
    opacity: 0; 
    width: 100%;
    height: 200px;
    position: absolute;
    cursor: pointer;
  }

  .uploadForm:hover {
    background: lightblue; 
  }

  .uploadForm p {
    font-size: 1.2em;
    text-align: center;
    padding: 50px 0;
  } */
</style>