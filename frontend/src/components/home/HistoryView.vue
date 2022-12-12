<template>
    <el-empty :image-size="200" v-if="listItem.length == 0 || !logged" description="没有数据" />
    <el-row justify="center" v-else>
        <!-- 右侧列表展示页面 -->
        <el-col :span="15">
            <el-row justify="center">
                <el-col>
                    <el-row :size="16" :gutter="12" style="align-items: stretch;">
                        <el-col v-for="i in listItem" :span="25" style="margin-bottom:16px">
                            <video-list-item :title="i['title']" :timestamp="timeFormat(i['timestamp'])"
                                :cover="i['cover']" :id="i['id']">
                            </video-list-item>
                        </el-col>
                    </el-row>
                </el-col>
            </el-row>
        </el-col>
    </el-row>

</template>

<script setup lang="ts">
import { useLocalStorage } from "@vueuse/core"
import { getUserInfo } from "../../api";
function timeFormat(arg: string) {
    return arg.substring(0, 16).replace("T", " ")
}
const logged = ref(false);
const listItem = useLocalStorage("historyVideos", [])
getUserInfo().then((res: any) => {
    logged.value = true;
});

</script>

<style scoped>
:deep(.el-col-25) {
    width: 20%;
}

.login-tip {
    position: absolute;
    width: 30rem;
    left: 35%;
    margin-top: 150px;
    z-index: 1000000;
    border-radius: 10px;
}
</style>
