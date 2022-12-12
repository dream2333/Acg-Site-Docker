<template>
    <div class="item">
        <div class="badge">{{ value >= 99 ? "99+" : value }}</div>
        <div style="height: 2px;"/>
        <div class="text1">{{ text }}</div>
    </div>
</template>

<script setup lang="ts">
const props = defineProps(["text", "value"])
</script>

<style scoped>
.item {
    margin-right: 6px;
    margin-left: 6px;
        text-align: center;
}
.badge {
    font-size: x-small;
    color: white;
    width: 32px;
    height: 20px;
    line-height: 20px;
    background: #53a8ff;
    border-radius: 8px;
}
.text1{
    font-size: x-small;
    line-height: 20px;

}
</style>