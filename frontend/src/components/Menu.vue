<template>
    <div class="menu">
        <div class="catalog">
            <div class="link">
                <router-link :to="{ path: '/', }">ВСЕ ДОКУМЕНТЫ</router-link>
            </div>
            <div class="link">
                <router-link :to="{ path: '/d/common', }">ОБЩИЙ ДОСТУП</router-link>
            </div>
            <div class="link">
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
.search{
    margin: 30px 50px;
    margin-bottom: 0;
    height: 35px;
    width: calc(100% - 130px);
    background-color: white;
    border: 0;
    padding: 0px 15px;
}
/**/
.catalog{
    margin-top: 50px;
}
.catalog > *{
    margin: 10px;
    margin: auto;
}
.link{
    margin: 30px 20px;
    margin-left: 50px;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 16px;
    color: #373737;
}
a{
    text-decoration: none;
    color: #373737;
}
a:hover{
    color:#347090;
    cursor: pointer;
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