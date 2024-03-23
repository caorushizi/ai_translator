<template>
  <el-upload
    class="upload-demo"
    drag
    action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
    multiple
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
</script>

<style scoped>
.upload-demo {
  width: 100%;
}
</style>
