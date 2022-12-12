<template>
  <div class="container" ref="img">
    <el-image class="pic" :src="image" fit="contain" @error="loadError">
      <template #error>
        <div class="image-slot">
          <el-icon>
            <icon-picture />
          </el-icon>
        </div>
      </template>
    </el-image>
    <div class="shadow" @click="linkTo"></div>
    <span class="text" @click="linkTo">
      <slot>{{titleText}}</slot>
    </span>
  </div>
</template>

<script setup lang="ts">
import { ElImage } from "element-plus/es";
import { Picture as IconPicture } from "@element-plus/icons-vue";
import { useRouter } from "vue-router";

const props = defineProps({
  image: null,
  titleText: String,
  isOuter: { type: Boolean, default: false },
  id: { type: Number, default: 1 },
});
const router = useRouter();
const img = ref<HTMLElement>();
var isLoaddingFailed = false;
//自适应大小
const resizeListener = () => {
  if (isLoaddingFailed) {
    loadError();
  }
};
//挂载时添加监听器，取消挂载时移除监听器
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
  background: var(--el-fill-color-light);
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
  background-image: linear-gradient(
    180deg,
    rgba(0, 0, 0, 0) 0%,
    rgba(0, 0, 0, 0.5) 50%,
    rgb(0, 0, 0, 1) 100%
  );
  border-radius: 10px;
  transition: all 0.6s;
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
}

.container:hover .shadow {
  background-position-y: 70%;
}

.text {
  font-size: small;
  max-width: 85%;
  white-space: nowrap;
  word-break: break-all;
  overflow: hidden;
  text-overflow: ellipsis;
  position: absolute;
  left: 5%;
  bottom: 6%;
  text-align: left;
  border-radius: 10px;
  line-height: 28px;
  color: #fff;
  transition: 0.4s;
}

.container:hover .text {
  font-size: medium;
  white-space: normal;
}
</style>
