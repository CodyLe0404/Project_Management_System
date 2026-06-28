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
        <form v-if="!showChangePw" @submit.prevent="handleLogin" class="flex flex-col gap-4 mt-4">
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
            
            <div class="flex items-center justify-between gap-4">
              <Button type="submit" label="Sign In" icon="pi pi-sign-in" :loading="loading" />
              <Button type="button" label="Change Password" class="p-button-secondary" icon="pi pi-key" @click="toggleChangePassword" />
            </div>
        </form>

        <form v-else @submit.prevent="handleChangePassword" class="flex flex-col gap-4 mt-4">
            <div class="flex flex-col gap-1">
                <label for="cp-userid" class="text-sm font-medium text-surface-700 dark:text-surface-300">User ID</label>
                <InputText id="cp-userid" v-model="cpUserId" placeholder="User ID" class="w-full" :invalid="submitChangePW && !cpUserId" />
                <small v-if="submitChangePW && !cpUserId" class="text-red-500">User ID is required.</small>
            </div>
            
            <div class="flex flex-col gap-1">
                <label for="cp-current" class="text-sm font-medium text-surface-700 dark:text-surface-300">Current Password</label>
                <Password id="cp-current" v-model="cpCurrentPassword" placeholder="••••••••" toggleMask :feedback="false" inputClass="w-full" class="w-full" :invalid="submitChangePW && !cpCurrentPassword" />
                 <small v-if="submitChangePW && !cpCurrentPassword" class="text-red-500">Current password is required.</small>
            </div>

            <div class="flex flex-col gap-1">
                <label for="cp-new" class="text-sm font-medium text-surface-700 dark:text-surface-300">New Password</label>
                <Password id="cp-new" v-model="cpNewPassword" placeholder="••••••••" toggleMask :feedback="false" inputClass="w-full" class="w-full" :invalid="submitChangePW && !cpNewPassword" />
                 <small v-if="submitChangePW && !cpNewPassword" class="text-red-500">New password is required.</small>
            </div>

            <div v-if="cpError" class="p-3 bg-red-50 text-red-600 rounded text-sm text-center">
                {{ cpError }}
            </div>

            <div class="flex items-center justify-between gap-4">
              <Button type="submit" label="Submit" icon="pi pi-check" :loading="cpLoading" />
              <Button type="button" label="Cancel" class="p-button-secondary" icon="pi pi-times" @click="toggleChangePassword" />
            </div>
        </form>
        <div v-if="cpStatusMessage" :class="cpStatusSuccess ? 'p-3 bg-green-50 text-green-700 rounded text-sm text-center' : 'p-3 bg-red-50 text-red-600 rounded text-sm text-center'">
            {{ cpStatusMessage }}
        </div>
    </template>
  </Card>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { Card, InputText, Password, Button } from 'primevue';
import { changeUserPassword } from '../../services/projectService'

const router = useRouter()
const auth = useAuthStore()

const userId = ref('')
const password = ref('')
const loading = ref(false)
const submitted = ref(false)
const submitChangePW = ref(false)
const error = ref('')

const showChangePw = ref(false)
const cpUserId = ref('')
const cpCurrentPassword = ref('')
const cpNewPassword = ref('')
const cpLoading = ref(false)
const cpError = ref('')
const cpStatusMessage = ref('')
const cpStatusSuccess = ref(false)

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
          error.value = 'Wrong User ID or Password';
      }
  } catch (e) {
      error.value = e.message || 'Login failed';
  } finally {
      loading.value = false;
  }
}

const toggleChangePassword = () => {
    // reset state when toggling
    submitChangePW.value = false
    cpError.value = ''
    cpStatusMessage.value = ''
    cpStatusSuccess.value = false
    cpUserId.value = ''
    cpCurrentPassword.value = ''
    cpNewPassword.value = ''
    showChangePw.value = !showChangePw.value
}

const handleChangePassword = async () => {
    submitChangePW.value = true
    cpError.value = ''
    cpStatusMessage.value = ''
    cpStatusSuccess.value = false

    if (!cpUserId.value || !cpCurrentPassword.value || !cpNewPassword.value) return

    cpLoading.value = true
    try {
        const result = await changeUserPassword({ userId: cpUserId.value, currentPassword: cpCurrentPassword.value, newPassword: cpNewPassword.value })

        if (result.status === 1) {
            cpStatusSuccess.value = true
            cpStatusMessage.value = 'Password has been updated.'
            showChangePw.value = false
        } else {
            cpStatusSuccess.value = false
            cpStatusMessage.value = 'Incorrect username or current password.'
        }
    } catch (e) {
        cpError.value = e.message || 'Change password failed'
    } finally {
        cpLoading.value = false
    }
}
</script>
