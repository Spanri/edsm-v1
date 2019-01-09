<template>
    <div>
        <button
            @click="changeMenuVisibility">
            sgsdfg
        </button>
        <div class="left-dropdown-menu" v-if = "visibleStatus">
            <transition-group
                    name="slideLeft">
                <li class="dropdown-menu-item"
                    v-for = "item in options"
                    :key="item"
                    @click="selectOptionHandler">
                    {{item}}
                </li>
            </transition-group>
        </div>
	</div>
</template>

<script>
import DropdownMenu from './DropdownMenu';
import {AUTH_LOGOUT} from '../store/mutation-types'

export default {
    data: function () {
        return {
            visibleStatus: false,
            options: ['options'],
        }
    },
    methods: {
        changeMenuVisibility: function ( event ) {
            this.visibleStatus = !this.visibleStatus
        },
        selectOptionHandler: function ( event ) {
            this.visibleStatus = false
            this.$parent.$emit ( 'menuSelect', event.target.innerHTML.trim() )
        }
    },
}
</script>

<style>
.dropdown-menu-item {
    position:relative;
    display:block;
    text-decoration:none;
    color:#555;
    padding: 10px;
    background-color:#ddd;
    cursor:pointer;
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
  position:fixed;
  top:70px;
  left:10px;
  z-index:300;
  margin:0;
  background-color:transparent;
  max-height:80%;
  overflow:auto;
}
</style>
