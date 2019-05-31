<template>
    <div class="menu">
        <p>Картотека</p>
        <select v-model="fileCabinet" @change="onChange()">
            <option v-for="(fileC) in fileCabinets" :key="fileC.id" :value="fileC">{{fileC.name}}</option>
        </select>
        <router-link class="router-link" :to="{ path: '/documents/all', }">ВСЕ ДОКУМЕНТЫ</router-link>
        <router-link class="router-link" :to="{ path: '/documents/common', }">ОБЩИЙ ДОСТУП</router-link>
        <router-link class="router-link" :to="{ path: '/documents/myDocs', }">МОИ ДОКУМЕНТЫ</router-link>
        <router-link class="router-link" :to="{ path: '/documents/signature-request', }">НА ПОДПИСЬ</router-link>
        <router-link class="router-link" :to="{ path: '/documents/signature-success', }">ПОДПИСАННОЕ</router-link>
        <router-link class="router-link" :to="{ path: '/documents/available-to-me', }">ДОСТУПНЫ МНЕ</router-link>      
    </div>
</template>

<script>
import { } from '../store/mutation-types'
import {DOCS_FILE_CABINET, DOCS_REQUEST, DOCS_FILTER} from '../store/mutation-types'

export default {
    name: 'Menu',
    data () {
        return {
            fileCabinets: [],
            fileCabinet: '',
        }
    },
    created(){
        this.fileCabinets = this.$store.getters.getFileCabinets;
        this.fileCabinet = this.$store.getters.getFileCabinet;
    },
    methods: {
        onChange() {
            this.$store.commit(DOCS_FILE_CABINET, this.fileCabinet)
            this.$store.dispatch(DOCS_FILTER)
            console.log('store getFileCabinet', this.$store.getters.getFileCabinet)
            console.log('store getDocs', this.$store.getters.getDocs)
        },
    },
}
</script>

<style scoped>
/* Основное */
.menu{
    background-color: #ADE0FC;
    min-width: 250px;
    font-family: 'El Messiri', sans-serif;
    font-weight: 600;
    /* padding-top: 40px; */
}
/**/
.menu a{
    text-decoration: none;
    color: #373737;
}
.menu .router-link-exact-active{
    background: #64b2db;
}
.menu .router-link{
    font-size: 16px;
    color: #373737;
    padding: 11px 20px;
    padding-left: 50px;
	margin-top: 3px;
	margin-bottom: 3px;
	text-decoration: none;
	color: black;
	width: calc(100% - 70px);
	margin-left: 0;
	margin-right: 0;
	display: block;
}
.menu .link > router-link:hover{
    cursor: pointer;
}
.menu select{
    margin: 25px;
    margin-top: 5px;
    padding: 6px;
    font-size: 13.5px;
    min-width: 250px;
    border: 1;
}
.menu select button{
    border: 10px solid black;
}
.menu p{
    margin: 25px;
    margin-bottom: 0;
    font-weight: 500;
}
/* @media (max-width: 500px) {
    .menu{
        min-width: 0;
        background-color: blue;
    }
    .menu *{
        min-width: 0;
    }
} */
</style>