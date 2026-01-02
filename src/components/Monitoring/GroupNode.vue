<template>
  <div class="group-node w-full h-full border-2 border-dashed rounded-lg transition-all"
    :class="[
      isSelected ? 'border-primary-500 bg-primary-500/10' : 'border-surface-400 dark:border-surface-600 bg-surface-200/20 dark:bg-surface-800/20'
    ]"
  >
    <!-- Label -->
    <div class="absolute -top-7 left-0 bg-surface-100 dark:bg-surface-800 px-2 py-0.5 rounded border border-surface-300 dark:border-surface-600 text-xs font-bold text-surface-600 dark:text-surface-300 shadow-sm backdrop-blur-sm">
        {{ label }}
    </div>
  </div>
</template>

<script setup>
import { inject, ref, onUnmounted } from 'vue';

const getNode = inject('getNode');
const node = getNode();

const data = ref(node.getData() || {});
const label = ref(node.prop('label') || 'Group');
const isSelected = ref(data.value.isSelected || false);

const updateState = () => {
    const newData = node.getData() || {};
    data.value = newData;
    label.value = node.prop('label') || 'Group';
    isSelected.value = newData.isSelected || false;
};

node.on('change:data', updateState);
node.on('change:label', updateState);


onUnmounted(() => {
    node.off('change:data', updateState);
    node.off('change:label', updateState);
});
</script>

<style scoped>
.group-node {
    /* Allow passing clicks through to valid targets if needed, but usually we want to select the group */
}
</style>
