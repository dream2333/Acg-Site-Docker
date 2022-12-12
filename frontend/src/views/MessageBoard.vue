<template>
    <el-row justify="center" align="top">
        <el-col :span="18" style="min-height: 800px;">

            <el-space v-infinite-scroll="load" infinite-scroll-distance="50"
                style="margin-top:64px;justify-content: center;" wrap :infinite-scroll-immediate="scrollImmediate">
                <message-sticker v-for="i in MessageList" :avatar="i['user']['avatar']" :user="i['user']['username']"
                    :text="i['message']" :timestamp="timeFormat(i['timestamp'])" />
            </el-space>

        </el-col>
        <el-button type="primary" style="position:sticky;top: 860px;" size="large" :icon="Edit" @click="drawer = true"
            circle />
    </el-row>
    <el-drawer v-model="drawer" direction="rtl" size="25%" @open="drawerOpen">
        <template #default>
            <el-empty v-if="!logged" :description="'请先登录账号'" />
            <div v-else>
                <div style="font-weight: bold;font-size:x-large;margin-bottom:32px">我的历史留言</div>
                <el-timeline style="padding-left: 16px;">
                    <el-timeline-item v-for="(activity, index) in myMessageList" :key="index"
                        :timestamp="timeFormat(activity['timestamp'])">{{ activity["message"] }}</el-timeline-item>
                </el-timeline>
            </div>
        </template>
        <template #footer v-if="logged">
            <div style="flex: auto">
                <el-input v-model="textarea" maxlength="45" rows="3" placeholder="请输入内容" show-word-limit type="textarea"
                    style="bottom:24px;" />
                <el-button @click="cancelClick">取消</el-button>
                <el-button type="primary" @click="confirmClick">提交</el-button>
            </div>
        </template>
    </el-drawer>
</template>

<script setup lang="ts">
import { Edit } from '@element-plus/icons-vue'
import { ElNotification } from 'element-plus';
import { getAllMessage, getMyMessage, leaveMessage } from '../api';

const drawer = ref(false)
const textarea = ref('')
const itemList = ref([])
const MessageList = ref([])
const myMessageList = ref([])
const logged = ref(false)
const scrollImmediate = ref(false)
getMsg()
//懒加载的光标
let cursor = 0
//进入页面加载所有留言
function getMsg() {
    getAllMessage().then((res) => {
        itemList.value = res.data.reverse()
        if (itemList.value.length >= 16) {
            MessageList.value = itemList.value.slice(0, 16)
            scrollImmediate.value = true
        }
        else {
            MessageList.value = itemList.value
        }
    }).catch((e) => {
        console.log(e)
    })
}

//打开抽屉时加载我的留言
function drawerOpen() {
    getMyMessage().then((res) => {
        logged.value = true
        myMessageList.value = res.data.reverse().slice(0, 9)

    }).catch((e) => {
        logged.value = false
    })
}

function timeFormat(arg: string) {
    return arg.substring(0, 16).replace("T", " ")
}

//滚动到底部时懒加载留言
function load() {

    cursor += 4
    MessageList.value = itemList.value.slice(0, 16 + cursor)
}
//提交留言
function confirmClick() {
    if (textarea.value.length != 0) {
        leaveMessage({ text: textarea.value }).then((res) => {
            getMsg()
            ElNotification({
                title: '留言成功',
                message: '您刚刚留言：' + textarea.value,
                type: 'success',
                position: "bottom-left"
            })
            textarea.value = ""
            drawer.value = false
        }).catch(() => {
            ElNotification({
                title: '错误',
                message: '留言失败',
                type: "error",
                position: "bottom-left"
            })
        })


    }
    else {
        ElNotification({
            title: '警告',
            message: '留言不能为空',
            type: "warning",
            position: "bottom-left"
        })
    }
}
function cancelClick() {
    drawer.value = false
}
</script>

<style scoped>
</style>