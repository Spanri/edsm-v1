<template>
    <div id="adm">
        <p v-if="error" style="color:red">{{error}}</p>
        <h3>Управление приставками к регистрационным номерам</h3>
        <table>
            <thead><tr><th>Название</th><th>Действия</th></tr>
            </thead>
            <tbody>
                <tr v-for="(entry,j) in regs" :key="j">
                    <td>
                        <div v-if="!editRegName[j]" class="editNameReg">
                            {{entry.name}}
                        </div>
                        <div v-if="editRegName[j]" class="editNameReg2">
                            <input
                                v-model="regsNew[j]"
                                type="text"
                                placeholder="Картотека"
                                style="min-width:150px;margin-left:-8px"
                            />
                            <svg @click="editRegName.splice(j, 1, false);regsNew.splice(j, 1, regs[j].name);" style="margin-left: 10px;cursor: pointer;margin-top: 7px;" height="22px" viewBox="0 0 33 33" width="22px" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                                <g id="Cancel" stroke="black" stroke-width="1">
                                    <path clip-rule="evenodd" d="M16,0C7.163,0,0,7.163,0,16c0,8.836,7.163,16,16,16   c8.836,0,16-7.163,16-16C32,7.163,24.836,0,16,0z M16,30C8.268,30,2,23.732,2,16C2,8.268,8.268,2,16,2s14,6.268,14,14   C30,23.732,23.732,30,16,30z" 
                                        fill="#121313" fill-rule="evenodd"/>
                                    <path clip-rule="evenodd" d="M22.729,21.271l-5.268-5.269l5.238-5.195   c0.395-0.391,0.395-1.024,0-1.414c-0.394-0.39-1.034-0.39-1.428,0l-5.231,5.188l-5.309-5.31c-0.394-0.396-1.034-0.396-1.428,0   c-0.394,0.395-0.394,1.037,0,1.432l5.301,5.302l-5.331,5.287c-0.394,0.391-0.394,1.024,0,1.414c0.394,0.391,1.034,0.391,1.429,0   l5.324-5.28l5.276,5.276c0.394,0.396,1.034,0.396,1.428,0C23.123,22.308,23.123,21.667,22.729,21.271z" 
                                        fill="#121313" fill-rule="evenodd"/>
                                </g>
                            </svg>
                            <svg @click="editNameReg(j)" style="margin-left: 10px;cursor: pointer;margin-top: 7px;" height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg">
                                <path class="heroicon-ui" d="M6.3 12.3l10-10a1 1 0 0 1 1.4 0l4 4a1 1 0 0 1 0 1.4l-10 10a1 1 0 0 1-.7.3H7a1 1 0 0 1-1-1v-4a1 1 0 0 1 .3-.7zM8 16h2.59l9-9L17 4.41l-9 9V16zm10-2a1 1 0 0 1 2 0v6a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6c0-1.1.9-2 2-2h6a1 1 0 0 1 0 2H4v14h14v-6z"/>
                            </svg>
                        </div>
                    </td>
                    <td>
                        <button v-if="!editRegName[j]" @click="editRegName.splice(j, 1, true)" type="button" style="margin-top:0;">ПЕРЕИМЕНОВАТЬ</button>
                        <button type="button" style="margin-top:0;" @click="deleteReg(j)">УДАЛИТЬ ПРИСТАВКУ</button> <br>
                    </td>
                </tr>
                <tr>
                    <p @click='isAddReg=true' v-if="!isAddReg" class="addRegP" style="margin:0;padding:10px;padding-left:15px;">Добавить приставку</p>
                </tr>
            </tbody>
        </table>
        <form v-if="isAddReg" @submit.prevent="addReg" style="margin-bottom:40px">
            <p @click='isAddReg=false' class="addRegP">Скрыть добавление приставки</p>
            <h3>Создать приставку</h3>
            <input
                required
                v-model="reg"
                type="text" 
                placeholder="Введите название картотеки"
            />
            <button type="submit">СОЗДАТЬ</button> <br>
        </form>
        <div style="margin-bottom:40px"></div>
        <hr>
        <h3>Управление картотеками</h3>
        <table>
            <thead><tr><th>Название</th><th>Действия</th></tr>
            </thead>
            <tbody>
                <tr v-for="(entry,j) in fileCabinets" :key="j">
                    <td>
                        <div v-if="!editFileCabinetName[j]" class="editNameFileCabinet">
                            {{entry.name}}
                        </div>
                        <div v-if="editFileCabinetName[j]" class="editNameFileCabinet2">
                            <input
                                v-model="fileCabinetsNew[j]"
                                type="text"
                                placeholder="Картотека"
                                style="min-width:150px;margin-left:-8px"
                            />
                            <svg @click="editFileCabinetName.splice(j, 1, false);fileCabinetsNew.splice(j, 1, fileCabinets[j].name);" style="margin-left: 10px;cursor: pointer;margin-top: 7px;" height="22px" viewBox="0 0 33 33" width="22px" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                                <g id="Cancel" stroke="black" stroke-width="1">
                                    <path clip-rule="evenodd" d="M16,0C7.163,0,0,7.163,0,16c0,8.836,7.163,16,16,16   c8.836,0,16-7.163,16-16C32,7.163,24.836,0,16,0z M16,30C8.268,30,2,23.732,2,16C2,8.268,8.268,2,16,2s14,6.268,14,14   C30,23.732,23.732,30,16,30z" 
                                        fill="#121313" fill-rule="evenodd"/>
                                    <path clip-rule="evenodd" d="M22.729,21.271l-5.268-5.269l5.238-5.195   c0.395-0.391,0.395-1.024,0-1.414c-0.394-0.39-1.034-0.39-1.428,0l-5.231,5.188l-5.309-5.31c-0.394-0.396-1.034-0.396-1.428,0   c-0.394,0.395-0.394,1.037,0,1.432l5.301,5.302l-5.331,5.287c-0.394,0.391-0.394,1.024,0,1.414c0.394,0.391,1.034,0.391,1.429,0   l5.324-5.28l5.276,5.276c0.394,0.396,1.034,0.396,1.428,0C23.123,22.308,23.123,21.667,22.729,21.271z" 
                                        fill="#121313" fill-rule="evenodd"/>
                                </g>
                            </svg>
                            <svg @click="editNameFileCabinet(j)" style="margin-left: 10px;cursor: pointer;margin-top: 7px;" height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg">
                                <path class="heroicon-ui" d="M6.3 12.3l10-10a1 1 0 0 1 1.4 0l4 4a1 1 0 0 1 0 1.4l-10 10a1 1 0 0 1-.7.3H7a1 1 0 0 1-1-1v-4a1 1 0 0 1 .3-.7zM8 16h2.59l9-9L17 4.41l-9 9V16zm10-2a1 1 0 0 1 2 0v6a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6c0-1.1.9-2 2-2h6a1 1 0 0 1 0 2H4v14h14v-6z"/>
                            </svg>
                        </div>
                    </td>
                    <td>
                        <button v-if="!editFileCabinetName[j]" @click="editFileCabinetName.splice(j, 1, true)" type="button" style="margin-top:0;">ПЕРЕИМЕНОВАТЬ</button>
                        <button type="button" style="margin-top:0;" @click="deleteFileCabinet(j)">УДАЛИТЬ КАРТОТЕКУ</button> <br>
                    </td>
                </tr>
                <tr>
                    <p @click='isAddFileCab=true' v-if="!isAddFileCab" class="addFileCabP" style="margin:0;padding:10px;padding-left:15px;">Добавить картотеку</p>
                </tr>
            </tbody>
        </table>
        <form v-if="isAddFileCab" @submit.prevent="addFileCabinet" style="margin-bottom:40px">
            <p @click='isAddFileCab=false' class="addFileCabP">Скрыть добавление картотеки</p>
            <h3>Создать картотеку</h3>
            <input
                required
                v-model="fileCabinet"
                type="text" 
                placeholder="Введите название картотеки"
            />
            <button type="submit">СОЗДАТЬ</button> <br>
        </form>
        <div style="margin-bottom:40px"></div>
        <hr>
        <h3>Управление пользователями</h3>
        <table>
            <thead>
                <tr>
                    <th v-for="(col,j) in columns" :key="j">
                        {{col.name}}
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(entry,j) in filteredEvents" :key="j">
                    <td v-for="(key,i) in columns" :key="i">
                        <div class="editAdm" v-if="key.code=='is_staff'">
                            {{entry[key.code]}}
                            <svg @click="entry[key.code]=!entry[key.code];editStaff(entry)" class="editStaff" width="42" height="22" xmlns="http://www.w3.org/2000/svg">
                                <g>
                                    <path id="svg_2" d="m9.27039,21.301735l21.915211,0c5.075562,0 9.204388,-4.656818 9.204388,-10.381443s-4.128826,-10.381445 -9.204388,-10.381445l-21.915211,0c-5.07556,0 -9.204386,4.65682 -9.204386,10.381445s4.128826,10.381443 9.204386,10.381443zm0,-19.774178l21.915211,0c4.59211,0 8.327774,4.213385 8.327774,9.392735s-3.735664,9.392735 -8.327774,9.392735l-21.915211,0c-4.592112,0 -8.327778,-4.213383 -8.327778,-9.392735s3.735666,-9.392735 8.327778,-9.392735z"/>
                                    <path id="svg_3" v-if="!entry[key.code]" d="m10.851694,17.103909c3.539827,0 6.419889,-2.827057 6.419889,-6.301741s-2.880062,-6.301731 -6.419889,-6.301731s-6.419897,2.827055 -6.419897,6.301731s2.880064,6.301741 6.419897,6.301741zm0,-11.495476c2.917307,0 5.291121,2.33012 5.291121,5.193735s-2.373814,5.193739 -5.291121,5.193739s-5.291124,-2.330116 -5.291124,-5.193739s2.373245,-5.193735 5.291124,-5.193735z"/>
                                    <path id="svg_8" v-if="entry[key.code]" d="m28.549137,17.339874c3.539829,0 6.419888,-2.827057 6.419888,-6.301739s-2.880058,-6.301733 -6.419888,-6.301733s-6.419895,2.827055 -6.419895,6.301733s2.880062,6.301739 6.419895,6.301739zm0,-11.495476c2.917309,0 5.291119,2.33012 5.291119,5.193737s-2.37381,5.193737 -5.291119,5.193737s-5.291126,-2.330116 -5.291126,-5.193737s2.373245,-5.193737 5.291126,-5.193737z"/>
                                </g>
                            </svg>
                        </div>
                        <div class="editNotif" v-else-if="key.code=='is_get_notif_email'">
                            {{entry[key.code]}}
                            <svg @click="entry[key.code]=!entry[key.code];editNotif(entry)" class="editNotif2" width="42" height="22" xmlns="http://www.w3.org/2000/svg">
                                <g>
                                    <path id="svg_2" d="m9.27039,21.301735l21.915211,0c5.075562,0 9.204388,-4.656818 9.204388,-10.381443s-4.128826,-10.381445 -9.204388,-10.381445l-21.915211,0c-5.07556,0 -9.204386,4.65682 -9.204386,10.381445s4.128826,10.381443 9.204386,10.381443zm0,-19.774178l21.915211,0c4.59211,0 8.327774,4.213385 8.327774,9.392735s-3.735664,9.392735 -8.327774,9.392735l-21.915211,0c-4.592112,0 -8.327778,-4.213383 -8.327778,-9.392735s3.735666,-9.392735 8.327778,-9.392735z"/>
                                    <path id="svg_3" v-if="!entry[key.code]" d="m10.851694,17.103909c3.539827,0 6.419889,-2.827057 6.419889,-6.301741s-2.880062,-6.301731 -6.419889,-6.301731s-6.419897,2.827055 -6.419897,6.301731s2.880064,6.301741 6.419897,6.301741zm0,-11.495476c2.917307,0 5.291121,2.33012 5.291121,5.193735s-2.373814,5.193739 -5.291121,5.193739s-5.291124,-2.330116 -5.291124,-5.193739s2.373245,-5.193735 5.291124,-5.193735z"/>
                                    <path id="svg_8" v-if="entry[key.code]" d="m28.549137,17.339874c3.539829,0 6.419888,-2.827057 6.419888,-6.301739s-2.880058,-6.301733 -6.419888,-6.301733s-6.419895,2.827055 -6.419895,6.301733s2.880062,6.301739 6.419895,6.301739zm0,-11.495476c2.917309,0 5.291119,2.33012 5.291119,5.193737s-2.37381,5.193737 -5.291119,5.193737s-5.291126,-2.330116 -5.291126,-5.193737s2.373245,-5.193737 5.291126,-5.193737z"/>
                                </g>
                            </svg>
                        </div>
                        <div v-else>
                            {{entry[key.code]}}
                        </div>
                    </td>
                </tr>
                <tr>
                    <p @click='isAddUser=true' v-if="!isAddUser" class="addUserP" style="margin:0;padding:10px;padding-left:15px;">Добавить пользователя</p>
                </tr>
            </tbody>
        </table>
        <p v-if="error2" style="color:red">{{error2}}</p>
        <form v-if="isAddUser" @submit.prevent="addUser" style="margin-bottom:40px">
            <p @click='isAddUser=false' class="addUserP">Скрыть добавление пользователя</p>
            <h3>Создать пользователя</h3>
            <p>Email того, кому нужно создать аккаунт</p>
            <input
                required
                v-model="email"
                type="email" 
                placeholder="Введите email"
            />
            <canvas ref="canvas" width="100" height="100" v-insert-message="email[0]"></canvas>
            <img :src=img style="display:none">
            <p style="display: inline-block;padding-left:15px;padding-right:7px"> Администратор</p>
            <input class="checkbox" type="checkbox" name="common" true-value="1"  false-value="0" v-model="is_staff">
            <br>
            <button type="submit">СОЗДАТЬ</button> <br>
        </form>
    </div>
</template>

<script>
import {
    AUTH_SIGNUP, 
    USERS_REQUEST, 
    USER_UPDATE_OTHER,
    DOCS_FILE_CABINET, 
    DOCS_REGS,
    DOCS_REG_CREATE, 
    DOCS_REG_EDIT,
    DOCS_REG_DELETE,
    DOCS_FILTER,
    DOCS_FILE_CABINET_CREATE, 
    DOCS_FILE_CABINET_EDIT,
    DOCS_FILE_CABINET_DELETE,
} from '../../store/mutation-types'

export default {
    name: 'adm',
    data () {
        return {
            self_id: this.$store.getters.getProfile.id,
            reg: '',
            regsNew: [],
            editRegName: [],
            isAddReg: '',
            fileCabinet: '',
            fileCabinetsNew: [],
            editFileCabinetName: [],
            isAddFileCab: false,
            isAddUser: false,
            users: [],
            email: '',
            is_staff: false,
            error: '',
            error2: '',
            img: '',
            columns: [
                {
                    name: 'Пользователь',
                    code: 'full_name'
                },
                {
                    name: 'Email',
                    code: 'email'
                },
                {
                    name: 'Администратор',
                    code: 'is_staff'
                },
                {
                    name: 'Уведомления на почту',
                    code: 'is_get_notif_email'
                },
            ],
        }
    },
    created(){
        this.$store.dispatch(DOCS_FILTER)
        this.$store.dispatch(DOCS_REGS)
        for(let i=0;i<this.fileCabinets.length;i++){
            this.editFileCabinetName.push(false);
        }
        for(let i=0;i<this.fileCabinets.length;i++){
            this.fileCabinetsNew.push(this.fileCabinets[i].name)
        }
        this.$store.dispatch(USERS_REQUEST)
        .then(resp=>{
            this.users = resp
        })
    },
    directives: {
        insertMessage(canvasElement, binding, vnode) {
            var ctx = canvasElement.getContext("2d");
            ctx.clearRect(0, 0, 100, 100);
            ctx.fillStyle = "#347090";
            ctx.font = "80px Comic Sans MS";
            ctx.fillText(binding.value, 30, 70);

            var canvas = vnode.context.$refs.canvas;
            vnode.context.img = canvas.toDataURL("image/png");
        }
    },
    computed: {
        filteredEvents() {
            return this.users.filter(
                user => this.self_id != user.id
            )
        },
        fileCabinets() {
            return this.$store.getters.getFileCabinets;
        },
        regs() {
            return this.$store.getters.getRegs;
        },
    },
    methods: {
        addUser(){
            let reg = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,24}))$/
            let isVaid = (this.email == "") ? "" : (reg.test(this.email));
            if (isVaid == false) {
                this.error2 = 'Неправильный email.'
            } else {
                this.error2 = 'Пользователь создается...'

                var d = new FormData();
                console.log(this.email)
                d.append('email', this.email);
                this.is_staff ? d.append('is_staff', true) : d.append('is_staff', false);
                console.log(this.img);
                d.append('photo', this.img);
                this.$store.dispatch(AUTH_SIGNUP, d)
                .then((resp) => {
                    this.email = ''
                    this.error2 = 'Пользователь создан.'
                })
                .catch(err=>{
                    console.log(err)
                    this.error2 = 'Пользователь не создан. Такой пользователь уже существует.'
                });
            }
        },
        addFileCabinet(){
            this.$store.dispatch(DOCS_FILE_CABINET_CREATE, this.fileCabinet)
            .then((resp) => {
                this.fileCabinet = ''
                this.error = 'Картотека создана.'
            })
            .catch(err=>{
                console.log(err)
                this.error = 'Картотека не создана. Что-то пошло не так.'
            });
        },
        editNameFileCabinet(j){
            this.$store.dispatch(DOCS_FILE_CABINET_EDIT, {
                id: this.fileCabinets[j].id,
                name: this.fileCabinetsNew[j]
            })
            .then((resp) => {
                this.editFileCabinetName[j] = false;
                this.fileCabinetsNew.splice(j, 1, '');
            })
            .catch(err=> {
                console.log(err)
                this.error = 'Имя не изменено. Что-то пошло не так.'
            });
        },
        async deleteFileCabinet(j){
            let res = await confirm('Вы уверены, что хотите удалить картотеку \"' + this.fileCabinets[j].name + '\"? Это действие также удалит все документы, которые есть в картотеке!', { title: 'Подтверждение' });
			if (res) {
                this.$store.dispatch(DOCS_FILE_CABINET_DELETE, {
                id: this.fileCabinets[j].id,
            })
            .then(r => {
                this.$store.commit(DOCS_FILE_CABINET, '');
                this.error = 'Картотека удалена.'
            })
            .catch(err=>{
                this.error = 'Ошибка. Что-то пошло не так.'
            })
            }
        },
        addReg(){
            this.$store.dispatch(DOCS_REG_CREATE, this.reg)
            .then((resp) => {
                this.reg = ''
                this.error = 'Приставка создана.'
            })
            .catch(err=>{
                console.log(err)
                this.error = 'Приставка не создана. Что-то пошло не так.'
            });
        },
        editNameReg(j){
            this.$store.dispatch(DOCS_REG_EDIT, {
                id: this.regs[j].id,
                name: this.regsNew[j]
            })
            .then((resp) => {
                this.editRegName[j] = false;
                this.regsNew.splice(j, 1, '');
            })
            .catch(err=> {
                console.log(err)
                this.error = 'Имя не изменено. Что-то пошло не так.'
            });
        },
        async deleteReg(j){
            let res = await confirm('Вы уверены, что хотите удалить приставку? \"' + this.regs[j].name + '\"? Это действие также удалит все документы с этой приставкой!', { title: 'Подтверждение' });
			if (res) {
                this.$store.dispatch(DOCS_REG_DELETE, {
                id: this.regs[j].id,
            })
            .then(r => {
                this.error = 'Приставка удалена.'
            })
            .catch(err=>{
                this.error = 'Ошибка. Что-то пошло не так.'
            })
            }
        },
        editStaff(user){
            this.$store.dispatch(USER_UPDATE_OTHER, {
                id: user.id,
                is_staff: user.is_staff
            })
            .catch(err=>{
                this.error = 'Ошибка. Что-то пошло не так.'
            })
        },
        editNotif(user){
            this.$store.dispatch(USER_UPDATE_OTHER, {
                id: user.id,
                is_get_notif_email: user.is_get_notif_email
            })
            .catch(err=>{
                this.error = 'Ошибка. Что-то пошло не так.'
            })
        },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* Основное */
#adm{
    margin-left: 15px;
    padding: 45px;
    padding-top: 0;
    padding-left: 60px;
}
/* Поле ввода */
input[type="email"], input[type="text"]{
	border: 0;
	margin: 0;
    height: 35px;
    padding-left: 15px;
	padding-right: 15px;
    min-width: 350px;
    background: rgb(223, 243, 253);
}
/**/
input[type="checkbox"]{
    height: 15px;
    width: 15px;
    margin: 0;
    vertical-align: middle;
}
/* Картотеки */
.fileCabinet, .reg{
    border: #347090 1px solid;
    border-bottom: 0;
    padding: 5px;
}
.editNameFileCabinet, .editNameReg{
    display: grid;
	grid-template-columns: 1fr auto;
}
.editNameFileCabinet2, .editNameReg2{
    display: grid;
	grid-template-columns: 1fr auto auto;
}
.addFileCabP:hover, .addUserP:hover, .addRegP:hover{
    cursor: pointer;
}
/**/
table {
    border-collapse: collapse;
    text-align: left;
}
table, th, td{
    border: #64b2db 2px solid;
    border-radius: 5px;
}
th{
    background: rgb(223, 243, 253);
}
td, th{
    padding: 7px 15px;
}
.arrow{
    display: inline-block;
}
.editAdm{
    display: grid;
	grid-template-columns: 1fr auto;
}
.editNotif{
    display: grid;
	grid-template-columns: 1fr auto;
}
.editStaff, .editNotif2{
    fill: #64b2db;
    vertical-align: text-bottom;
    text-align: right;
}
.editStaff:hover, .editNotif2:hover{
    cursor: pointer;
    fill: #347090;
}
/**/
hr { 
    overflow: visible;
    border: 0;
    margin-left: -2px;
    border-top: dotted #347090 4px;
} 
/**/
canvas {
    border: 1px solid #BBB;
    display: none;
}
</style>