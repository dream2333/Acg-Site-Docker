<template>
  <el-row justify="center">
    <el-col :md="21" :lg="18">
      <recommend-collection></recommend-collection>
      <el-row :gutter="16" style="margin-bottom: 50px">
        <el-col :span="18">
          <div class="title-container">
            <el-row style="align-items: center">
              <heart-two-tone two-tone-color="#eb2f96" style="fontsize: 28px" />
              <span class="title-text">推荐</span>
              <span class="title-text-tip">Recommend</span>
            </el-row>
          </div>
          <el-row justify="space-between" :gutter="12" style="padding-bottom: 32px">
            <el-col :span="Math.floor(24 / 4)" v-for="i in recommendList.slice(0, 4)">
              <cover-with-title-video :image="i.cover" :id="i.id" :title-text="i.title"></cover-with-title-video>
            </el-col>
          </el-row>
          <el-row justify="space-between" :gutter="12" style="padding-bottom: 32px">
            <el-col :span="Math.floor(24 / 4)" v-for="i in recommendList.slice(4, 8)">
              <cover-with-title-video :image="i.cover" :id="i.id" :title-text="i.title"></cover-with-title-video>
            </el-col>
          </el-row>
        </el-col>
        <el-col :span="6" style="text-align: left">
          <rank-lisk :data="videoList"></rank-lisk>
        </el-col>
      </el-row>

      <el-row :gutter="16" style="margin-bottom: 50px">
        <el-col>
          <div class="title-container">
            <el-row style="align-items: center">
              <like-two-tone two-tone-color="#b31818" style="fontsize: 28px" />
              <span class="title-text">评测</span>
              <span class="title-text-tip">Rating</span>
            </el-row>
          </div>
          <el-row justify="space-between" :gutter="12" style="padding-bottom: 32px">
            <el-col :span="Math.floor(24 / 4)" v-for="i in tempData.slice(21, 25)">
              <cover-with-title :image="i.img" :id="i.id" :title-text="i.title"></cover-with-title>
            </el-col>
          </el-row>
          <el-row justify="space-between" :gutter="12" style="padding-bottom: 32px">
            <el-col :span="Math.floor(24 / 4)" v-for="i in tempData.slice(25, 29)">
              <cover-with-title :image="i.img" :id="i.id" :title-text="i.title"></cover-with-title>
            </el-col>
          </el-row>
        </el-col>
      </el-row>
      <el-row :gutter="16" style="margin-bottom: 50px">
        <el-col>
          <div class="title-container">
            <el-row style="align-items: center">
              <tag-two-tone two-tone-color="#48df5c" style="fontsize: 28px" />
              <span class="title-text">其他</span>
              <span class="title-text-tip">Other</span>
            </el-row>
          </div>
          <el-row justify="space-between" :gutter="12" style="padding-bottom: 32px">
            <el-col :span="Math.floor(24 / 6)" v-for="i in tempData.slice(29, 35)">
              <cover-with-title :image="i.img" :id="i.id" :title-text="i.title"></cover-with-title>
            </el-col>
          </el-row>
          <el-row justify="space-between" :gutter="12" style="padding-bottom: 32px">
            <el-col :span="Math.floor(24 / 6)" v-for="i in tempData.slice(35, 41)">
              <cover-with-title :image="i.img" :id="i.id" :title-text="i.title"></cover-with-title>
            </el-col>
          </el-row>
          <el-row justify="space-between" :gutter="12" style="padding-bottom: 32px">
            <el-col :span="Math.floor(24 / 6)" v-for="i in tempData.slice(41, 47)">
              <cover-with-title :image="i.img" :id="i.id" :title-text="i.title"></cover-with-title>
            </el-col>
          </el-row>
        </el-col>
      </el-row>
    </el-col>
  </el-row>

</template>

<script setup lang="ts">
import {
  LikeTwoTone,
  TagTwoTone,
  HeartTwoTone,
} from "@ant-design/icons-vue";
import { getArticleList, getVideoList } from "../../api";
const tempData = ref(Array())
const videoList = ref(Array())
const recommendList = ref(Array())
getVideoList(1, "timestamp").then((res) => {
  videoList.value = res.data.results
})

getArticleList().then((res) => {
  res.data.forEach((el: any) => {
    tempData.value.push(
      {
        id: el.id,
        img: el.cover ? el.cover : "",
        title: el.title
      }
    )
  })
})

fakeRecommend()
function getRandomArrayElements(arr: any[], count: number) {
    var shuffled = arr.slice(0), i = arr.length, min = i - count, temp, index;
    while (i-- > min) {
        index = Math.floor((i + 1) * Math.random());
        temp = shuffled[index];
        shuffled[index] = shuffled[i];
        shuffled[i] = temp;
    }
    return shuffled.slice(min);
}
function fakeRecommend() {
    getVideoList(1, "cover").then((res) => {
        recommendList.value = res.data.results
        getVideoList(2, "cover").then((res) => {
            recommendList.value = recommendList.value.concat(res.data.results)
            getVideoList(3, "cover").then((res) => {
                recommendList.value = recommendList.value.concat(res.data.results)
                getVideoList(4, "cover").then((res) => {
                    recommendList.value = recommendList.value.concat(res.data.results)
                    getVideoList(5, "cover").then((res) => {
                        recommendList.value = recommendList.value.concat(res.data.results)
                        recommendList.value = getRandomArrayElements(recommendList.value,8)
                        console.log(recommendList.value)
                    })
                })

            })

        })
    })
}
</script>

<style scoped>
.title-text {
  align-self: center;
  font-size: x-large;
  padding-left: 6px;
}

.title-container {
  padding-bottom: 12px;
}

.title-text-tip {
  padding: 6px;
  align-self: center;
  font-size: medium;
  color: #909399;
}
</style>
