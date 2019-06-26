<template>
    <div id="headerProfileGradient">
        <div id="headerProfile">
            <img class="avatar" :src="photo">
            <div v-if="profile.profile.first_name" class="rightPart">
                <p style="margin-top:0;padding-top:7px">
					{{profile.profile.second_name}} 
					{{profile.profile.first_name}}
					{{profile.profile.patronymic}}
				</p>
                <p>
					{{profile.profile.position}}
				</p>
            </div>
        </div>
		<p style="padding:15px;margin:0">Моя почта: {{profile.email}}</p>
    </div>
</template>

<script>
import {USER_PHOTO, path} from '../../store/mutation-types'

export default {
	name: 'headerProfile',
	data () {
		return {
		}
	},
	created() {
		this.$store.dispatch(USER_PHOTO)
	},
	computed: {
		photo(){
			console.log(this.$store.getters.getPhoto)
            return this.$store.getters.getPhoto;
        },
		profile() {
			return this.$store.getters.getProfile
		},
	},
}
</script>

<style scoped>
#headerProfileGradient{
	background: rgb(173,224,252);
	background: linear-gradient(90deg, rgb(101, 189, 236) 0%, rgb(99, 138, 211) 50%, rgb(186, 125, 236) 100%);
	color: white;
	font-size: 16px;
	margin-bottom: 20px;
	max-width: 350px;
	border-radius: 5px;
}
#headerProfile{
	padding: 15px;
	padding-bottom: 0;
	display: grid;
	grid-template-columns: max-content auto;
}
.avatar{
	margin: 8px 10px;
	margin-left: 0;
    width: 70px;
    height: 70px;
	background-color: white;
    border-radius: 10px;
}
.rightPart *{
	max-width: 210px;
	word-wrap: break-word;
	margin: 0;
	padding: 10px;
	padding-bottom: 0;
}
</style>