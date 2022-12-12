<template>
    <div>
        <div style="flex: auto;">
            <span style="margin: 4px 12px 12px 4px;font-size: large;font-weight: bold;">影评</span>
            <el-rate v-model="rate" allow-half size="small" />
            <el-input v-model="textarea" maxlength="45" rows="3" placeholder="请输入内容" show-word-limit type="textarea" />
            <el-button type="primary" @click="confirmClick" style="width:72px;margin-right:12px">提 交</el-button>
            <el-button type="info" @click="textarea = ''" style="width:72px;margin-right:24px;">清 空</el-button>
            <el-timeline style="margin-top:16px">
                <el-timeline-item v-for="(activity, index) in itemList" :timestamp="timeFormat(activity.timestamp)">
                    <el-row align="middle" style="line-height: 24px;" justify="space-between">
                        <div>
                            <el-avatar :src="activity.user.avatar" style="margin-right: 12px;display:inline-block">
                            </el-avatar>
                            <span style="display:inline-block">
                                <div style="font-weight:bolder ;">
                                    {{ activity.user.username }}：
                                </div>
                                <div style="font-size:small ;">
                                    {{ activity.message }}
                                </div>
                            </span>
                        </div>
                        <div>
                            <el-rate v-if="activity.rating" v-model="activity.rating" disabled allow-half />
                        </div>
                    </el-row>
                </el-timeline-item>
            </el-timeline>

        </div>
    </div>
</template>

<script setup lang="ts">
import { ElNotification } from 'element-plus';
import { getAllMessage, getComment, leaveComment, leaveMessage } from '../../api';
const emits = defineEmits(["ratingGetted"])
const textarea = ref('')
const itemList = ref()
const props = defineProps(["id"])
const rate = ref()

getMsg()
function getMsg() {
    getComment(props.id).then((res) => {
        itemList.value = res.data.reverse()
        let avg = 0
        for (var i = 0; i < res.data.length; i++) {
            avg += res.data[i].rating
        }
        avg = avg / i
        emits("ratingGetted", avg)
    })
}
function timeFormat(arg: string) {
    return arg.substring(0, 16).replace("T", " ")
}
function confirmClick() {
    if (textarea.value.length != 0) {
        console.log(rate.value)
        leaveComment({ text: textarea.value, link_to_id: props.id, rating: rate.value != 0 ? rate.value : null }).then((res) => {
            if (res.data.status) {
                getMsg()
                ElNotification({
                    title: '评价成功',
                    message: '您刚刚评价：' + textarea.value,
                    type: 'success',
                    position: "bottom-left"
                })
            }
            else {
                ElNotification({
                    title: '评论重复',
                    message: '您已经进行过打分了',
                    type: 'info',
                    position: "bottom-left"
                })
            }
            textarea.value = ""
            rate.value = 0
        }).catch(() => {
            ElNotification({
                title: '错误',
                message: '评价失败',
                type: "error",
                position: "bottom-left"
            })
        })


    }
    else {
        ElNotification({
            title: '警告',
            message: '评分或留言不能为空',
            type: "warning",
            position: "bottom-left"
        })
    }
}


</script>

<style scoped>
:deep(.el-rate__decimal) {
    position: absolute;
    top: 0;
    left: 0;
    display: inline-block;
    overflow: hidden;
    color: var(--el-rate-fill-color)
}
</style>