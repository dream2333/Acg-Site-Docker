<template>
    <el-row :span="24">
        <el-col :span="8" v-for="i in 3">
            <cover class="cover" :image="data[(i - 1) * 2].img" :id="data[(i - 1) * 2].id">{{ data[(i - 1) * 2].title }}
            </cover>
            <cover class="cover" :image="data[(i - 1) * 2 + 1].img" :id="data[(i - 1) * 2 + 1].id">{{ data[(i - 1) * 2 +
                    1].title
            }}</cover>
        </el-col>
    </el-row>
</template>

<script setup lang="ts">

defineProps(["data"])

</script>

<style scoped>
.cover {
    margin-left: 6%;
    margin-bottom: 9%;
}
</style>