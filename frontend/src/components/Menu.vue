<template>
    <div class="menu">
        <div class="catalog">
            <div class="link" :class="{active: page==1 ? true : false}" @click="page=1">
                <router-link :to="{ path: '/', }">ВСЕ ДОКУМЕНТЫ</router-link>
            </div>
            <div class="link" :class="{active: page==2 ? true : false}" @click="page=2">
                <router-link :to="{ path: '/d/common', }">ОБЩИЙ ДОСТУП</router-link>
            </div>
            <div class="link" :class="{active: page==3 ? true : false}" @click="page=3">
                <router-link :to="{ path: '/d/myDocs', }">МОИ ДОКУМЕНТЫ</router-link>
            </div>
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
    min-width: 280px;
}
/* Поиск */
.menu .search{
    margin: 30px 50px;
    margin-bottom: 0;
    height: 35px;
    width: calc(100% - 130px);
    background-color: white;
    border: 0;
    padding: 0px 15px;
}
/**/
.menu .catalog{
    margin-top: 50px;
}
.menu .catalog > *{
    margin: 10px;
    margin: auto;
}
.menu .link{
    padding: 20px 20px;
    padding-left: 50px;
    margin-top: 10px;
    margin-bottom: 10px;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 16px;
    color: #373737;
}
.menu a{
    text-decoration: none;
    color: #373737;
}
.menu .link:hover{
    color:#347090;
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