<template>
    <div class="headerProfileGradient">
        <div class="headerProfile">
            <img class="avatar" :src="profile.photo">
            <div v-if="profile.first_name">
                <p style="font-size:20px;margin-bottom:0">
					{{profile.second_name}}
					{{profile.first_name}}
					{{profile.patronymic}}
				</p>
                <p style="font-size:16px;margin-top:5px">
					{{profile.position}}
				</p>
            </div>
        </div>
    </div>
</template>

<script>
import {USER_REQUEST} from '../../store/mutation-types'

export default {
	name: 'account',
	created(){
		console.log(this.$store.getters.getProfile.profile);
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
	margin: 8px 40px;
	margin-left: 0;
    width: 70px;
    height: 70px;
	background-color: white;
    /* border-radius: 50%; */
}
</style>