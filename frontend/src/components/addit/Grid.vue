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
                <tr v-for="(entry,j) in filteredHeroes" :key="j" @click="toDoc(entry.doc.id)">
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
import {DOCS_REQUEST, DOC_REQUEST, USER_REQUEST, USER_NOTIF_REQUEST, DOC_FOLDER_PAGE, DOC_FOLDER_PAGE_PROFILE} from '../../store/mutation-types'

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
            sortOrders: sortOrders
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
            // token: 'token',
            // getNotif: 'getNotif',
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
                return this.getDocs
                .filter(d => 
                    d.user.id == this.getProfile.id && d.is_owner && 
                    !d.is_signature_request && !d.is_signature
                );
            } else if(this.$route.params.id == 'signature-request') {
                return this.getDocs
                .filter(d =>
                    !d.is_owner && d.is_signature_request && !d.is_signature
                );
            } else if(this.$route.params.id == 'signature-success') {
                return this.getDocs
                .filter(d =>
                    !d.is_owner &&
                    d.is_signature_request && 
                    d.is_signature
                );
            } else if(this.$route.params.id == 'available-to-me') {
                return this.getDocs
                .filter(d => 
                    !d.is_owner && !d.is_signature_request
                );
            } else if(this.id == 'notif') {
                let docs = this.getDocs
                .filter(d =>
                    (
                        d.is_owner &&
                        d.is_signature_request && 
                        d.is_signature &&
                        d.is_show_notif
                    ) || (
                        !d.is_owner && 
                        d.is_signature_request && 
                        !d.is_signature
                    )
                );
                docs.forEach(d => {
                    if(
                        d.is_owner &&
                        d.is_signature_request && 
                        d.is_signature &&
                        d.is_show_notif
                    ){
                        d.message = "Ваш документ подписали."
                    }
                    if(
                        !d.is_owner && 
                        d.is_signature_request && 
                        !d.is_signature
                    ){
                        d.message = "Вас просят подписать документ."
                    }
                })
                console.log(docs);
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
        toDoc(id){
            this.$router.push('/document/'+id);
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