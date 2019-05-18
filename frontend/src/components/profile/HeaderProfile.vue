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
                <p style="font-size:16px;margin-top:2px">
					{{profile.position}}
				</p>
            </div>
        </div>
    </div>
</template>

<script>
import {USER_REQUEST} from '../../store/mutation-types'

export default {
	name: 'headerProfile',
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
	font-family: 'El Messiri', sans-serif;
    max-width: 900px;
	margin: auto;
	color: white;
	font-size: 18px;
	display: grid;
	grid-template-columns: max-content auto;
}
.headerProfile p{
	margin-top: 13px;
	color: white;
	font-size: 18px;
}
.avatar{
	margin: 8px 30px;
	margin-left: 0;
    width: 70px;
    height: 70px;
	background-color: white;
    border-radius: 30%;
}
</style>