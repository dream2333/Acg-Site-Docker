<script setup lang="ts">
import { ElImage } from "element-plus/es";
import { useRouter } from "vue-router";

const router = useRouter()
defineProps(
  ["imgList"]
)
const imageTool = ref<Array<InstanceType<typeof ElImage>>>([])
const carouselHeight = ref("100px")
const resizeListener = () => {
  resizeCarousel()
}

onMounted(() => {
  window.addEventListener('resize', resizeListener)
})
onUnmounted(() => {
  window.removeEventListener('resize', resizeListener)
})
function clicked(id:any){
  router.push("/article/" + id.toString());
}
function resizeCarousel() {
  carouselHeight.value = imageTool.value[0].$el.offsetHeight + "px"
}
</script>

<template>
  <div class="container">
    <el-carousel :height="carouselHeight" class="carousel">
      <el-carousel-item v-for="i in imgList" :key="i" @click="clicked(i.id)">
        <el-image :src="i.img" fit="contain" ref="imageTool" @load="resizeCarousel" />
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<style scoped>
.carousel {
  width: 100%;
  border-radius: 10px;
}

.container {
  margin-right: 5%;
}

.carousel::-webkit-scrollbar {
  display: none;
}
</style>