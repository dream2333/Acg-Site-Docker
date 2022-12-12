<template>
    <el-row justify="center" :gutter="8">
        <el-col :span="20" style="line-height: 64px;">
            <el-card class="card">
                <el-page-header :icon="ArrowLeft" :content="title" @back="router.back()" />
                <el-row>
                    <el-col :span="18" ref="leftCol">
                        <div style="margin-top:24px">
                            <video ref="videoPlayer" controls :src="video_url" class="vplayer">
                            </video>
                        </div>
                        <div class="info">
                            <div style="display: inline-block;width:85%">
                                <span style="margin-right:8px">
                                    <el-icon style="margin:8px">
                                        <video-camera />
                                    </el-icon>{{ title }}
                                </span>
                                <el-divider direction="vertical" />
                                <span>
                                    <el-icon style="margin:8px">
                                        <calendar />
                                    </el-icon>{{ time }}
                                </span>

                                <div style="display:flex">
                                    <el-icon style="margin:8px;">
                                        <chat-line-square />
                                    </el-icon>
                                    <span>{{ intro }}</span>
                                </div>
                                <el-tag v-for="i in tags" class="mx-1" effect="plain" round style="margin:4px">{{ i }}</el-tag>
                            </div>

                            <div class="rating">
                                <div style="font-weight: bold;font-size: large;">
                                    {{ ratingAvg ? ratingAvg.toFixed(1) + "分" : "暂无评分" }}
                                </div>
                                <el-rate v-model="ratingAvg" disabled allow-half></el-rate>
                            </div>

                        </div>
                    </el-col>
                    <el-col :span="6" style="padding-top:24px;padding-left: 24px;line-height: 24px; font-weight: 200;">
                        <el-scrollbar :height="leftHeight">
                            <!-- 推荐栏 -->
                            <div v-for="i in recommendList" style="display:flex">
                                <div>
                                    <el-image :src="i.cover" style="width:150px;"></el-image>
                                </div>
                                <el-link style="margin-left:8px;align-items:flex-start;font-size:small;"
                                    :underline="false" @click="router.push({ name: 'video', params: { id: i.id } })">{{
                                            i.title
                                    }}
                                </el-link>
                            </div>
                        </el-scrollbar>
                    </el-col>
                </el-row>
                <video-comment :id="id" @rating-getted="(avg) => ratingAvg = avg" />
            </el-card>
        </el-col>

        <el-col :span="1">
            <el-tooltip v-if="!alreadyLiked" class="box-item" effect="light" content="收藏此视频" placement="right-start">
                <el-button type="primary" style="position:sticky;top: 860px;margin:64px;" size="large" :icon="FolderAdd"
                    circle @click="clickLikeButton" />
            </el-tooltip>
            <el-tooltip v-else class="box-item" effect="light" content="取消收藏" placement="right-start">
                <el-button type="danger" style="position:sticky;top: 860px;margin:64px;" size="large" :icon="Close"
                    circle @click="clickRemoveButton" />
            </el-tooltip>
        </el-col>
    </el-row>
</template>

<script setup lang="ts">import { toInteger } from 'lodash';
import { ArrowLeft, Calendar, ChatLineSquare, VideoCamera, FolderAdd, Close } from '@element-plus/icons-vue'
import { useRoute, useRouter } from 'vue-router';
import { getLikedList, getVideoInfo, getVideoList, likeVideo, removeLiked } from '../../api';
import { useLocalStorage } from "@vueuse/core"
function timeFormat(arg: string) {
    return arg.substring(0, 16).replace("T", " ")
}
const leftHeight = ref(0)
const leftCol = ref()
const historyVideos = useLocalStorage("historyVideos", Array())
const route = useRoute()
const router = useRouter()
const id = toInteger(route.params.id)
const title = ref("")
const video_url = ref("")
const time = ref("")
const intro = ref("")
const ratingAvg = ref(0)
const alreadyLiked = ref(false)
const recommendList = ref(Array())
const tags = ref("")
const resizeListener = () => {
    //leftHeight.value = leftCol.value.$el.clientHeight
}
watch(route, () => {
    window.location.reload()
})
onMounted(() => {
    //leftHeight.value = leftCol.value.$el.clientHeight
    window.addEventListener('resize', resizeListener)
    fakeRecommend()
})
getVideoInfo(id).then((res) => {
    const data = res.data
    title.value = data.title
    video_url.value = res.data.video
    time.value = timeFormat(res.data.timestamp)
    intro.value = res.data.intro
    tags.value = res.data.tags.split(" ")
    console.log(tags.value)
    for (var i of historyVideos.value) {
        if (isObjectValueEqual(i, res.data)) {
            return
        }
    }
    historyVideos.value.unshift(res.data)
})

getLikedList().then((res) => {
    for (var i = 0; i < res.data.length; i++) {
        if (res.data[i].id == id) {
            alreadyLiked.value = true
            break;
        }
    }
})
function clickLikeButton() {
    likeVideo(id).then((res) => {
        res.data
        alreadyLiked.value = true
        ElMessage({
            message: "添加收藏成功",
            type: "success",
            offset: 40
        });
    })
}
function clickRemoveButton() {
    removeLiked(id).then((res) => {
        res.data
        alreadyLiked.value = false
        ElMessage({
            message: "移除收藏成功",
            type: "info",
            offset: 40
        });
    })
}
function isObjectValueEqual(a: object, b: object) {
    // 判断两个对象是否指向同一内存，指向同一内存返回true
    if (a === b) return true
    // 获取两个对象键值数组
    let aProps = Object.getOwnPropertyNames(a)
    let bProps = Object.getOwnPropertyNames(b)
    // 判断两个对象键值数组长度是否一致，不一致返回false
    if (aProps.length !== bProps.length) return false
    // 遍历对象的键值
    for (let prop in a) {
        // 判断a的键值，在b中是否存在，不存在，返回false
        if (b.hasOwnProperty(prop)) {
            // 判断a的键值是否为对象，是则递归，不是对象直接判断键值是否相等，不相等返回false
            if (typeof a[prop] === 'object') {
                if (!isObjectValueEqual(a[prop], b[prop])) return false
            } else if (a[prop] !== b[prop]) {
                return false
            }
        } else {
            return false
        }
    }
    return true
}
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
                        recommendList.value = getRandomArrayElements(recommendList.value, 6)
                        console.log(recommendList.value)
                    })
                })

            })

        })
    })
}
</script>

<style scoped>
.vplayer {
    width: 100%;
    height: 100%;
    object-fit: fill;
}

.info {
    width: 100%;
    line-height: 36px;
    font-size: smaller;
    color: grey;
    align-items: center;
    display: inline-flex;
    justify-content: space-between;
    margin-bottom: 32px
}

.rating {
    display: inline;
    text-align: center;
    vertical-align: middle;
    color: var(--el-color-primary);
}

.card {
    justify-content: center;
    padding-left: 36px;
    padding-right: 36px;
    padding-top: 12px;
}

:deep(.el-rate__decimal) {
    position: absolute;
    top: 0;
    left: 0;
    display: inline-block;
    overflow: hidden;
    color: var(--el-rate-fill-color)
}
</style>