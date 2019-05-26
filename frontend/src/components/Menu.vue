<template>
    <div class="menu">
        <router-link class="router-link" :to="{ path: '/documents/all', }">ВСЕ ДОКУМЕНТЫ</router-link>
        <router-link class="router-link" :to="{ path: '/documents/common', }">ОБЩИЙ ДОСТУП</router-link>
        <router-link class="router-link" :to="{ path: '/documents/myDocs', }">МОИ ДОКУМЕНТЫ</router-link>
        <router-link class="router-link" :to="{ path: '/documents/signature-request', }">НА ПОДПИСЬ</router-link>
        <router-link class="router-link" :to="{ path: '/documents/signature-success', }">ПОДПИСАННОЕ</router-link>
        <router-link class="router-link" :to="{ path: '/documents/available-to-me', }">ДОСТУПНЫ МНЕ</router-link>      
    </div>
</template>

<script>
import { } from '../store/mutation-types'

export default {
    name: 'Menu',
    data () {
        return {
        }
    },
}
</script>

<style scoped>
/* Основное */
.menu{
    background-color: #ADE0FC;
    min-width: 250px;
    font-family: 'El Messiri', sans-serif;
    font-weight: 600;
    padding-top: 40px;
}
/**/
.menu a{
    text-decoration: none;
    color: #373737;
}
.menu .router-link-exact-active{
    background: #64b2db;
}
.menu .router-link{
    font-size: 16px;
    color: #373737;
    padding: 11px 20px;
    padding-left: 50px;
	margin-top: 3px;
	margin-bottom: 3px;
	text-decoration: none;
	color: black;
	width: calc(100% - 70px);
	margin-left: 0;
	margin-right: 0;
	display: block;
}
.menu .link > router-link:hover{
    cursor: pointer;
}
@media (max-width: 500px) {
    .menu{
        min-width: 0;
        background-color: blue;
    }
    .menu *{
        min-width: 0;
    }
}
</style>