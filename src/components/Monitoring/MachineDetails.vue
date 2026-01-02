<template>
    <div class="h-full flex flex-col bg-surface-0 dark:bg-surface-900 border-l border-surface-200 dark:border-surface-700">
        <!-- Header -->
        <div class="p-4 border-b border-surface-200 dark:border-surface-700 bg-surface-50 dark:bg-surface-800 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <Avatar icon="pi pi-cog" size="large" shape="circle" class="bg-primary-100 text-primary-600" />
                <div>
                    <h2 class="text-xl font-bold">{{ machine?.label || 'Select Machine' }}</h2>
                    <span v-if="machine" class="text-sm text-surface-500">ID: {{ machine?.id }}</span>
                </div>
            </div>
            <Button v-if="machine" icon="pi pi-times" text rounded aria-label="Close" @click="$emit('close')" />
        </div>

        <!-- Content -->
        <div v-if="machine" class="p-6 flex-1 overflow-y-auto flex flex-col gap-6">
            <!-- Status Card -->
            <div class="p-4 rounded-lg border border-surface-200 dark:border-surface-700 bg-surface-50 dark:bg-surface-800">
                <div class="flex justify-between items-center mb-4">
                    <span class="text-sm font-medium uppercase tracking-wider text-surface-500">Current Status</span>
                    <Tag :value="machine.data.status" :severity="getStatusSeverity(machine.data.status)" />
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div class="text-center p-3 bg-surface-0 dark:bg-surface-900 rounded border border-surface-100 dark:border-surface-700">
                        <div class="text-2xl font-bold text-surface-900 dark:text-surface-0">{{ machine.data.temp }}°C</div>
                        <div class="text-xs text-surface-500 mt-1">Temperature</div>
                    </div>
                    <div class="text-center p-3 bg-surface-0 dark:bg-surface-900 rounded border border-surface-100 dark:border-surface-700">
                        <div class="text-2xl font-bold text-surface-900 dark:text-surface-0">{{ machine.data.load }}</div>
                        <div class="text-xs text-surface-500 mt-1">Load</div>
                    </div>
                </div>
            </div>

            <!-- Maintenance Info -->
            <div>
                <h3 class="font-bold mb-3">Maintenance</h3>
                <div class="flex justify-between py-2 border-b border-surface-100 dark:border-surface-700">
                    <span class="text-surface-600">Last Maintenance</span>
                    <span class="font-medium">{{ machine.data.lastMaintenance }}</span>
                </div>
                <div class="flex justify-between py-2 border-b border-surface-100 dark:border-surface-700">
                    <span class="text-surface-600">Technician</span>
                    <span class="font-medium">John Doe</span>
                </div>
            </div>

            <Divider />

            <!-- Actions -->
             <div class="flex gap-3">
                <Button label="Report" severity="danger" icon="pi pi-exclamation-triangle" outlined class="flex-1" />
                <Button label="Logs" severity="secondary" icon="pi pi-list" outlined class="flex-1" />
             </div>
        </div>
        
        <!-- Empty State -->
        <div v-else class="flex-1 flex flex-col items-center justify-center p-8 text-center text-surface-500">
            <i class="pi pi-map-marker text-4xl mb-4 text-surface-300 dark:text-surface-600"></i>
            <p>Select a machine on the map to view details.</p>
        </div>
    </div>
</template>

<script setup>
import { Avatar, Tag, Divider, Button } from 'primevue';

defineProps({
    machine: Object
});

defineEmits(['close']);

const getStatusSeverity = (status) => {
    switch (status) {
        case 'running': return 'success';
        case 'idle': return 'warn';
        case 'error': return 'danger';
        default: return 'info';
    }
};
</script>
