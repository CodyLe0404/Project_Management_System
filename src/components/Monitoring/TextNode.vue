<template>
  <div class="text-node p-1 transition-all"
    :class="{ 'ring-1 ring-primary-400 rounded': isSelected }"
  >
    <span class="font-bold text-lg text-surface-900 dark:text-surface-100 whitespace-nowrap">
        {{ label }}
    </span>
    <!-- Optional: Add small handle if needed, but text acts as handle usually -->
  </div>
</template>

<script setup>
import { inject, ref, onUnmounted } from 'vue';

const getNode = inject('getNode');
const node = getNode();

const data = ref(node.getData() || {});
const label = ref(node.prop('label') || 'Text');
const isSelected = ref(data.value.isSelected || false);

const updateData = () => {
    const newData = node.getData() || {};
    data.value = newData;
    isSelected.value = newData.isSelected || false;
};

node.on('change:data', updateData);
node.on('change:label', ({ current }) => {
    label.value = current || 'Text';
});

onUnmounted(() => {
    node.off('change:data', updateData);
    node.off('change:label');
});
</script>
