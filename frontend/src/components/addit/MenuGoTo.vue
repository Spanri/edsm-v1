<template>
    <div id="menuGoTo">
        <router-link @click.native="goToFolder" class="router-link" :to="{ path: path, }">
            <!-- <svg enable-background="new 0 0 50 50" height="20px" id="Layer_1" version="1.1" viewBox="0 0 50 50" width="20px" style="margin-right:15px;" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                <rect fill="none" height="50" width="50"/>
                <path :stroke="color" fill="none" d="M46,15v-4  c0-1.104-0.896-2-2-2c0,0-24.648,0-26,0c-1.469,0-2.484-4-4-4H3C1.896,5,1,5.896,1,7v4v29v4c0,1.104,0.896,2,2,2h39  c1.104,0,2-0.896,2-2" stroke-linecap="round" stroke-miterlimit="10" stroke-width="4"/>
                <path :stroke="color" fill="none" d="M1,44l5-27  c0-1.104,0.896-2,2-2h39c1.104,0,2,0.896,2,2l-5,27" stroke-linecap="round" stroke-miterlimit="10" stroke-width="4"/>
            </svg> -->
            {{text}}
        </router-link>
    </div>
</template>

<script>
import {
    DOCS_FILE_CABINET,
    DOCS_REQUEST,
    DOCS_FILTER,
    ADDIT_RELOAD,
} from '../../store/mutation-types'

export default {
    name: 'MenuGoTo',
    props: {
        path: { type: String, default: ""},
        text: { type: String, default: ""},
        color: { type: String, default: "black"},
    },
    data () {
        return {

        }
    },
    created(){

    },
    computed: {
        reload: {
            get(){
                return this.$store.getters.getReload;
            },
            set(newValue){
                this.$store.commit(ADDIT_RELOAD, newValue);
            }
        }
    },
    methods: {
        async goToFolder(){
            this.reload = true;
            await this.$store.dispatch(DOCS_REQUEST);
            await this.$store.dispatch(DOCS_FILTER);
            this.reload = false;
        }
    },
}
</script>

<style scoped>
/**/
a{
    text-decoration: none;
    color: #373737;
}
.router-link-exact-active{
    background: #64b2db;
    pointer-events: none;
    cursor: default;
}
.router-link{
    font-size: 16px;
    color: #373737;
    padding: 11px 20px;
    padding-left: 25px;
	margin-top: 3px;
	margin-bottom: 3px;
	text-decoration: none;
	color: black;
	width: calc(100% - 45px);
	margin-left: 0;
	margin-right: 0;
	display: block;
}
.link > router-link:hover{
    cursor: pointer;
}
</style>
