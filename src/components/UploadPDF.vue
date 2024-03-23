<template>
  <el-upload
    class="upload-demo"
    drag
    action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
    :http-request="handleRequest"
    :limit="1"
    :disabled="loading"
  >
    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
    <div class="el-upload__text">拖拽文件或者 <em>点击上传</em></div>
    <template #tip>
      <div class="el-upload__tip">pdf 最大 500kb</div>
    </template>
  </el-upload>
</template>

<script setup lang="ts">
import { UploadFilled } from '@element-plus/icons-vue'
import { defineEmits } from 'vue'
import { ref } from 'vue'
import { http } from '@/helper'
import type { UploadRequestHandler } from 'element-plus'

const loading = ref(false)
const emit = defineEmits(['success'])

function handleSuccess() {
  console.log('success')
  emit('success')
}

const handleRequest: UploadRequestHandler = async function (option) {
  try {
    loading.value = true
    console.log(option)
    const form = new FormData()
    form.append('file', option.file)
    const res = await http.post('/api/upload', form, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    option.onSuccess(res)
    console.log(res)
    emit('success')
  } catch (e) {
    console.log('error:', e)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.upload-demo {
  width: 100%;
}
</style>
