<script setup lang="ts">
import { House, Football, User, VideoCamera, DataBoard ,Stamp} from '@element-plus/icons-vue'
import { useLocalStorage } from '@vueuse/core';
import { ElMessage } from 'element-plus';
import 'element-plus/theme-chalk/display.css'
import { useRouter, useRoute } from 'vue-router';
import { getUserInfo, logout } from '../api';
import logo from "../assets/logo.svg";

const router = useRouter();
const showPopup = ref(false);
const username = ref("游客")
const buttonText = ref("登 录")
const avatar = ref("")
const listItem = useLocalStorage("historyVideos", [])
const tooltipContent = ref("您还未登录账号")
const route = useRoute()
const defaultActive = computed(() => {
  return route.path; //监听路由，控制菜单选择
})
const isAdmin =ref(false)
logged()
function timeFormat(arg: string) {
  return arg.substring(0, 16).replace("T", " ")
}

function logged() {
  getUserInfo().then((res) => {
    username.value = res.data["username"]
    avatar.value = res.data["avatar"]
    buttonText.value = "登 出"
    tooltipContent.value = "您上次的登录时间为： " + timeFormat(res.data["last_login"])
    showPopup.value = false
    isAdmin.value=res.data["is_superuser"]
  }).catch(() => {
    username.value = "游客"
    avatar.value = "https://s1.hdslb.com/bfs/static/jinkela/space/assets/icon-auth.png"
    buttonText.value = "登 录"
    tooltipContent.value = "您还未登录账号"
  })
}



onMounted(() => {
    window.onbeforeunload = () => {
        sessionStorage.removeItem("carList")
    }
})
function loginButtonClicked() {
  if (buttonText.value == "登 录") {
    showPopup.value = true
  }
  else {
    logout().finally(() => {
      listItem.value=[]
      localStorage.removeItem('ACCESS_TOKEN')
      window.location.reload()
      buttonText.value = "登 录"
      username.value = "游客"
      tooltipContent.value = "您还未登录账号"
      avatar.value = "https://s1.hdslb.com/bfs/static/jinkela/space/assets/icon-auth.png"
      ElMessage({
        message: "登出成功",
        type: "success",
        offset: 40
      });
    })
  }
}

function adminClick(){
  window.location.href="/admin"
}


function linkTo(str: string) {
  router.push(str)
  sessionStorage.setItem("table_actived", str);
}
</script>

<template>

  <div class="header">
    <login-dialog :show="showPopup" v-model="showPopup" @logged="logged" />
    <el-row justify="center" align="middle">
      <el-col :xs="13" :sm="16" :md="15" :lg="12">
        <el-row justify="start" align="middle">
          <el-col :xs="0" :sm="0" :md="3" :lg="3">
            <el-image :src="logo" class="logo" />
          </el-col>
          <el-col :xs="24" :sm="21" :md="21" :lg="21">
            <el-menu :default-active='defaultActive' class="mymenu" mode="horizontal">
              <el-menu-item index='/home' @click="linkTo('/home')">
                <el-icon>
                  <house />
                </el-icon>主站
              </el-menu-item>

              <el-menu-item index='/msgboard' @click="linkTo('/msgboard')">
                <el-icon>
                  <data-board />
                </el-icon>留言板
              </el-menu-item>

              <el-menu-item index='/userinfo' @click="linkTo('/userinfo')">
                <el-icon>
                  <User />
                </el-icon>个人中心
              </el-menu-item>

              <el-menu-item index='/about' @click="linkTo('/about')">
                <el-icon>
                  <User />
                </el-icon>关于
              </el-menu-item>
            </el-menu>
          </el-col>
        </el-row>
      </el-col>
      <el-col :xs="11" :sm="8" :md="8" :lg="7">
        <el-row align="middle" justify="end">
          <el-tooltip class="box-item" effect="dark" :content="tooltipContent" placement="bottom">
            <el-avatar :size="34" :src="avatar" class="avatar" @click="linkTo('/userinfo')"/>
          </el-tooltip>
          <span style="margin-left: 10px; margin-right: 16px">{{ username }}</span>
          <el-button :type="buttonText == '登 出' ? 'warning' : 'primary'" @click="loginButtonClicked"
            class="login-button">
            {{ buttonText }}
            <el-icon>
              <User />
            </el-icon>
          </el-button>
          <el-button v-if="isAdmin" type="primary" @click="adminClick" class="login-button">
            后 台
            <el-icon>
              <Stamp />
            </el-icon>
          </el-button>
        </el-row>
      </el-col>
    </el-row>
  </div>

</template>

<style scoped>
.mymenu {
  border-style: none;
  background-color: transparent;
  height: 50px;
  width: 70%;

}

.el-menu-item {
  margin-right: 32px;
  width: 70px;
  font-size: small;
  background-color: transparent !important;
  border-bottom: 0px !important;
}

.header {
  font-size: small;
  background: rgba(220, 222, 224, 0.253);
  box-shadow: 0px 1px 6px 2px rgba(46, 46, 46, 0.137);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  position: relative;
  z-index: 100000;
}

.login-button {
  padding-left: 30px;
  padding-right: 30px;
  font-size: small;
  font-weight: lighter;
}

.logo {
  height: 20px;
}

.avatar {
  cursor: pointer;

  border: 2px solid;
}
</style>