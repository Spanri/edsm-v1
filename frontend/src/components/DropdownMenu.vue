<template>
    <div class="dropdownMenu">
        <img 
            class="profile-img"
            src="../assets/logo.png"
            alt="Профиль"
            @click="changeMenuVisibility"
        >
        <div class="a" v-if = "visibleStatus">
            <div class="left-dropdown-menu" v-if = "visibleStatus">
                <transition-group
                        name="slideLeft">
                    <li class="registr"
                        v-for = "item in options"
                        :key="item"
                        @click="dropdownMenuClick(item)">
                        {{item}}
                    </li>
                </transition-group>
            </div>
        </div>
	</div>
</template>

<script>
import {AUTH_LOGOUT} from '../store/mutation-types'

export default {
    data: function () {
        return {
            visibleStatus: false,
        }
    },
    props: ['options'],
    computed: {
        profileImg() {
            return './assets/logo.png';
        }
    },
    methods: {
        changeMenuVisibility: function ( event ) {
            this.visibleStatus = !this.visibleStatus
        },
        logout () {
			this.$store.dispatch(AUTH_LOGOUT)
			.then(() => {
				this.$router.push('/auth')
			});
        },
        dropdownMenuClick(item) {
            this.visibleStatus = false
            switch(item) {
                case 'Профиль':
                    this.$router.push('/account')
                    break;
                case 'Выйти':
                    this.logout();
                    break;
                default:
                    break;
            }
        }
    },
}
</script>

<style>
.dropdownMenu {
    position: relative;
}
.profile-img {
    width: 40px;
}

.profile-img:hover{
    cursor: pointer;
}

.dropdown-menu-item {
    position: absolute;
    display: block;
    text-decoration: none;
    color:#555;
    padding: 10px;
    background-color:#ddd;
    cursor: pointer;
    text-overflow: ellipsis;
    animation: show-item-left 1s;
}
.dropdown-menu-item:before {
	content: "\2756 \0020";
}
.dropdown-menu-item:hover {
    border:dashed 1px #777;
    background-color:#555;
    color:white;
}
.dropdown-menu-item:hover:before {
	content: "\27A0 \0020";
}

.left-dropdown-menu {
    position: absolute;
    top: 45px;
    right: 0px;
    z-index: 300;
    margin: 0;
    background-color: #7cb0c1;
    min-width: 150px;
    /* max-height: 80%; */
    overflow: auto;
}

.registr{
    text-align: center;
    list-style-type: none;
    border: 0;
    padding: 10px;
    margin: 0;
    background-color: #7cb0c1;
    color: white;
}
.a {
    z-index: 300;
}
.a::after {
    content: ''; 
    position: absolute;
    right: 10px;
    top: 20px;
    border: 15px solid transparent;
    border-bottom: 15px solid #7cb0c1;
   }
.registr:hover{
    cursor: pointer;
    background-color: #6393a3;
    transition: background-color .3s ease-out;
}
</style>
