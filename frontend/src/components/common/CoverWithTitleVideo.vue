<template>
  <div class="container" ref="img" @click="linkTo">
    <el-image class="pic" :src="image" fit="contain" @error="loadError">
      <template #error>
        <div class="image-slot">
          <el-icon>
            <icon-picture />
          </el-icon>
        </div>
      </template>
    </el-image>

    <div class="shadow"></div>
  </div>
  <div class="text" @click="linkTo" style="cursor: pointer;">
    <slot>{{ titleText }}</slot>
  </div>
  <div class="text2">作者：{{ author }}</div>
</template>

<script setup lang="ts">
import { ElImage } from "element-plus/es";
import { Picture as IconPicture } from "@element-plus/icons-vue";
import { useRouter } from "vue-router";

const props = defineProps({
  image: null,
  titleText: String,
  author: { type: String, default: "无名氏" },
  id: { type: Number, default: 1 },
});
const router = useRouter();

const img = ref<HTMLElement>();
var isLoaddingFailed = false;
const resizeListener = () => {
  if (isLoaddingFailed) {
    loadError();
  }
};
onMounted(() => {
  window.addEventListener("resize", resizeListener);
});
onUnmounted(() => {
  window.removeEventListener("resize", resizeListener);
});
function loadError() {
  isLoaddingFailed = true;
  const imgStyle = img.value!.style;
  imgStyle.height = img.value!.offsetWidth * 0.625 + "px";
}
function linkTo() {
  router.push("/video/" + props.id.toString());
}
</script>

<style scoped>
.image-slot {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;

  color: var(--el-text-color-secondary);
  font-size: 30px;
}

.pic {
  cursor: pointer;
  border-radius: 10px;
}

.shadow {
  position: absolute;
  left: 0px;
  bottom: 0px;
  width: 100%;
  height: 100%;
  background-color: #00000000;
  border-radius: 10px;
  transition: all 1s;
  background-size: auto 200%;
  background-position-y: 0%;
}

.container {
  justify-content: center;
  cursor: pointer;
  position: relative;
  align-items: center;
  display: flex;
  overflow: hidden;
  background-color: #90939934;
  border-radius: 10px;
}

.container:hover .shadow {
  background-position-y: 70%;
  background-color: rgba(44, 44, 44, 0.342);
}

.text {
  text-align: left;
  font-size: medium;
  color: #303133;
  width: 100%;
  max-width: 90%;
  white-space: nowrap;
  word-break: break-all;
  overflow: hidden;
  text-overflow: ellipsis;
  padding-top: 4px;
  border-radius: 10px;
  line-height: 18px;
  transition: 0.4s;
}

.text2 {
  text-align: left;
  font-size: smaller;
  color: #909399;
  width: 100%;
  max-width: 90%;
  white-space: nowrap;
  word-break: break-all;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 18px;
  border-radius: 10px;
  transition: 0.4s;
}
</style>
