<template>
    <div id="preview">
        <div class="bb0"></div>
        <div class="bb1">
            <div class="bb2"></div>
        </div>
        <div></div>
        <p>{{typeFile.toUpperCase()}}</p>
        <div></div>
    </div>
</template>

<script>
export default {
    name: 'preview',
    props: {
        typeFile: { type: String, default: ""},
    },
}
</script>

<style scoped>
#preview{
    border: 4px solid #5a95b4;
    border-radius: 10px;
    margin-right: 15px;
    text-align: center;
    width: 80px;
    height: 110px;
    display: grid;
    grid-template-rows: auto auto 1fr auto 1fr;
}
p{
    border: 4px solid #5a95b4;
    border-radius: 5px;
    background: rgb(255, 255, 255);
    text-align: center;
    vertical-align: middle;
    width: auto;
    padding: 5px;
    height: auto;
    margin: auto;
    margin-right: -15px;
    color: #5a95b4;
    font-weight: 900;
    font-size: 18px;
}
.bb0{
    width: 40px;
    height: 40px;
    border: 0;
    margin-top:-5px;
    margin-left:-5px;
    background: white;
}
.bb1{
    margin-top:-35px;
    width: 35px;
    height: 35px;
    border: 5px solid #5a95b4;
    border-width: 0 5px 5px 0;
    border-radius: 0 0 5px 0;
}
.bb2{
    width: 55px;
    height: 17px;
    border: 5px solid #5a95b4;
    border-width: 0 0 5px 0;
    margin-left: -16px;
    transform: rotate(-45deg)
}
</style>