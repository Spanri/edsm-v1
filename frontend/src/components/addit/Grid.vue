<template>
	<div class="grid">
		<form id="search">
			Поиск по всем столбцам <input name="query" v-model="filterKey">
		</form>
        <p v-if="error" style="color: red;">{{error}}</p>
        <div style="display: flex; align-items: flex-start">
            <table class="showData">
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
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(entry,j) in filteredHeroes" :key="j" @click="toDoc(entry)" :style="{background: entry.rowBackg}">
                        <td v-for="(key,i) in columns" :key="i">
                            {{entry[key.key]}}
                        </td>
                    </tr>
                </tbody>
            </table>
            <table style="border: white 3px solid;border-radius: 5px;" v-if="id == 'notif'">
                <thead>
                    <tr>
                        <th style="border:0;">&nbsp;</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(entry,j) in filteredHeroes" :key="j">
                        <td style="padding:0px">
                            <div v-if="entry.status != 3" style="padding:7.5px;magrin:0;">&nbsp;</div>
                            <svg v-if="entry.status == 3" @click="hideNotif(j);" style="margin:0;padding:7px;cursor:pointer;" height="17px" viewBox="0 0 33 33" width="18px" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
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
    DOC_REQUEST, 
    USER_REQUEST, 
    USER_NOTIF_REQUEST, 
    DOC_FOLDER_PAGE, 
    DOC_FOLDER_PAGE_PROFILE,
    DOCS_FILTER,
    DOC_EDIT_NOTIF,
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
    created(){
        this.$store.dispatch(USER_REQUEST)
        this.$store.dispatch(DOCS_REQUEST)
    },
    computed: {
        ...mapGetters({
            getProfile: 'getProfile',
            getDocs: 'getDocs',
            getDocsOld: 'getDocsOld',
        }),
        filteredHeroes() {
            var sortKey = ''
            var sortOrders = {}
            this.columns.forEach(function (key) {
                sortOrders[key] = 1
            });
            var filterKey = this.filterKey && this.filterKey.toLowerCase()
            var order = this.sortOrders[sortKey] || 1
            var heroes = this.heroes || this.h;
            heroes.forEach((h, i) => {
                let hh = h.is_read.filter(h0 => {
                    return h0.id == this.getProfile.id
                })
                let myDoc = h.status == 0 && h.user.id == this.getProfile.id
                heroes[i].rowBackg = (hh.length != 0 || myDoc) ? "white" : "#dcdbfc"
            })
            // console.log(heroes)
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
            if(this.$route.params.id == 'all'){
			    return this.getDocs;
            } else if(this.$route.params.id == 'common') {
                return this.getDocs
                .filter(d => d.doc.common);
            } else if(this.$route.params.id == 'myDocs') {
                return this.getDocs.filter(d =>
                    d.user.id == this.getProfile.id && 
                    d.status == 0
                );
            } else if(this.$route.params.id == 'signature-request') {
                return this.getDocs.filter(d => d.status == 2);
            } else if(this.$route.params.id == 'signature-success') {
                return this.getDocs.filter(d => d.status == 6);
            } else if(this.$route.params.id == 'available-to-me') {
                return this.getDocs
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
                return docs;
            }
            return null;
		}
    },
    filters: {
        capitalize(str) {
            return str.charAt(0).toUpperCase() + str.slice(1)
        }
    },
    methods: {
        sortBy(key) {
            this.sortKey = key
            this.sortOrders[key] = this.sortOrders[key] * -1
        },
        toDoc(entry){
            let id = this.getProfile.id;
            this.$store.dispatch(DOC_EDIT_NOTIF, {
                user: id,
                notif: entry.id,
                pk3: 0,
            })
            .then(r => {
                this.$store.dispatch(DOCS_REQUEST)
                this.$router.push('/document/' + entry.doc.id);
            })
            .catch(err=>{
                console.log(err)
                this.error = 'Ошибка. Что-то пошло не так.'
            })
        },
        hideNotif(j){
            let id = this.getProfile.id;
            this.$store.dispatch(DOC_EDIT_NOTIF, {
                user: id,
                notif: this.filteredHeroes[j].id,
                pk3: 1,
            })
            .catch(err=>{
                console.log(err)
                this.error = 'Ошибка. Что-то пошло не так.'
            })
        }
    }
}
</script>

<style>
.grid{
	width: 100%;
	background: white;
}
.grid > *{
	margin: 50px;
}
.grid table {
    border-collapse: collapse;
}
.grid .showData table, .grid .showData th, .grid .showData td{
    border: #64b2db 2px solid;
    border-radius: 5px;
}
.grid td, .grid th{
    padding: 7px 15px;
}
.grid .showData th{
    background: rgb(223, 243, 253);
}
.grid .showData tr:hover{
    cursor: pointer;
    background: rgb(223, 243, 253);
}
.grid .arrow{
    display: inline-block;
}
.grid input{
	border: #e0e0e0 3px solid;
    border-radius: 5px;
	height: 30px;
	min-width: 250px;
	margin: 0 auto;
	margin-left: 20px;
	padding-left: 15px;
	padding-right: 15px;
}
</style>