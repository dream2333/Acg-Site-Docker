<script setup lang="ts">
//动态载入
const banner = new URL("../../assets/ac_banner.png", import.meta.url).href;
</script>
<template>
  <el-row>
    <div style="font-size: 0%">
      <el-image :src="banner" class="banner" fit="cover" />
    </div>
  </el-row>
</template>

<style scoped>
.banner {
  height: 240px;
}
</style>
