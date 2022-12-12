<template>
  <el-row justify="center" style="margin-top: 64px;">
  <el-col :span="12">
    <el-card>
      <md-editor v-model="text" previewOnly class="content" />
    </el-card>
    </el-col>
  </el-row>
</template>

<script setup lang="ts">
import MdEditor from "md-editor-v3";
const text = `
### 关于我们


>  Follow your heart.

![](https://pandao.github.io/editor.md/examples/images/8.jpg)

  此处为Markdown测试
  `
</script>

<style scoped>
</style>