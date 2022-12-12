<template>
    <div class="outter">
        <el-avatar size="large" class="avatar" :src="avatar"></el-avatar>
        <div class="time">{{ timestamp }}</div>
        <el-card class="card" :body-style="'background-color:' + color[Math.floor((Math.random() * 5))]">
            <div style="padding-top: 14px;font-weight: bolder;font-size:larger">{{ user }}</div>
            <div style="padding-top:14px;text-align:left;overflow-y:hidden;font-size:13px">{{ text }}</div>
        </el-card>
    </div>
</template>

<script setup lang="ts">
const color = [" #53a8ff", " #95d475", " #eebe77", " #f89898", " #b1b3b8"]
defineProps({
    avatar: { default: "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png" },
    user: { default: "测试用户" },
    text: {
        default: "这是一段测试留言😊这是一段测试留言😊这是一段测试留言😊这是一段测试留言😊"
    },
    timestamp: { default: "2022-1-1" }
})
</script>

<style scoped>
.card {
    top: 30px;
    height: 180px;
    width: 260px;
    position: absolute;
    border-radius: 12px;
    z-index: -10;
}

.time {
    position: absolute;
    right: 8px;
    bottom: 8px;
    color: gray;
    font-size: small;
    font-weight: 100;
}

.avatar {
    top: -10;
}

.outter {
    position: relative;
    height: 210px;
    width: 260px;
    margin: 16px;
    text-align: center;
}
</style>
