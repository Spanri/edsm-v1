<template>
    <div class="headerProfileGradient">
        <div class="headerProfile">
            <img class="avatar">
            <div v-if="profile.first_name">
                <p style="font-size:24px;">
					{{profile.second_name}}
					{{profile.first_name}}
					{{profile.patronymic}}
				</p>
                <p>{{profile.position}}</p>
            </div>
        </div>
    </div>
</template>

<script>
import {USER_REQUEST} from '../../store/mutation-types'

export default {
	name: 'account',
	created(){
		return this.$store.dispatch(USER_REQUEST, this.$store.getters.token)
	},
	computed: {
		profile: function(){
			return this.$store.getters.getProfile.profile
		}
	},
	methods: {
		
	}
}
</script>

<style>
.headerProfileGradient{
	background: radial-gradient(1448.86px at 0% 100%, #ADE0FC 0%, #93ADDF 53.65%, #DFB8FE 100%);
}
.headerProfile{
    max-width: 900px;
	margin: auto;
	color: white;
	font-size: 18px;
	font-family: serif;
	display: grid;
	grid-template-columns: max-content auto;
}
.avatar{
	margin: 10px 60px;
	margin-left: 0;
    width: 100px;
    height: 100px;
	background-color: white;
    border-radius: 50%;
}
</style>