<template>
  <el-row justify="center">
    <el-col :span="17" style="line-height: 64px">
      <el-card style="margin-top: 8px">
        <el-page-header
          :icon="ArrowLeft"
          content="首页"
          @back="router.back()"
          style="margin: 8px"
        />
        <el-row justify="center">
          <div class="title">{{ title }}</div>
        </el-row>
        <el-row justify="center">
          <div class="sub">作者：{{ author }}</div>
          <div class="sub">时间：{{ timestamp }}</div>
        </el-row>
        <el-row justify="center">
          <el-skeleton :rows="6" animated v-if="!show"  class="content" style="margin-top:100px"/>
          <md-editor
            v-model="text"
            previewOnly
            class="content"
            @onHtmlChanged="show = true"
          />
        </el-row>
      </el-card>
    </el-col>
    <el-col></el-col>
  </el-row>
</template>

<script setup lang="ts">
import { getArticle } from "../../api";
import { useRoute, useRouter } from "vue-router";
import { ArrowLeft } from "@element-plus/icons-vue";
import { toInteger } from "lodash";
import MdEditor from "md-editor-v3";
import "md-editor-v3/lib/style.css";
const router = useRouter();
const route = useRoute();
const text = ref("");
const title = ref("");
const author = ref("");
const timestamp = ref("");
const show = ref(false);
getArticle(toInteger(route.params.id)).then((res) => {
  text.value = res.data.text;
  title.value = res.data.title;
  author.value = res.data.username;
  timestamp.value = timeFormat(res.data.timestamp);
});

function timeFormat(arg: string) {
  return arg.substring(0, 16).replace("T", " ");
}
</script>

<style scoped>
.title {
  margin-top: 24px;
  font-size: xx-large;
  font-weight: bold;
  justify-content: center;
}
.content {
  padding-left: 120px;
  padding-right: 120px;
  margin-bottom: 72px;
}
.sub {
  font-size: small;
  font-weight: 100;
  margin-left: 32px;
  margin-right: 32px;
  color: rgb(167, 164, 164);
}
</style>
