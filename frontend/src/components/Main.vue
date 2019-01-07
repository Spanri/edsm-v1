<template>
	<div class="main">
		<h4 v-if="authenticated">
			You are logged in!
		</h4>
		<h4 v-if="!authenticated">
			You are not logged in! Please <a @click="auth.login()">Log In</a> to continue.
		</h4>
	</div>
</template>

<script>
import axios from 'axios'

export default {
	name: 'main',
	data () {
		return {
			stories: []
		}
	},
	props: ['auth', 'authenticated'],
	computed: {
        userName(){
            if(this.$auth.isAuthenticated()){
                return this.$auth.user.name;
            }
            else {
                console.log(this.$auth.isAuthenticated());
                return 'Нет имени';
            }
        }
	},
	mounted() {
		axios.get('https://api.storyblok.com/v1/cdn/stories?starts_with=tp&excluding_fields=body&excluding_ids=48471,48547,60491&token=dtONJHwmxhdJOwKxyjlqAgtt').then((res) => {
			this.stories = res.data.stories
		})
	},
	methods: {
		getStoryLink(story) {
			return `https://www.storyblok.com/${story.full_slug}`
		}
	}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.main{
    height: 100%;
	width: 100%;
	background: white;
}
h1{
  	font-weight: normal;
	margin: 20px;
}
</style>
