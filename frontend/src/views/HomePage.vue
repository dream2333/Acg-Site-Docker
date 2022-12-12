<script setup lang="ts">
import "element-plus/theme-chalk/display.css";


</script>

<template>
  <div class="home">
    <banner />
    <home-menu />
    <div class="home-content">
      <router-view #default="{ Component }">
        <keep-alive>
          <component :is="Component" v-if="$route.meta.keepAlive" :key="$route.name" />
        </keep-alive>
        <component :is="Component" v-if="!$route.meta.keepAlive" :key="$route.name" />
      </router-view>
    </div>
  </div>
  <app-footer/>
</template>

<style scoped>
.home {
  position: relative;
  top: -15px;
}
</style>
