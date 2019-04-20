<template>
	<div class="account">
		<p>ID {{id}}</p>
		<form id="search">
			Поиск по всем столбцам <input name="query" v-model="searchQuery">
		</form>
		<Grid
			:heroes="gridData"
			:columns="gridColumns"
			:filter-key="searchQuery">
		</Grid>
	</div>
</template>

<script>
import { mapState } from 'vuex'
import Grid from '../components/Grid';

export default {
	name: 'account',
	components: { Grid },
	props: {
		id: String,
	},
	data() {
		return {
			searchQuery: '',
			gridColumns: ['Номер', 'Название', 'Инициатор', 'Столбец', 'Дата инициирования'],
			
		}
	},
	computed: {
		gridData() {
			if (this.id == "all") {
				return [
					{ 
						'Номер': 'Chuck Norris', 
						'Название': Infinity,
						'Инициатор': 'dfg11',
						'Столбец': 'dfg'
					},
					{ 
						'Номер': 'Bruce Lee', 
						'Название': 9000,
						'Инициатор': 'dfkkkg',
						'Столбец': 'dfg'
					},
					{ 
						'Номер': 'Jackie Chan', 
						'Название': 7000,
						'Инициатор': 'dbbbfg',
						'Столбец': 'dfg'
					},
					{ 
						'Номер': 'Jet Li', 
						'Название': 8000,
						'Инициатор': 'dvvvfg',
						'Столбец': 'dfg'
					}
				];
			}
			if (this.id == "common") {
				return [
					{ 
						'Номер': '1', 
						'Название': Infinity,
						'Инициатор': 'dfg11',
						'Столбец': 'dfg'
					},
					{ 
						'Номер': '2 Lee', 
						'Название': 9000,
						'Инициатор': 'dfkkkg',
						'Столбец': 'dfg'
					},
					{ 
						'Номер': 'Jackie 3', 
						'Название': 7000,
						'Инициатор': 'dbbbfg',
						'Столбец': 'dfg'
					},
					{ 
						'Номер': 'Jet 4', 
						'Название': 8000,
						'Инициатор': 'dvvvfg',
						'Столбец': 'dfg'
					}
				];
			}
			if (this.id == "mydoc") {
				return [
					{ 
						'Номер': '1', 
						'Название': 'uiik',
						'Инициатор': 'dfg11',
						'Столбец': 'dfg'
					},
					{ 
						'Номер': '2 Lnghnghee', 
						'Название': 9000,
						'Инициатор': 'dfkkkg',
						'Столбец': 'dfg'
					},
					{ 
						'Номер': 'Jacghngnkie 3', 
						'Название': 7000,
						'Инициатор': 'dbbbfg',
						'Столбец': 'dfg'
					},
					{ 
						'Номер': 'Jetfgnhh 4', 
						'Название': 8000,
						'Инициатор': 'dvvvfg',
						'Столбец': 'dfg'
					}
				];
			}
		}
	}
}
</script>

<style>
.account{
	width: 100%;
	background: white;
}
.account > *{
	padding: 25px;
}
/* Поля ввода */
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