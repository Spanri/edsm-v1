<template>
    <div id="menu">
        <div v-if="closeMenu" title="Раскрыть" style="height:100%;" class="openCloseMenuButton" @click="closeMenu = false">
            <svg fill="#347090" enable-background="new 0 0 96 96" height="26px" viewBox="0 0 96 96" width="26px" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                <path d="M12,52h62.344L52.888,73.456c-1.562,1.562-1.562,4.095-0.001,5.656c1.562,1.562,4.096,1.562,5.658,0l28.283-28.284l0,0  c0.186-0.186,0.352-0.391,0.498-0.609c0.067-0.101,0.114-0.21,0.172-0.315c0.066-0.124,0.142-0.242,0.195-0.373  c0.057-0.135,0.089-0.275,0.129-0.415c0.033-0.111,0.076-0.217,0.099-0.331C87.973,48.525,88,48.263,88,48l0,0  c0-0.003-0.001-0.006-0.001-0.009c-0.001-0.259-0.027-0.519-0.078-0.774c-0.024-0.12-0.069-0.231-0.104-0.349  c-0.039-0.133-0.069-0.268-0.123-0.397c-0.058-0.139-0.136-0.265-0.208-0.396c-0.054-0.098-0.097-0.198-0.159-0.292  c-0.146-0.221-0.314-0.427-0.501-0.614L58.544,16.888c-1.562-1.562-4.095-1.562-5.657-0.001c-1.562,1.562-1.562,4.095,0,5.658  L74.343,44L12,44c-2.209,0-4,1.791-4,4C8,50.209,9.791,52,12,52z"/>
            </svg>
        </div>
        <div v-if="!closeMenu" class="menuOpen">
            <div title="Скрыть" style="display: grid;grid-template-columns: 1fr auto;">
                <!-- <p style="color: red;font-size:14px;">{{reload}}&nbsp;</p> -->
                <p v-if="!reload">&nbsp;</p>
                <svg v-if="reload" class="reload" version="1.1" viewBox="0 0 16 16" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                    <path d="M14,8c-0.609,0-0.898,0.43-1,0.883C12.635,10.516,11.084,13,8,13c-0.757,0-1.473-0.172-2.114-0.474L6.414,12  C6.773,11.656,7,11.445,7,11c0-0.523-0.438-1-1-1H3c-0.609,0-1,0.492-1,1v3c0,0.541,0.428,1,1,1c0.484,0,0.688-0.273,1-0.594  l0.408-0.407C5.458,14.632,6.685,15,8,15c4.99,0,7-4.75,7-5.938C15,8.336,14.469,8,14,8z M3,7.117C3.365,5.485,4.916,3,8,3  c0.757,0,1.473,0.171,2.114,0.473L9.586,4C9.227,4.344,9,4.555,9,5c0,0.523,0.438,1,1,1h3c0.609,0,1-0.492,1-1V2  c0-0.541-0.428-1-1-1c-0.484,0-0.688,0.273-1,0.594l-0.408,0.407C10.542,1.368,9.315,1,8,1C3.01,1,1,5.75,1,6.938  C1,7.664,1.531,8,2,8C2.609,8,2.898,7.57,3,7.117z"/>
                </svg>
                <svg class="openCloseMenuButton" style="margin-bottom:0px;margin-top:15px;margin-right:15px;" @click="closeMenu = true" height="21px" viewBox="0 0 31 32" width="22px" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                    <g id="Cancel" stroke="#347090" stroke-width="1">
                        <path clip-rule="evenodd" d="M16,0C7.163,0,0,7.163,0,16c0,8.836,7.163,16,16,16   c8.836,0,16-7.163,16-16C32,7.163,24.836,0,16,0z M16,30C8.268,30,2,23.732,2,16C2,8.268,8.268,2,16,2s14,6.268,14,14   C30,23.732,23.732,30,16,30z"
                            fill="#121313" fill-rule="evenodd"/>
                        <path clip-rule="evenodd" d="M22.729,21.271l-5.268-5.269l5.238-5.195   c0.395-0.391,0.395-1.024,0-1.414c-0.394-0.39-1.034-0.39-1.428,0l-5.231,5.188l-5.309-5.31c-0.394-0.396-1.034-0.396-1.428,0   c-0.394,0.395-0.394,1.037,0,1.432l5.301,5.302l-5.331,5.287c-0.394,0.391-0.394,1.024,0,1.414c0.394,0.391,1.034,0.391,1.429,0   l5.324-5.28l5.276,5.276c0.394,0.396,1.034,0.396,1.428,0C23.123,22.308,23.123,21.667,22.729,21.271z"
                            fill="#121313" fill-rule="evenodd"/>
                    </g>
                </svg>
            </div>
            <p style="margin-top:0px">Картотека</p>
            <select v-model="fileCabinet" @change="onChange()">
                <option v-for="(fileC) in fileCabinets" :key="fileC.id" :value="fileC">{{fileC.name}}</option>
            </select>
            <router-link @click.native="goToFolder" class="router-link" to="/documents/all">ВСЕ ДОКУМЕНТЫ</router-link>
            <router-link @click.native="goToFolder" class="router-link" to="/documents/myDocs">МОИ ДОКУМЕНТЫ</router-link>
            <router-link @click.native="goToFolder" class="router-link" to="/documents/common">ОБЩИЙ ДОСТУП</router-link>
            <router-link @click.native="goToFolder" class="router-link" to="/documents/available-to-me">ДОСТУПНЫ МНЕ</router-link>
            <router-link @click.native="goToFolder" class="router-link" to="/documents/my-doc-signature-request">НА ПОДПИСИ</router-link>
            <router-link @click.native="goToFolder" class="router-link" to="/documents/signature-request">НА ПОДПИСЬ</router-link>
            <router-link @click.native="goToFolder" class="router-link" to="/documents/signature-success">ПОДПИСАННОЕ</router-link>
        </div>
    </div>
</template>

<script>
import {
    DOCS_FILE_CABINET,
    DOCS_REQUEST,
    DOCS_FILTER,
    ADDIT_RELOAD,
} from '../store/mutation-types'

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
        this.reload = true;
        this.$store.dispatch(DOCS_FILTER);
        let docs = this.$store.getters.getDocsOld;
        this.fileCabinets = this.$store.getters.getFileCabinets;
        let dfc = [];
        this.fileCabinets = this.fileCabinets.filter(re => {
            dfc = docs.filter(r => r.doc.file_cabinet.id == re.id);
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
        this.reload = false;
    },
    computed: {
        reload: {
            get(){
                return this.$store.getters.getReload;
            },
            set(newValue){
                this.$store.commit(ADDIT_RELOAD, newValue);
            }
        }
    },
    methods: {
        async onChange(){
            this.reload = true;
            await this.$store.commit(DOCS_FILE_CABINET, this.fileCabinet);
            await this.$store.dispatch(DOCS_REQUEST);
            await this.$store.dispatch(DOCS_FILTER);
            this.reload = false;
        },
        async goToFolder(){
            this.reload = true;
            await this.$store.dispatch(DOCS_REQUEST)
            await this.$store.dispatch(DOCS_FILTER)
            this.reload = false;
        }
    },
}
</script>

<style scoped>
/* Основное */
#menu {
    background-color: #ADE0FC;
    font-family: 'PT+Sans+Narrow', sans-serif;
}

/**/
.menuOpen {
    min-width: 250px;
}

.openCloseMenuButton {
    margin: 5px;
}

.openCloseMenuButton:hover, .openCloseMenuButton:hover *{
    cursor: pointer;
    fill:#7cb0c1;
    stroke: #7cb0c1;
}

/* Картотека */
select {
    margin: 25px;
    margin-top: 5px;
    padding: 6px;
    font-size: 13.5px;
    min-width: 230px;
    border: 1;
}

select button {
    border: 10px solid black;
}

p {
    margin: 25px;
    margin-bottom: 0;
    font-weight: 500;
}

/**/
.reload {
    fill: white;
    enable-background: new 0 0 16 16;
    padding: 15px;
    margin-left: 10px;
    height: 20px;
    width: 20px;
    animation: spin 2s linear infinite;
}

@keyframes spin {
    100% {
        transform: rotate(360deg);
    }
}

/**/
a {
    text-decoration: none;
    color: #373737;
}

.router-link-exact-active {
    background: #64b2db;
    pointer-events: none;
    cursor: default;
}

.router-link {
  font-size: 16px;
  color: #373737;
  padding: 11px 20px;
  padding-left: 40px;
	margin-top: 3px;
	margin-bottom: 3px;
	text-decoration: none;
	color: black;
	width: calc(100% - 45px);
	margin-left: 0;
	margin-right: 0;
	display: block;
}

.link > router-link:hover {
    cursor: pointer;
}
</style>
