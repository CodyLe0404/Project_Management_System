<route>
{
  meta: {
    title: "KPI Phòng Ban",
    icon: "pi pi-users",
    permission: ["DS_PMS_DK"],
  }
}
</route>

<template>
  <section class="border rounded-lg p-2 mb-6 shadow-sm bg-white">
    <div class="p-6">
      <h1 class="text-2xl font-bold mb-4"> Coming soon 🤏</h1>
    </div>
    <div>
      <!-- <p>{{ authStore.user.displayName }}</p>
      <p>{{ authStore.user.userId}}</p>
      <p>{{ authStore }}</p> -->
    </div>
  </section>
</template>

<script setup>
import { useAuthStore } from '../../stores/auth';

const authStore = useAuthStore();


</script>
