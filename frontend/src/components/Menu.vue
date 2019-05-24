<template>
    <div class="menu">
            <div class="link" :class="{active: page==1 ? true : false}" @click="page=1">
                <router-link :to="{ path: '/', }">ВСЕ ДОКУМЕНТЫ</router-link>
            </div>
            <div class="link" :class="{active: page==2 ? true : false}"  @click="page=2">
                <router-link :to="{ path: '/documents/common', }">ОБЩИЙ ДОСТУП</router-link>
            </div>
            <div class="link" :class="{active: page==3 ? true : false}" @click="page=3">
                <router-link :to="{ path: '/documents/myDocs', }">МОИ ДОКУМЕНТЫ</router-link>
            </div>
            <div class="link" :class="{active: page==4 ? true : false}" @click="page=4">
                <router-link :to="{ path: '/documents/signature-request', }">НА ПОДПИСЬ</router-link>
            </div>
            <div class="link" :class="{active: page==5 ? true : false}" @click="page=5">
                <router-link :to="{ path: '/documents/signature-success', }">ПОДПИСАННОЕ</router-link>
            </div>
    </div>
</template>

<script>
import {} from '../store/mutation-types'

export default {
    name: 'Menu',
    data () {
        return {
            page: 1,
        }
    },
    methods: {
        
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
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
.menu .link{
    padding: 18px 20px;
    padding-left: 50px;
    font-size: 16px;
    color: #373737;
}
.menu a{
    text-decoration: none;
    color: #373737;
}
.menu .link > router-link:hover{
    cursor: pointer;
}
/**/
.menu .active{
    background: #64b2db;
}
/**/
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