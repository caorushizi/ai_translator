<script setup lang="ts">
import { ref } from 'vue'
import { RouterView } from 'vue-router'

const activeIndex = ref('/')
</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <el-menu
          :default-active="activeIndex"
          class="el-menu-demo"
          mode="horizontal"
          :ellipsis="false"
          router
        >
          <el-menu-item index="0">
            <img style="width: 100px" src="@/assets/element-plus-logo.svg" alt="Element logo" />
          </el-menu-item>
          <div class="flex-grow" />
          <el-menu-item index="/">首页</el-menu-item>
          <el-menu-item index="/about">关于</el-menu-item>
        </el-menu>
      </el-header>
      <el-main>
        <RouterView />
      </el-main>
    </el-container>
  </div>
</template>

<style scoped>
.flex-grow {
  flex-grow: 1;
}
</style>
