<script setup lang="ts">
import { Search } from '@element-plus/icons-vue'
import 'element-plus/theme-chalk/display.css'
import { useRouter, useRoute } from 'vue-router';
import { getMenu, getUserInfo } from '../../api';
import { useLocalStorage } from "@vueuse/core"
const route = useRoute()
const router = useRouter()
const defaultActive = computed(() => {
  return route.path; //监听路由，控制菜单选择
})
const searchText = ref("")
const logged = ref(false);
getUserInfo().then((res) => {
  logged.value = true;
  getMenu().then((res) => {
    data[2].count = res.data.liked
    data[3].count = listItem.value.length
  })
});
const listItem = useLocalStorage("historyVideos", [])
const data = reactive([{
  itemName: "资讯",
  count: 0,
  path: "/home"
}, {
  itemName: "视频",
  count: 0,
  path: "/videoList"
}, {
  itemName: "收藏",
  count: 0,
  path: "/like"
}, {
  itemName: "看过",
  count: 0,
  path: "/history"
}])

getMenu().then((res) => {
  data[0].count = res.data.article
  data[1].count = res.data.video
})

function search() {
  if (searchText.value) {
    router.push("/search/" + searchText.value)
  }
}
</script>

<template>
  <el-row justify="center" align="middle" style="background-color: white;  margin-bottom: 16px;">
    <el-col :xs="24" :sm="16" :md="15" :lg="13">
      <el-menu :default-active="defaultActive" class="mymenu" mode="horizontal">
        <el-menu-item v-for="item in data" :index="item.path" @click="router.push(item.path)">
          <home-menu-item :text="item.itemName" :value="item.count" />
        </el-menu-item>
      </el-menu>
    </el-col>
    <el-col :xs="0" :sm="5" :md="5" :lg="4">
      <el-input v-model="searchText" class="w-50 m-2" :placeholder="logged ? '在此搜索您想要的视频' : '请登陆后再使用搜索功能'"
        :prefix-icon="Search" size="large" :disabled="!logged" @keyup.enter.native="search" />
    </el-col>
  </el-row>
</template>

<style scoped>
.mymenu {
  font-size: small;
  border-style: none;
  background-color: white;
  background-color: transparent;
  height: 54px;
}

.el-menu-item {
  font-size: small;
  background-color: transparent !important;
}

.phone-qr {
  color: rgb(49, 49, 49);
  font-size: small;
  text-align: right;
  line-height: 54px;
}
</style>
