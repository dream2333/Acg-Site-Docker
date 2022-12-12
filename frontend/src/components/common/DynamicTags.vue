<template>
  <el-tag v-show="tag" v-for="tag in dynamicTags" :key="tag" class="tag" closable :disable-transitions="false"
    @close="handleClose(tag)">{{ tag }}</el-tag>
  <el-input v-if="inputVisible" ref="InputRef" v-model="inputValue" class="ml-1 w-20" size="small"
    @keyup.enter="InputRef.$refs.input.blur()" @blur="handleInputConfirm" />
  <el-button v-else class="button-new-tag ml-1" size="small" @click="showInput">+ 新标签</el-button>
</template>

<script lang="ts" setup>
import { updateUserInfo } from '../../api';

const inputValue = ref('')
const inputVisible = ref(false)
const InputRef = ref()

const handleClose = (tag: string) => {
  dynamicTags.value.splice(dynamicTags.value.indexOf(tag), 1)
}
const props = defineProps(["tags"])
const dynamicTags = ref(props.tags.split(" "))
const showInput = () => {
  inputVisible.value = true
  nextTick(() => {
    InputRef.value!.input!.focus()
  })
}

const handleInputConfirm = () => {
  if (inputValue.value) {
    dynamicTags.value.push(inputValue.value)
  }
  inputVisible.value = false
  inputValue.value = ''
}

//侦听tags是否变化
watch(dynamicTags.value, () => {
  updateUserInfo({ tags: dynamicTags.value.join(" ") }).then((res) => {
    if (res.data.status == 0) {
      ElMessage({
        message: "更改标签错误",
        type: "error",
        offset: 40
      });
    } else {
      ElMessage({
        message: "更改标签成功",
        type: "success",
        offset: 40
      });
    }
  }).catch((e) => {
    console.log(e)
  })
})
</script>

<style scoped>
.tag {
  margin-bottom: 0.5rem;
  margin-right: 0.25rem;
}

.w-20 {
  width: 5rem;
}

.ml-1 {
  margin-bottom: 0.5rem;
  margin-left: 0.25rem;
}
</style>