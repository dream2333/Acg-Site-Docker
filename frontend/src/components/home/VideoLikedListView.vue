<template>
    <el-row el-row justify="center">
        <el-col :span="18">
            <el-empty :image-size="200" v-if="listItem.length==0 " description="没有数据" />
            <el-row justify="start" :gutter="24" v-else>
                <el-col v-for="i in listItem" :span="4" style="margin-bottom:16px;">
                    <video-liked-item :title="i['title']" :timestamp="timeFormat(i['timestamp'])" :cover="i['cover']"
                        :id="i['id']">
                    </video-liked-item>
                </el-col>
            </el-row>
            <el-row justify="center">
            </el-row>
        </el-col>
    </el-row>
</template>

<script setup lang="ts">
import { getLikedList } from '../../api';

const listItem = ref(Array())

getLikedList().then((res) => {
    listItem.value = res.data
})

function timeFormat(arg: string) {
    return arg.substring(0, 11).replace("T", " ")
}

</script>

<style scoped>
</style>