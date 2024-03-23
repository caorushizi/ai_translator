<script setup lang="ts">
import { fetchEventSource } from '@microsoft/fetch-event-source'
import { Edit, Picture, UploadFilled } from '@element-plus/icons-vue'
import { ref, shallowRef } from 'vue'
import UploadPDF from '@/components/UploadPDF.vue'
import ControlBlock from '@/components/ControlBlock.vue'

const message = ref('')
const component = shallowRef(UploadPDF)

async function handleClick() {
  await fetchEventSource('http://localhost:5000/api/python', {
    onmessage(event) {
      console.log(event.data)
      message.value += event.data
    },
    onerror(error) {
      console.error(error)
    }
  })
}
</script>

<template>
  <main>
    <el-steps class="mb-4" :space="200" :active="1" simple>
      <el-step title="Step 1" :icon="Edit" />
      <el-step title="Step 2" :icon="UploadFilled" />
      <el-step title="Step 3" :icon="Picture" />
    </el-steps>
    <el-container class="main-container">
      <component :is="component" />
    </el-container>
    <ControlBlock />
  </main>
</template>

<style scoped lang="scss">
.main-container {
  padding: 20px;
}
</style>
