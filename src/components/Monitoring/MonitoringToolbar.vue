<template>
    <div class="flex items-center justify-between p-4 bg-surface-0 dark:bg-surface-900 border-b border-surface-200 dark:border-surface-700">
        <div class="flex items-center gap-4">
            <div class="flex-col">
                <h1 class="text-xl font-bold text-surface-900 dark:text-surface-0">Factory Floor Map</h1>
                 <div class="text-xs text-surface-500 flex items-center gap-2">
                    <span :class="{'text-green-600 font-medium': isAdmin, 'text-surface-500': !isAdmin}">
                        {{ isAdmin ? 'Admin Access' : 'View Only' }}
                    </span>
                 </div>
            </div>
        </div>

        <div class="flex items-center gap-4">
            <!-- Blink Toggle -->
            <div class="flex items-center gap-2">
                <InputSwitch :modelValue="blinkingEnabled" @update:modelValue="$emit('update:blinkingEnabled', $event)" inputId="blink-switch" />
                <label for="blink-switch" class="text-sm font-medium">Blink Status</label>
            </div>

            <div class="h-8 w-[1px] bg-surface-200 dark:bg-surface-700 mx-2"></div>

            <!-- Admin Actions -->
            <template v-if="isAdmin">
                <!-- Lock Toggle -->
                <Button 
                    :icon="isMapUnlocked ? 'pi pi-lock-open' : 'pi pi-lock'" 
                    :label="isMapUnlocked ? 'Unlocked' : 'Locked'"
                    :severity="isMapUnlocked ? 'warn' : 'secondary'"
                    text
                    size="small"
                    :title="isMapUnlocked ? 'Click to Lock Map' : 'Click to Unlock Map'"
                    @click="$emit('toggle-lock')"
                />

                <!-- Editor Palette (Only when Unlocked) -->
                <template v-if="isMapUnlocked">
                    <div class="h-6 w-[1px] bg-surface-200 dark:bg-surface-700 mx-1"></div>
                    
                    <div class="flex items-center gap-1 bg-surface-100 dark:bg-surface-800 p-1 rounded-lg">
                        <Button 
                            icon="pi pi-box" 
                            text 
                            severity="secondary" 
                            size="small"
                            title="Add Group Box"
                            @click="$emit('add-group')"
                        />
                        <Button 
                            icon="pi pi-receipt" 
                            text 
                            severity="secondary" 
                            size="small"
                            title="Add Text Label"
                            @click="$emit('add-text')"
                        />
                        <Button 
                            icon="pi pi-share-alt" 
                            :severity="isConnectionMode ? 'primary' : 'secondary'" 
                            :text="!isConnectionMode"
                            size="small"
                            title="Toggle Connection Mode"
                            @click="$emit('toggle-connection-mode')"
                        />
                    </div>

                    <div class="h-6 w-[1px] bg-surface-200 dark:bg-surface-700 mx-1"></div>
                </template>

                <!-- Save Layout (Only visible if Unlocked AND Dirty) -->
                <Button 
                    v-if="isMapUnlocked && hasUnsavedChanges"
                    label="Save Layout" 
                    icon="pi pi-save" 
                    severity="primary" 
                    size="small"
                    title="Save current positions"
                    @click="$emit('save')"
                />
                
                 <Button 
                    label="Reset" 
                    icon="pi pi-refresh" 
                    severity="danger" 
                    text
                    size="small"
                    title="Undo changes and reload last saved layout"
                    @click="$emit('reset')"
                />
            </template>
        </div>
    </div>
</template>

<script setup>
import { InputSwitch, Button } from 'primevue';

defineProps({
    isAdmin: Boolean,
    blinkingEnabled: Boolean,
    hasUnsavedChanges: Boolean,
    isMapUnlocked: Boolean,
    isConnectionMode: Boolean
});

defineEmits(['update:blinkingEnabled', 'save', 'reset', 'toggle-lock', 'add-group', 'add-text', 'toggle-connection-mode']);
</script>
