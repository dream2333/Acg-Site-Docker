<template>
    <el-card class="el-card-d" shadow="always">
        <div class="infinite-list-wrapper" style="overflow:auto;">
            <el-timeline infinite-scroll-disabled="disabled">
                <div v-if="allmessages.length > 0">
                    <el-timeline-item
                        v-for="(item, index) in allmessages"
                        :key="index"
                        :timestamp="item.createTime"
                        placement="top"
                    >
                        <el-card class="el-card-m" style="height:120px">
                            <h4>{{ item.memberName }}：</h4>
                            <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{ item.content }}</p>
                        </el-card>
                    </el-timeline-item>
                </div>
                <div v-else>
                    <el-timeline-item placement="top">
                        <el-card class="el-card-m" style="height:120px">
                            <h4>大黄子：</h4>
                            <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 说点什么吧😁</p>
                        </el-card>
                    </el-timeline-item>
                </div>
            </el-timeline>
        </div>
        <div class="el-card-messages">
            <el-input
                type="textarea"
                :rows="5"
                placeholder="输入留言"
                maxlength="200"
                v-model="message"
            ></el-input>
            <el-button type="info" round class="submit-message" @click="submitMessage">留言</el-button>
        </div>
    </el-card>
</template>

<script setup lang="ts">
const message = ''
const allmessages = [{
    createTime: '2022-04-12 20:46',
    memberName: "测试1",
    content: "说点什么吧😁"
}, {
    createTime: "'2022-04-12 20:47'",
    memberName: "测试2",
    content: "说点什么吧😁"
},]
function submitMessage() {
    if (message == '') {
        return;
    }
    //  这里往下写调用后端的代码；
}

</script>

<style scoped>
.infinite-list-wrapper {
    width: 100%;
    height: 100%;
}
.submit-message {
    width: 100%;
    background: rgb(235, 245, 247);
    color: cadetblue;
    letter-spacing: 20px;
}
.el-card-m {
    text-align: left;
}
@media screen and (max-width: 3000px) and (min-width: 767px) {
    .el-card-d {
        margin-left: 20%;
        margin-right: 20%;
        padding: 64px;
    }
}
/*
  屏幕小于768px的
  */
@media screen and (max-width: 768px) and (min-width: 100px) {
    .el-card-d {
        width: 100%;
        height: 100%;
    }
}
</style>