<template>
  <div>
    <el-row justify="space-between">
      <el-col :span="10">
        <carousel-adaptive  v-if="carouselData.length > 0" :img-list="carouselData" />
      </el-col>
      <el-col v-if="colData.length > 0" :span="14">
        <cover-collection :data="colData" />
      </el-col>
    </el-row>
    <el-row justify="space-between" :gutter="12" style="padding-bottom: 32px;">
      <el-col :span="Math.floor(24 / 6)" v-for="item in otherCoverData">
        <cover :image="item.img" :id="item.id" :title-text="item.title"></cover>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { getArticleList } from "../../api"

const tempData = Array()
const colData = ref(Array())
const otherCoverData = ref(Array())
const carouselData = ref(Array())
getArticleList().then((res) => {
  res.data.forEach((el: any) => {
    tempData.push(
      {
        id: el.id,
        img: el.cover ? el.cover : "",
        title: el.title
      }
    )
  })
  colData.value = tempData.slice(0, 6)
  otherCoverData.value = tempData.slice(6, 12)
  carouselData.value = tempData.slice(0, 4)

})

</script>

<style scoped>
</style>