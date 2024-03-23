<template>
  <div fill direction="horizontal" class="control-block">
    <div class="block prev" @click="$emit('prev')">上一步</div>
    <div class="block next" @click="$emit('next')">下一步</div>
  </div>
</template>

<style scoped lang="scss">
.control-block {
  display: flex;
  flex-direction: row;
  gap: 10px;
  .block {
    flex: 1;
    text-align: center;
    background: var(--el-fill-color-light);
    border-radius: 4px;
    padding: 13px 8%;
    cursor: pointer;
  }
}
</style>
