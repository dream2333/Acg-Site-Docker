<template>
    <el-row justify="center">
        <el-col :span="18">
            <el-empty :image-size="200" v-if="count == 0" description="没有数据" />
            <el-row justify="start" :gutter="24" v-else>
                <el-col v-for="i in listItem" :span="4" style="margin-bottom:16px;">
                    <video-list-item :title="i['title']" :timestamp="timeFormat(i['timestamp'])" :cover="i['cover']"
                        :id="i['id']">
                    </video-list-item>
                </el-col>
            </el-row>
            <el-row justify="center">
                <!-- 分页工具 Math.floor(count / 24)为页数 -->
                <el-pagination background layout="prev, pager, next" :page-size="18" :total="count"
                    @current-change="(p) => { newPage(words, p) }" />
            </el-row>
        </el-col>
    </el-row>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router';
import { videoSearch } from '../api';

const listItem = ref(Array())
const count = ref(0)
const route = useRoute()
let words: any = route.params.str
newPage(words, 1)
watch(route, () => {
    words = route.params.str
    newPage(words, 1)
})

function newPage(words: string, page: number) {
    videoSearch(words, page).then((res) => {
        listItem.value = res.data.results
        count.value = res.data.count
    })
}

function timeFormat(arg: string) {
    return arg.substring(0, 11).replace("T", " ")
}
</script>

<style scoped>
</style>