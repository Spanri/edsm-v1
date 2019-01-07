<template>
  <div class="menu">
    <div class="menu2">
        <br>
        <div class="link">
            <a href="">Главная</a>
        </div>
        <div class="link">
            <a href="">Расписание</a>
        </div>
        <div class="link">
            <a href="">Научная работа</a>
        </div>
    </div>
  </div>
</template>

<script>
export default {
    name: 'Menu',
    data () {
        return {   
            msg: 'Welcome to Your Vue.js App'
        }
    },
    methods: {
        
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.menu2 > *{
    margin: 10px;
    margin: auto;
}
.link{
    margin: 20px;
    margin-left: 50px;
}
a{
    text-decoration: none;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 20px;
    color: white;
}
</style>