<template>
	<div class="account">
        <table>
            <thead>
                <tr>
                    <th v-for="key in columns"
                        :key="key"
                        @click="sortBy(key)"
                        :class="{ active: sortKey == key }">
                        {{ key | capitalize }}
                    <span class="arrow" :class="sortOrders[key] > 0 ? 'asc' : 'dsc'">
                    </span>
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="entry in filteredHeroes" :key="entry">
                    <td v-for="key in columns" :key="key">
                    {{entry[key]}}
                    </td>
                </tr>
            </tbody>
        </table>
	</div>
</template>

<script>
import { mapState } from 'vuex'

export default {
    name: 'account',
    props: {
        heroes: Array,
        columns: Array,
        filterKey: String
    },
    data: function () {
        var sortOrders = {}
        this.columns.forEach(function (key) {
        sortOrders[key] = 1
        })
        return {
        sortKey: '',
        sortOrders: sortOrders
        }
    },
    computed: {
        filteredHeroes: function () {
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
        }
    },
    filters: {
        capitalize: function (str) {
        return str.charAt(0).toUpperCase() + str.slice(1)
        }
    },
    methods: {
        sortBy: function (key) {
        this.sortKey = key
        this.sortOrders[key] = this.sortOrders[key] * -1
        }
    }
}
</script>

<style>
.account{
    /* height: 100%; */
	width: 100%;
	background: white;
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
</style>