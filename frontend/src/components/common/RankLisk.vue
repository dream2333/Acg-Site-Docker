<template>
    <el-row>
        <span class="title-text title-container">视频排行</span>
    </el-row>
    <el-row>
        <el-col v-if="data.length > 0">
            <cover-video :image="data[0]['cover']" :id="data[0]['id']">{{ data[0]['title'] }}</cover-video>
            <div class="tag">1</div>
            <rank-list-item class="rank-list-item" v-for="i in Math.min(data.length, 4)" :tag="i + 1"
                :id="data[i]['id']">{{ data[i]['title'] }}</rank-list-item>
            <el-button class="button" type="info" plain @click="router.push('videoList')">查看更多</el-button>
        </el-col>
    </el-row>
</template>

<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router';
const router = useRouter()
const props = defineProps({
    data: {
        default: [{
            id: 1,
            title: "此处为测试内容",
            cover: ""
        }]
    }
})
console.log(props.data)
</script>

<style scoped>
.rank-list-item {
    margin-bottom: 16px;
    margin-top: 16px;
}

.title-text {
    align-self: center;
    font-size: x-large;
    padding-left: 6px;
}

.title-container {
    padding-bottom: 12px;
}

.tag {
    color: ghostwhite;
    font-size: small;
    align-items: center;
    text-align: center;
    line-height: 28px;
    background-color: #53a8ff;
    border-radius: 10px 0px 10px 0px;
    width: 32px;
    height: 26px;

    position: absolute;
    top: 0;
    left: 0;
}

.button {
    width: 100%;
}
</style>