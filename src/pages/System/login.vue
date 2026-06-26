<route>
{
  path: "/login",
  meta: {
    layout: "authentication",
    hidden: true
  }
}
</route>

<template>
  <Card class="shadow-xl border-none">
    <template #title>
        <div class="text-center mb-2">
            <h1 class="text-2xl font-bold text-surface-900 dark:text-surface-0">Welcome Back</h1>
            <p class="text-surface-500 dark:text-surface-400 font-normal text-base mt-2">Sign in with your Badge ID</p>
        </div>
    </template>
    
    <template #content>
        <form @submit.prevent="handleLogin" class="flex flex-col gap-4 mt-4">
            <div class="flex flex-col gap-1">
                <label for="userid" class="text-sm font-medium text-surface-700 dark:text-surface-300">User ID</label>
                <InputText id="userid" v-model="userId" placeholder="New Employee ID" class="w-full" :invalid="submitted && !userId" />
                <small v-if="submitted && !userId" class="text-red-500">User ID is required.</small>
            </div>
            
            <div class="flex flex-col gap-1">
                <label for="password" class="text-sm font-medium text-surface-700 dark:text-surface-300">Password</label>
                <Password id="password" v-model="password" placeholder="••••••••" toggleMask :feedback="false" inputClass="w-full" class="w-full" :invalid="submitted && !password" />
                 <small v-if="submitted && !password" class="text-red-500">Password is required.</small>
            </div>
            
            <div v-if="error" class="p-3 bg-red-50 text-red-600 rounded text-sm text-center">
                {{ error }}
            </div>
            
            <Button type="submit" label="Sign In" icon="pi pi-sign-in" :loading="loading" />
        </form>
    </template>
  </Card>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { Card, InputText, Password, Button } from 'primevue';

const router = useRouter()
const auth = useAuthStore()

const userId = ref('')
const password = ref('')
const loading = ref(false)
const submitted = ref(false)
const error = ref('')

const handleLogin = async () => {
  submitted.value = true;
  error.value = '';
  
  if (!userId.value || !password.value) return;

  loading.value = true;
  try {
      const success = await auth.login(userId.value, password.value);
      if (success) {
          router.push('/');
      } else {
          error.value = 'Invalid Credentials';
      }
  } catch (e) {
      error.value = e.message || 'Login failed';
  } finally {
      loading.value = false;
  }
}
</script>
