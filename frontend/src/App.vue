<script setup lang="ts">
import { useRouter } from "vue-router";
const route = useRouter();
const rate = ref()
</script>

<template>
  <el-container>
    <el-header style="margin: 0px; padding: 0px">
      <app-header />
    </el-header>
    <el-main class="main">
      <page-background />
      <el-scrollbar>
        <el-row>
          <el-col>
            <router-view key="key"  />
          </el-col>
        </el-row>
      </el-scrollbar>
    </el-main>
  </el-container>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.main {
  margin: 0px;
  padding: 0px;
  height: 100%;
  width: 100%;
  position: fixed;
  top: 0;
  bottom: 0;
}


</style>
