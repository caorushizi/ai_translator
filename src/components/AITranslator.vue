<template>
  <el-row>
    <el-col :span="12"><div class="grid-content ep-bg-purple">1</div></el-col>
    <el-col :span="12"><div class="grid-content ep-bg-purple-light">1</div></el-col>
  </el-row>
</template>

<style lang="scss">
.el-row {
  margin-bottom: 20px;
}
.el-row:last-child {
  margin-bottom: 0;
}
.el-col {
  border-radius: 4px;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
</style>
