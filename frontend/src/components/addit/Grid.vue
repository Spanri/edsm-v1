<template>
	<div class="grid">
		<form id="search">
			Поиск по всем столбцам <input name="query" v-model="filterKey">
		</form>
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
                </tr>
            </thead>
            <tbody>
                <tr v-for="(entry,j) in filteredHeroes" :key="j" @click="toDoc(entry.id)">
                    <td v-for="(key,i) in columns" :key="i">
                    {{entry[key.key]}}
                    </td>
                </tr>
            </tbody>
        </table>
	</div>
</template>

<script>
import { mapGetters, mapState } from 'vuex'
import {DOCS_REQUEST, DOC_REQUEST, USER_REQUEST} from '../../store/mutation-types'

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
            title: {
                '': 'ВСЕ ДОКУМЕНТЫ',
                'common': 'ОБЩИЙ ДОСТУП',
                'myDocs': 'МОИ ДОКУМЕНТЫ'
            },
            sortKey: '',
            filterKey: '',
            sortOrders: sortOrders
        }
    },
    created(){
        this.$store.dispatch(USER_REQUEST, this.token)
        this.$store.dispatch(DOCS_REQUEST, this.getProfile.docs)
    },
    computed: {
        ...mapGetters({
            getProfile: 'getProfile',
            getDocs: 'getDocs',
            token: 'token',
            getNotif: 'getNotif',
        }),
        filteredHeroes() {
            var sortKey = ''
            var sortOrders = {}
            this.columns.forEach(function (key) {
                sortOrders[key] = 1
            });
            var filterKey = this.filterKey && this.filterKey.toLowerCase()
            var order = this.sortOrders[sortKey] || 1
            var heroes = this.heroes
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
            return heroes
        },
		heroes() {
            if(this.$route.params.id == 'all'){
			    return this.getDocs;
            } else if(this.$route.params.id == 'common') {
                return this.getDocs
                .filter(d => d.common == true);
            } else if(this.$route.params.id == 'myDocs') {
                return this.getDocs
                .filter(d => d.owner_id == this.getProfile.id);
            } else if(this.id == 'notif') {
                return this.getProfile.notif;
            }
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
        toDoc(id){
            this.$router.push('/doc/'+id);
        },
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
.grid table, .grid th, .grid td{
    border: #64b2db 2px solid;
    border-radius: 5px;
}
.grid td, .grid th{
    padding: 7px 15px;
}
.grid th{
    background: rgb(223, 243, 253);
}
.grid tr:hover{
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