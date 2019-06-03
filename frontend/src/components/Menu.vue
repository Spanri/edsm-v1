<template>
    <div class="menu">
        <div v-if="closeMenu" title="Раскрыть" style="height:100%" class="openCloseMenuButton" @click="closeMenu = false">
            <svg fill="#347090" enable-background="new 0 0 96 96" height="26px" viewBox="0 0 96 96" width="26px" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                <path d="M12,52h62.344L52.888,73.456c-1.562,1.562-1.562,4.095-0.001,5.656c1.562,1.562,4.096,1.562,5.658,0l28.283-28.284l0,0  c0.186-0.186,0.352-0.391,0.498-0.609c0.067-0.101,0.114-0.21,0.172-0.315c0.066-0.124,0.142-0.242,0.195-0.373  c0.057-0.135,0.089-0.275,0.129-0.415c0.033-0.111,0.076-0.217,0.099-0.331C87.973,48.525,88,48.263,88,48l0,0  c0-0.003-0.001-0.006-0.001-0.009c-0.001-0.259-0.027-0.519-0.078-0.774c-0.024-0.12-0.069-0.231-0.104-0.349  c-0.039-0.133-0.069-0.268-0.123-0.397c-0.058-0.139-0.136-0.265-0.208-0.396c-0.054-0.098-0.097-0.198-0.159-0.292  c-0.146-0.221-0.314-0.427-0.501-0.614L58.544,16.888c-1.562-1.562-4.095-1.562-5.657-0.001c-1.562,1.562-1.562,4.095,0,5.658  L74.343,44L12,44c-2.209,0-4,1.791-4,4C8,50.209,9.791,52,12,52z"/>
            </svg>
        </div>
        <div v-if="!closeMenu" class="menuOpen">
            <div title="Скрыть" style="display: grid;grid-template-columns: 1fr auto;">
                <div></div>
                <svg class="openCloseMenuButton" style="margin-bottom:0px;margin-top:15px;margin-right:15px;" @click="closeMenu = true" height="21px" viewBox="0 0 31 32" width="22px" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                    <g id="Cancel" stroke="#347090" stroke-width="1">
                        <path clip-rule="evenodd" d="M16,0C7.163,0,0,7.163,0,16c0,8.836,7.163,16,16,16   c8.836,0,16-7.163,16-16C32,7.163,24.836,0,16,0z M16,30C8.268,30,2,23.732,2,16C2,8.268,8.268,2,16,2s14,6.268,14,14   C30,23.732,23.732,30,16,30z" 
                            fill="#121313" fill-rule="evenodd"/>
                        <path clip-rule="evenodd" d="M22.729,21.271l-5.268-5.269l5.238-5.195   c0.395-0.391,0.395-1.024,0-1.414c-0.394-0.39-1.034-0.39-1.428,0l-5.231,5.188l-5.309-5.31c-0.394-0.396-1.034-0.396-1.428,0   c-0.394,0.395-0.394,1.037,0,1.432l5.301,5.302l-5.331,5.287c-0.394,0.391-0.394,1.024,0,1.414c0.394,0.391,1.034,0.391,1.429,0   l5.324-5.28l5.276,5.276c0.394,0.396,1.034,0.396,1.428,0C23.123,22.308,23.123,21.667,22.729,21.271z" 
                            fill="#121313" fill-rule="evenodd"/>
                    </g>
                </svg>
            </div>
            <p style="margin-top:10px">Картотека</p>
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
            closeMenu: false,
        }
    },
    created(){
        this.$store.dispatch(DOCS_FILTER)
        let docs = this.$store.getters.getDocsOld;
        this.fileCabinets = this.$store.getters.getFileCabinets;
        let dfc = [];
        this.fileCabinets = this.fileCabinets.filter(re => {
            dfc = docs.filter(r => r.doc.fileCabinet.id == re.id);
            if (dfc.length != 0) {
                return true;
            } else {
                return false;
            }
        })
        this.fileCabinet = this.$store.getters.getFileCabinet;
        if (this.fileCabinet in this.fileCabinets === false) {
            this.fileCabinet = this.fileCabinets[0];
        }
    },
    methods: {
        onChange() {
            this.$store.commit(DOCS_FILE_CABINET, this.fileCabinet)
            this.$store.dispatch(DOCS_FILTER)
        },
    },
}
</script>

<style scoped>
/* Основное */
.menu{
    background-color: #ADE0FC;
    font-family: 'El Messiri', sans-serif;
    font-weight: 600;
    /* padding-top: 40px; */
}
/**/
.menu .menuOpen{
    min-width: 250px;
}
.menu .openCloseMenuButton{
    margin: 5px;
}
.menu .openCloseMenuButton:hover, .menu .openCloseMenuButton:hover *{
    cursor: pointer;
    fill:#7cb0c1;
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