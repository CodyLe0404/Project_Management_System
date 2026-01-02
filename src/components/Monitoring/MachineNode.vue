<template>
    <div class="machine-node shadow-lg rounded-xl bg-surface-0 dark:bg-surface-800 border-2 w-48 transition-all hover:scale-105"
        :class="[
            'cursor-move',
             isSelected ? 'border-primary-500 ring-2 ring-primary-200' : 'border-surface-200 dark:border-surface-700'
        ]"
    >
        <!-- Header -->
        <div class="p-3 border-b border-surface-200 dark:border-surface-700 bg-surface-50 dark:bg-surface-800 rounded-t-lg flex items-center justify-between">
            <span class="font-bold text-sm truncate">{{ label }}</span>
            <span class="w-3 h-3 rounded-full border-2 border-transparent" 
                :class="[
                    statusColor,
                    { 'machine-blink-error': data?.blinkEnabled && data?.status === 'error', 'machine-blink-active': data?.blinkEnabled && data?.status === 'running' }
                ]"
            ></span>
        </div>

        <!-- Body -->
        <div class="p-3 text-xs text-surface-600 dark:text-surface-400 flex flex-col gap-2">
            <!-- Temp -->
            <div class="flex justify-between items-center">
                <span>Temp:</span>
                <span class="font-medium text-surface-900 dark:text-surface-200">{{ data?.temp || 0 }}°C</span>
            </div>

            <!-- Load Bar -->
            <div class="flex flex-col gap-1">
                <div class="flex justify-between items-center">
                    <span>Load:</span>
                    <span class="font-medium text-surface-900 dark:text-surface-200">{{ data?.load || '0%' }}</span>
                </div>
                <!-- Mini Progress Bar -->
                <div class="w-full bg-surface-200 dark:bg-surface-700 rounded-full h-1.5 overflow-hidden">
                    <div class="bg-blue-500 h-full rounded-full transition-all duration-500" 
                        :style="{ width: data?.load || '0%' }"
                    ></div>
                </div>
            </div>

            <!-- Status Message (if any) -->
            <div v-if="data?.message" class="mt-1 p-2 bg-surface-100 dark:bg-surface-900 rounded border border-surface-200 dark:border-surface-700 text-[10px] leading-tight text-surface-700 dark:text-surface-300 italic">
                {{ data.message }}
            </div>
        </div>
    </div>
</template>

<script setup>
import { inject, ref, onMounted, computed, onUnmounted } from 'vue';

// X6 Injection
const getNode = inject('getNode');
const node = getNode();

const data = ref(node.getData() || {});
const label = ref(node.prop('label') || 'Machine');
const isSelected = ref(data.value.isSelected || false);

const updateData = () => {
    const newData = node.getData() || {};
    data.value = newData;
    isSelected.value = newData.isSelected || false;
};

// Listen to node changes
node.on('change:data', updateData);
node.on('change:label', ({ current }) => {
    label.value = current || 'Machine';
});

onUnmounted(() => {
    node.off('change:data', updateData);
    node.off('change:label');
});
</script>

<style scoped>
.machine-node {
    will-change: transform;
    /* Prevent default text selection during interaction */
    user-select: none;
}

@keyframes blink-red {
    0%, 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    50% { box-shadow: 0 0 15px 5px rgba(239, 68, 68, 0.5); border-color: rgba(239, 68, 68, 1); }
}

@keyframes blink-green {
    0%, 100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
    50% { box-shadow: 0 0 15px 5px rgba(34, 197, 94, 0.5); border-color: rgba(34, 197, 94, 1); }
}

.machine-blink-error {
    animation: blink-red 1.5s infinite;
}

.machine-blink-active {
    animation: blink-green 3s infinite;
}
</style>
