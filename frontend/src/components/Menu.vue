<template>
    <div class="menu">
        <input class="search" v-model="message" placeholder="Искать...">
        <p class="link editLink">РЕДАКТИРОВАТЬ ПАПКИ</p>
        <div class="catalog">
            <div class="link">
                <a href="">ВСЕ ДОКУМЕНТЫ</a>
            </div>
            <div class="link">
                <a href="">ОБЩИЙ ДОСТУП</a>
            </div>
            <div class="link">
                <a href="">МОИ ДОКУМЕНТЫ</a>
            </div>
            <div class="link" v-for="item in items" :key='item'>
                <a href="">{{item}}</a>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Menu',
    data () {
        return {   
            items: [
                "ДОКУМЕНТЫ СТУДЕНТОВ",
                "ДРУГИЕ ДОКУМЕНТЫ"
            ]
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
    min-width: 350px;
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
.editLink{
    margin-bottom:50px;
    color:#347090;
}
.editLink:hover{
    cursor: pointer;
    color:#ffffff;
}
a{
    text-decoration: none;
    color: #373737;
}
a:hover{
    color:#347090;
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