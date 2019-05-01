<template>
    <div class="menu">
        <input class="search" v-model="message" placeholder="Искать...">
        <p class="link editLink" @click="edit()">{{editMessage}}</p>
        <div class="catalog">
            <div class="link">
                <a href="/">ВСЕ ДОКУМЕНТЫ</a>
            </div>
            <div class="link">
                <a href="/d/1">ОБЩИЙ ДОСТУП</a>
            </div>
            <div class="link">
                <a href="/d/2">МОИ ДОКУМЕНТЫ</a>
            </div>
            <div class="link" v-for="item in items" :key="item.title">
                <a :href="item.ref">{{item.title}}</a>
                <a class="deleteMenu" @click="deleteMenu(item)" v-if="isEdit">X</a>
            </div>
            <div v-if="isEdit">
                <input class="newFolder" v-model="newFolder" placeholder="Введите имя новой папки">
                <button class="newFolderButton" @click="newFolderFun()">+</button>
            </div>
        </div>
    </div>
</template>

<script>
import {DOC_FOLDER_REQUEST, DOC_FOLDER_UPDATE} from '../store/mutation-types'

export default {
    name: 'Menu',
    data () {
        return {
            message: '',
            newFolder: '',
            isEdit: false,
            editMessage: 'РЕДАКТИРОВАТЬ ПАПКИ',
            items: []
        }
    },
    created() {
        this.$store.dispatch(DOC_FOLDER_REQUEST);
        this.items = this.$store.getters.getFolder;
    },
    methods: {
        edit(){
            this.editMessage=="ЗАКОНЧИТЬ РЕДАКТИРОВАНИЕ" ? 
                this.editMessage="РЕДАКТИРОВАТЬ ПАПКИ" : 
                this.editMessage="ЗАКОНЧИТЬ РЕДАКТИРОВАНИЕ";
            this.isEdit = !this.isEdit;
        },
        deleteMenu(item){
            if (confirm("Действительно удалить папку "+item.title+"?")){
                this.items = this.items.filter(function(el){
                    return el.ref != item.ref;
                });
                this.$router.push('/');
            }
        },
        newFolderFun(){
            let newFolderItem = {
                title: this.newFolder.toUpperCase(),
                ref: "/d/"+Number(this.items[this.items.length-1].ref) + 1
            }
            // this.items.push(newFolderItem);
            this.$store.dispatch(DOC_FOLDER_UPDATE, newFolderItem);
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* Основное */
.menu{
    background-color: #ADE0FC;
    min-width: 350px;
}
/* Поиск */
.search{
    margin: 30px 50px;
    margin-bottom: 0;
    height: 35px;
    width: calc(100% - 130px);
    background-color: white;
    border: 0;
    padding: 0px 15px;
}
/* Создать новую папку */
.newFolder{
    margin: 30px 0px 30px 50px;
    margin-top: 0;
    height: 35px;
    min-width: calc(100% - 160px);
    background-color: white;
    border: 0;
    padding: 0px 15px;
    display: inline-block;
}
.newFolderButton{
    border: 0;
	border-radius: 5px;
	padding: 8px;
	color: white;
	background-color: #347090;
    font-size: 18px;
    font-weight: 700;
}
/**/
.catalog > *{
    margin: 10px;
    margin: auto;
}
.link{
    margin: 30px 20px;
    margin-left: 50px;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 16px;
    color: #373737;
}
.editLink{
    margin-bottom:50px;
    color:#347090;
}
.editLink:hover{
    cursor: pointer;
    color:#ffffff;
}
a{
    text-decoration: none;
    color: #373737;
}
a:hover{
    color:#347090;
    cursor: pointer;
}
/**/
.deleteMenu{
    margin: 0 10px;
    color:#ffffff;
    font-size: 18px;
    font-weight: 700;
}
@media (max-width: 500px) {
    .menu{
        min-width: 0;
        background-color: blue;
    }
    .menu *{
        min-width: 0;
    }
}
</style>