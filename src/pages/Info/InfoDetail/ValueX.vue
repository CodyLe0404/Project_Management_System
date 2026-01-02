<route>
{
  meta: {
    title: "Value X Detail",
    icon: "pi pi-file"
  }
}
</route>

<template>
  <div>
    <Button label="Back to Dashboard" icon="pi pi-arrow-left" text @click="$router.push('/')" class="mb-4" />
    
    <Card>
        <template #title>
            <div class="flex items-center gap-3">
                <i class="pi pi-folder-open text-primary-500 text-2xl"></i>
                <span>Nested Route: ValueX</span>
            </div>
        </template>
        <template #subtitle>
            Path: <code class="bg-surface-100 p-1 rounded text-primary-600">/Info/InfoDetail/ValueX</code>
        </template>
        <template #content>
            <div class="p-4 bg-primary-50 border border-primary-100 rounded text-primary-900">
                <p class="leading-relaxed">
                    This page automatically appeared in the sidebar menu because you created the file:
                    <br>
                    <strong>src/pages/Info/InfoDetail/ValueX.vue</strong>
                </p>
                <p class="mt-2 text-sm text-primary-700">
                    The <code>getMenuItems</code> utility automatically parses the folder structure to build the <code>PanelMenu</code> you see on the left.
                </p>
            </div>
        </template>
    </Card>
  </div>
</template>

<script setup>
import { Card, Button } from 'primevue';
</script>
