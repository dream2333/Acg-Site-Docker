<template>
    <el-card class="login-tip" v-if="!logged">
        <el-result icon="warning" title="未登录" sub-title="登录以查看更多内容">
        </el-result>
    </el-card>
    <el-row justify="center" :class="{ mask: !logged }">
        <!-- 筛选排序框 -->
        <el-col :span="3" style="margin-right: 16px;">
            <el-card style="height: 67vh;position:sticky;top:64px;padding-left:12px">
                <h2>筛选排序</h2>
                <el-space direction="vertical">
                    <el-radio v-model="radio1" label="id" size="large">按默认 〰️</el-radio>
                    <el-radio v-model="radio1" label="-title" size="large">按名称 🔠</el-radio>
                    <el-radio v-model="radio1" label="-timestamp" size="large">按时间 📅</el-radio>
                </el-space>
            </el-card>
        </el-col>
        <!-- 右侧列表展示页面 -->
        <el-col :span="15">
            <el-row justify="center">
                <el-col>
                    <el-row :size="16" v-infinite-scroll="scroll" :gutter="12" style="align-items: stretch;"
                        :infinite-scroll-disabled="infinite_scroll" infinite-scroll-distance="300"
                        infinite-scroll-immediate>
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
import { getVideoList, getUserInfo } from '../../api';
const radio1 = ref("id")
const listItem = ref(Array())
const infinite_scroll = ref(false)
let page = 1;
const logged = ref(false);
let noPages = false;
getUserInfo().then((res: any) => {
    logged.value = true;
});
watch(radio1, (label) => {
    sessionStorage.removeItem("carList")
    page = 1
    listItem.value = Array()
    noPages = false;
    initPage(label)
})
function timeFormat(arg: string) {
    return arg.substring(0, 11).replace("T", " ")
}

initPage("id")
onActivated(() => {
    console.log("activated")
    infinite_scroll.value = false
})
onDeactivated(() => {
    console.log("deactivated")
    infinite_scroll.value = true
})
function initPage(label: string) {
    if (!noPages) {
        getVideoList(page, label).then((res) => {
            page += 1
            listItem.value = listItem.value.concat(res.data.results)
            if (res.data.next == null) {
                noPages = true
            }
            if (!noPages) {
                getVideoList(page, label).then((res) => {
                    page += 1
                    listItem.value = listItem.value.concat(res.data.results)
                    if (res.data.next == null) {
                        noPages = true
                    }
                    if (!noPages) {
                        getVideoList(page, label).then((res) => {
                            page += 1
                            listItem.value = listItem.value.concat(res.data.results)
                            if (res.data.next == null) {
                                noPages = true
                            }
                        })
                    }
                })
            }
        })
    }
}
function scroll() {
    if (!logged.value) {
        return
    }
    if (!noPages) {
        getVideoList(page, radio1.value).then((res) => {
            page += 1
            listItem.value = listItem.value.concat(res.data.results)

            if (res.data.next == null) {
                noPages = true
            }
        })
    }
}
defineProps({
    data: { default: "" },
});




</script>

<style scoped>
:deep(.el-col-25) {
    width: 20%;
}

.mask {
    filter: blur(12px);
    pointer-events: none;
    user-select: none;
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
