<template>
    <el-card :body-style="{ padding: '0px' }" style="height:100% ;align-items: stretch;">
        <el-image :src="cover" class="image" referrerPolicy="no-referrer" />
        <div style="padding: 12px 14px 4px 14px;">
            <div class="title"><span>{{ title }}</span>
                <el-button type="primary" :icon="Delete" @click="clickRemoveButton" />
            </div>
            <div class="bottom">
                <span class="time">{{ timestamp }}</span>
                <el-button type="text" class="button"
                    @click="() => router.push({ name: 'video', params: { id: props.id } })">
                    点击查看</el-button>
            </div>
        </div>
    </el-card>
</template>

<script lang="ts" setup>
import { Delete } from '@element-plus/icons-vue'
import { toInteger } from 'lodash';
import { useRouter } from 'vue-router';
import { removeLiked } from '../../api';
const router = useRouter()
const props = defineProps({
    title: { default: "占位内容" },
    timestamp: { default: "2000-01-01" },
    cover: { default: "" },
    id: { default: "1" }
})
function clickRemoveButton() {
    removeLiked(toInteger(props.id)).then((res) => {
        ElMessage({
            message: "移除收藏成功",
            type: "info",
            offset: 40
        });
        window.location.reload()
    })
}
</script>
<style>
.title {
    font-size: small;
    min-height: 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.time {
    font-size: smaller;
    color: #999;
}

.bottom {
    margin-top: 13px;
    line-height: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.button {
    padding: 0;
    font-size: smaller;
    min-height: auto;
}

.image {
    width: 100%;
    display: block;
}
</style>