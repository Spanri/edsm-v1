<template>
	<div class="grid">
        <div v-if="filteredHeroes.length == 0">
            <p>Так грустно... Здесь ничего нет.</p>
            <svg fill="#7cb0c1" height="44" viewBox="0 0 24 24" width="44" xmlns="http://www.w3.org/2000/svg">
                <path class="heroicon-ui" d="M12 22a10 10 0 1 1 0-20 10 10 0 0 1 0 20zm0-2a8 8 0 1 0 0-16 8 8 0 0 0 0 16zm-3.54-4.54a5 5 0 0 1 7.08 0 1 1 0 0 1-1.42 1.42 3 3 0 0 0-4.24 0 1 1 0 0 1-1.42-1.42zM9 11a1 1 0 1 1 0-2 1 1 0 0 1 0 2zm6 0a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/>
            </svg>
        </div>
        <div v-if="filteredHeroes.length != 0">
            <form class="search">
                <p style="display: inline-block;margin:0;margin-bottom:15px;margin-right: 20px;">Поиск по всем столбцам</p>
                <input placeholder="Введите что-то" name="query" v-model="filterKey">
            </form>
            <p v-if="error" style="color: red;">{{error}}</p>
            <table>
                <thead>
                    <tr>
                        <th v-for="(key,i) in columns"
                            :key="i"
                            @click="sortBy(key.title)"
                            :class="{ active: sortKey == key }">
                            {{ key.title | capitalize }}
                            <span class="arrow" :class="sortOrders[key] > 0 ? 'asc' : 'dsc'">
                            </span>
                        </th>
                        <th v-if="id == 'notif'" style="padding: 0px 9px;">
                            <svg height="17px" viewBox="0 0 33 33" width="18px" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                                <g id="Cancel" stroke="black" stroke-width="1">
                                    <path clip-rule="evenodd" d="M16,0C7.163,0,0,7.163,0,16c0,8.836,7.163,16,16,16   c8.836,0,16-7.163,16-16C32,7.163,24.836,0,16,0z M16,30C8.268,30,2,23.732,2,16C2,8.268,8.268,2,16,2s14,6.268,14,14   C30,23.732,23.732,30,16,30z" 
                                        fill="#121313" fill-rule="evenodd"/>
                                    <path clip-rule="evenodd" d="M22.729,21.271l-5.268-5.269l5.238-5.195   c0.395-0.391,0.395-1.024,0-1.414c-0.394-0.39-1.034-0.39-1.428,0l-5.231,5.188l-5.309-5.31c-0.394-0.396-1.034-0.396-1.428,0   c-0.394,0.395-0.394,1.037,0,1.432l5.301,5.302l-5.331,5.287c-0.394,0.391-0.394,1.024,0,1.414c0.394,0.391,1.034,0.391,1.429,0   l5.324-5.28l5.276,5.276c0.394,0.396,1.034,0.396,1.428,0C23.123,22.308,23.123,21.667,22.729,21.271z" 
                                        fill="#121313" fill-rule="evenodd"/>
                                </g>
                            </svg>
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(entry,j) in filteredHeroes" :key="j" :style="styleObject(entry)" class="rowData" :class="{disabled: disable}">
                        <td v-for="(key,i) in columns" :key="i" @click="i != 5 ? toDoc(entry) : ''">
                            {{entry[key.key]}}
                        </td>
                        <td style="padding: 0px 2px;" v-if="id == 'notif'">
                            <svg v-if="id == 'notif' && entry.status == 3" @click="hideNotif(j);" style="margin:auto;padding:7px;cursor:pointer;" height="17px" viewBox="0 0 33 33" width="18px" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                                <g id="Cancel" stroke="black" stroke-width="1">
                                    <path clip-rule="evenodd" d="M16,0C7.163,0,0,7.163,0,16c0,8.836,7.163,16,16,16   c8.836,0,16-7.163,16-16C32,7.163,24.836,0,16,0z M16,30C8.268,30,2,23.732,2,16C2,8.268,8.268,2,16,2s14,6.268,14,14   C30,23.732,23.732,30,16,30z" 
                                        fill="#121313" fill-rule="evenodd"/>
                                    <path clip-rule="evenodd" d="M22.729,21.271l-5.268-5.269l5.238-5.195   c0.395-0.391,0.395-1.024,0-1.414c-0.394-0.39-1.034-0.39-1.428,0l-5.231,5.188l-5.309-5.31c-0.394-0.396-1.034-0.396-1.428,0   c-0.394,0.395-0.394,1.037,0,1.432l5.301,5.302l-5.331,5.287c-0.394,0.391-0.394,1.024,0,1.414c0.394,0.391,1.034,0.391,1.429,0   l5.324-5.28l5.276,5.276c0.394,0.396,1.034,0.396,1.428,0C23.123,22.308,23.123,21.667,22.729,21.271z" 
                                        fill="#121313" fill-rule="evenodd"/>
                                </g>
                            </svg>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
	</div>
</template>

<script>
import { mapGetters, mapState } from 'vuex'
import {
    DOCS_REQUEST, 
    DOC_UPDATE, 
    USER_REQUEST, 
    USER_NOTIF_REQUEST, 
    DOC_FOLDER_PAGE, 
    DOC_FOLDER_PAGE_PROFILE,
    DOCS_FILTER,
    DOC_EDIT_NOTIF,
    DOC_REQUEST,
    DOC_RELOAD,
} from '../../store/mutation-types'

export default {
    name: 'grid',
    props: {
        id: String,
        columns: Array,
    },
    data: function () {
        var sortOrders = {}
        this.columns.forEach(function (key) {
            sortOrders[key] = 1
        });
        return {
            h: null,
            sortKey: '',
            filterKey: '',
            sortOrders: sortOrders,
            error: '',
        }
    },
    async created(){
        await this.$store.dispatch(DOCS_REQUEST)
        await this.$store.dispatch(DOCS_FILTER)
    },
    computed: {
        ...mapGetters({
            getProfile: 'getProfile',
            getDocs: 'getDocs',
            getDocsOld: 'getDocsOld',
        }),
        disable() {
            return this.$store.getters.getReload;
        },
        filteredHeroes() {
            var sortKey = ''
            var sortOrders = {}
            this.columns.forEach(function (key) {
                sortOrders[key] = 1
            });
            var filterKey = this.filterKey && this.filterKey.toLowerCase()
            var order = this.sortOrders[sortKey] || 1
            var heroes = this.heroes || this.h;
            if (filterKey) {
                heroes = heroes.filter(function (row) {
                    return Object.keys(row).some(function (key) {
                        return String(row[key]).toLowerCase().indexOf(filterKey) > -1
                    })
                })
            }
            if (sortKey) {
                heroes = heroes.slice().sort(function (a, b) {
                    a = a[sortKey]
                    b = b[sortKey]
                    return (a === b ? 0 : a > b ? 1 : -1) * order
                })
            }
            // console.log('heroes', heroes)
            return heroes
        },
		heroes() {
            let id = this.$route.params.id;
            // console.log(this.getDocs)
            let output = [];
            if(id == 'all'){
			    output = this.getDocs;
            } else if(id == 'common') {
                output = this.getDocs
                .filter(d => d.doc.common);
            } else if(id == 'myDocs') {
                output = this.getDocs.filter(d =>
                    d.user.id == this.getProfile.id && 
                    d.status == 0
                );
            } else if(id == 'signature-request') {
                output = this.getDocs.filter(d => d.status == 2);
            } else if(id == 'signature-success') {
                output = this.getDocs.filter(d => d.status == 6);
            } else if(id == 'available-to-me') {
                output = this.getDocs
                .filter(d => d.status == 5);
            } else if(this.id == 'notif') {
                let docs = this.getDocsOld.filter(d => 
                    d.status == 3 || d.status == 2
                );
                docs.forEach(d => {
                    if(d.status == 3){
                        d.message = "Ваш документ подписали."
                    }
                    if(d.status == 2){
                        d.message = "Вас просят подписать документ."
                    }
                })
                output = docs;
            } else {
                output = null;
            }
            // this.disable = false;
            return output;
		}
    },
    filters: {
        capitalize(str) {
            return str.charAt(0).toUpperCase() + str.slice(1)
        }
    },
    methods: {
        styleObject(entry) {
            return {'--button-background-color': entry.rowBackg}
        },
        sortBy(key) {
            this.sortKey = key
            this.sortOrders[key] = this.sortOrders[key] * -1
        },
        toDoc(entry){
            console.log(entry)
            if(entry.rowBackg == '#dcdbfc'){
                let id = this.getProfile.id;
                this.$store.dispatch(DOC_EDIT_NOTIF, {
                    user: id,
                    notif: entry.id,
                    pk3: 0,
                })
                .then(r => {
                    this.$store.dispatch(DOC_UPDATE, entry.id)
                    .then(s => {
                        this.$router.push('/document/' + entry.doc.id);
                    })
                })
                .catch(err => {
                    console.log(err)
                    this.error = 'Ошибка. Что-то пошло не так.'
                })
            } else if(entry.rowBackg == "white") {
                this.$store.dispatch(DOC_REQUEST, entry.id)
                .then(r => {
                    this.$router.push('/document/' + entry.doc.id);
                })
                .catch(err=>{
                    console.log(err)
                    this.error = 'Ошибка. Что-то пошло не так.'
                })
            }
        },
        hideNotif(j){
            let id = this.getProfile.id;
            this.$store.dispatch(DOC_EDIT_NOTIF, {
                user: id,
                notif: this.filteredHeroes[j].id,
                pk3: 1,
            })
            .then(r => {
                this.error = ''
            })
            .catch(err=>{
                console.log(err)
                this.error = 'Ошибка. Что-то пошло не так.'
            })
        }
    }
}
</script>

<style scoped>
.grid{
	width: 100%;
	background: white;
}
.grid > *{
	margin: 50px;
    margin-top: 35px;
}
table {
    border-collapse: collapse;
}
table, th, td{
    border: #64b2db 1px solid;
}
td, th{
    padding: 7px 15px;
}
th{
    background: rgb(223, 243, 253);
}
.rowData{
    background: var(--button-background-color);
}
.rowData:hover{
    cursor: pointer;
    background: rgb(223, 243, 253);
}
.arrow{
    display: inline-block;
}
.search{
    margin-top: 35px;
    margin-bottom: 35px;
}
input{
    border: 0;
    background: rgb(223, 243, 253);
	height: 30px;
	min-width: 250px;
	margin: 0 auto;
	margin-left: 0px;
	padding-left: 15px;
	padding-right: 15px;
}
/* Недоступность документов при обновлении данных */
.disabled{
    display: none;
    /* pointer-events: none;
    background: #d6d6d6;
    color: #4e4848; */
}
</style>