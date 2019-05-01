<template>
	<div class="account">
        <p>ID {{$route.params.id}}</p>
		<form id="search">
			Поиск по всем столбцам <input name="query" v-model="filterKey">
		</form>
        <table>
            <thead>
                <tr>
                    <th v-for="(key,i) in columns"
                        :key="i"
                        @click="sortBy(key)"
                        :class="{ active: sortKey == key }">
                        {{ key | capitalize }}
                    <span class="arrow" :class="sortOrders[key] > 0 ? 'asc' : 'dsc'">
                    </span>
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(entry,j) in filteredHeroes" :key="j">
                    <td v-for="(key,i) in columns" :key="i">
                    {{entry[key]}}
                    </td>
                </tr>
            </tbody>
        </table>
	</div>
</template>

<script>
import { mapState } from 'vuex'
import {DOCS_REQUEST} from '../store/mutation-types'

export default {
    name: 'account',
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
            sortKey: '',
            filterKey: '',
            sortOrders: sortOrders
        }
    },
    computed: {
        filteredHeroes() {
            // var sortKey = this.sortKey
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
			this.$store.dispatch(DOCS_REQUEST, this.id);
			return this.$store.getters.getDoc;
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
        }
    }
}
</script>

<style>
.account{
	width: 100%;
	background: white;
    padding: 25px;
}
.account > *{
	padding: 25px;
}
table {
    border-collapse: collapse;
}
table, th, td{
    border: #e0e0e0 3px solid;
    border-radius: 5px;
}
td, th{
    padding: 7px 15px;
}
.arrow{
    display: inline-block;
    
}
input{
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