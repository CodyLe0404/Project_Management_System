<route>
{
  meta: {
    title: "User Profile",
    icon: "pi pi-user",
    hidden: true
  }
}
</route>

<template>
    <div class="max-w-xl">
        <h1 class="text-2xl font-bold mb-6">User Profile</h1>
        
        <div class="flex flex-col gap-4">
            <div class="flex flex-col gap-2">
                <label class="font-medium">Username</label>
                <input type="text" value="Demo User" disabled class="p-2 border rounded bg-surface-50" />
            </div>
            <div class="flex flex-col gap-2">
                <label class="font-medium">Email</label>
                <input type="email" value="demo@example.com" disabled class="p-2 border rounded bg-surface-50" />
            </div>
            <button class="bg-primary-500 text-white px-4 py-2 rounded self-start mt-2">Update Profile</button>
        </div>
    </div>
</template>
