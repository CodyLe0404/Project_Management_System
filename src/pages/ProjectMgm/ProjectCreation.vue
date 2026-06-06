<route>
{
  meta: {
    title: "Thiết Lập Dự Án",
    icon: "pi pi-file-plus"
  }
}
</route>

<template>
  <section class="border rounded-lg p-2 mb-6 shadow-sm bg-white">
    <div class="p-6">
      <h1 class="text-2xl font-bold mb-4">⚙️ Thiết lập Dự án</h1>

      <!-- Khung 1: Thông tin chung -->
      <section class="border rounded-2xl p-5 mb-6 shadow-xl bg-slate-50">
      <h2 class="text-lg font-semibold text-slate-900">1. Thông tin chung</h2>
      <div class="flex gap-4">
        <div class="flex-1">
          <label class="block text-sm text-gray-600 mb-1">Số thứ tự (No)</label>
          <input v-model="general.no" type="text" class="w-full border rounded px-3 py-2" />
        </div>
            <div class="flex-1">
              <label class="block text-sm text-gray-600 mb-1">Project Number</label>
              <input v-model="general.projectNumber" type="text" class="w-full border rounded px-3 py-2" />
            </div>
            <div class="flex-1">
              <label class="block text-sm text-gray-600 mb-1">Project Name</label>
              <input v-model="general.projectName" type="text" class="w-full border rounded px-3 py-2" />
            </div>
        </div>
        </section>

        <!-- Khung 2: Hạng mục chính và ngân sách -->
      <section class="border rounded-2xl p-5 mb-6 shadow-xl bg-slate-50">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-5">
          <div>
            <h2 class="text-lg font-semibold text-slate-900">2. Hạng mục chính và ngân sách</h2>
            <!-- <p class="text-sm text-slate-500">Thêm hạng mục mới khi cần, và xóa nếu nhầm.</p> -->
          </div>
          <button @click="addItem" class="inline-flex items-center justify-center gap-2 rounded-full bg-sky-600 px-5 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-sky-700">
            <span>➕ Thêm Hạng mục mới</span>
          </button>
        </div>

        <div class="space-y-4">
            <div v-for="(item, idx) in items" :key="item.id" class="border rounded-2xl p-4 bg-white shadow-sm relative">
            <div class="flex items-center justify-between gap-3 mb-4">
                <div class="text-sm font-semibold text-slate-800">Task {{ idx + 1 }}</div>
                <button v-if="item.removable" @click="removeItem(idx)" type="button" class="inline-flex h-9 w-9 items-center justify-center rounded-full border border-red-200 bg-red-50 text-red-600 transition hover:bg-red-100 hover:text-red-800" title="Xóa hạng mục">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="h-4 w-4 fill-current">
                    <path d="M3 6h18v2H3V6zm3 3h12l-1.5 12.5c-.1.7-.7 1.2-1.4 1.2H8.9c-.7 0-1.3-.5-1.4-1.2L6 9zm5 2v8h2v-8h-2zm-4 0v8h2v-8H7zm8 0v8h2v-8h-2zM9 4V3h6v1h5v2H4V4h5z"/>
                </svg>
                </button>
            </div>

            <div class="grid gap-4 lg:grid-cols-[1.5fr_0.85fr_1.2fr] items-end">
              <div>
                <label class="block text-sm text-slate-600 mb-1">Hạng mục chính</label>
                <input v-model="item.main_task" type="text" placeholder="Ví dụ: LV" class="w-full border border-slate-300 rounded-2xl px-3 py-2 text-sm text-slate-900 focus:border-sky-400 focus:outline-none focus:ring-2 focus:ring-sky-100" />
              </div>
              <div>
                <label class="block text-sm text-slate-600 mb-1">Q'ty</label>
                <input v-model="item.qty" type="text" placeholder="0" class="w-full border border-slate-300 rounded-2xl px-3 py-2 text-sm text-slate-900 focus:border-sky-400 focus:outline-none focus:ring-2 focus:ring-sky-100" />
              </div>
              <div>
                <label class="block text-sm text-slate-600 mb-1">Ngân sách (Budget)</label>
                <input v-model="item.budget" type="text" placeholder="0" class="w-full border border-slate-300 rounded-2xl px-3 py-2 text-sm text-slate-900 focus:border-sky-400 focus:outline-none focus:ring-2 focus:ring-sky-100" />
              </div>
            </div>
            <div class="mt-4">
              <label class="block text-sm text-slate-600 mb-1">Danh sách công việc con</label>
              <textarea v-model="item.subtasks" rows="8" class="w-full border border-slate-300 rounded-2xl px-3 py-2 text-sm font-mono text-slate-800 focus:border-sky-400 focus:outline-none focus:ring-2 focus:ring-sky-100"></textarea>
            </div>
          </div>
        </div>
      </section>
    </div>
    <div class="mt-3 text-sm text-yellow-700 font-semibold bg-yellow-50 p-3 rounded border border-yellow-200" v-if="validationError">{{ validationError }}</div>
    <div class="mt-3 text-sm text-red-600" v-if="saveError">{{ saveError }}</div>
    <div class="mt-3 text-sm text-green-600 font-semibold" v-if="saveSuccess">✅ {{ saveSuccess }}</div>
    <div class="mt-5 flex flex-col items-end gap-2">
      <p class="text-sm text-slate-500" v-if="isSaving">Đang lưu dự án... Vui lòng chờ.</p>
      <button @click="createAndEmit" :disabled="isSaving" class="inline-flex items-center justify-center rounded-full bg-emerald-600 px-6 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:bg-slate-400">💾 KHỞI TẠO VÀ ĐƯA VÀO BẢNG</button>
    </div>
  </section>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { createProject } from '../../services/projectService'

const defaultSubtasks = `DE_SLD and Outline_diagram_R0
DE_Bill Of Material (LT)_R0
DE_Schematic diagram_R0
DE_Bill Of Material (ST)_R0
DE_Drawing for production_R0
DM_Assembly drawings_R0
DM_Bill Of Material (MD/LT)_R0
DM_DWG_Enclosure drawings (Frame, Top, Side)_R0
DM_DWG_Door drawings_R0
DM_DWG_Inner part drawings (DM)_R0
DM_DWG_Busbar drawings_R0
DM_DWG_Drawing for production_R0
DM_Bill Of Material(Final)_R0
DM_Final drawing_R0`

const general = reactive({ no: '', projectNumber: '', projectName: '' })
const isSaving = ref(false)
const saveError = ref('')
const saveSuccess = ref('')
const validationError = ref('')

let idCounter = 1
const items = ref([
  {
    id: idCounter++,
    main_task: '',
    qty: '',
    budget: '',
    subtasks: defaultSubtasks,
    removable: false
  }
])

const addItem = () => {
  items.value.push({ id: idCounter++, main_task: '', qty: '', budget: '', subtasks: defaultSubtasks, removable: true })
}

const removeItem = (index) => {
  items.value.splice(index, 1)
}

const emit = defineEmits(['create-project'])

const validateForm = () => {
  validationError.value = ''  // Reset lỗi validation cũ

  // Kiểm tra thông tin chung
  if (!general.no.trim()) {
    validationError.value = '⚠️ Vui lòng nhập Số thứ tự (No)'
    return false
  }

  if (!general.projectNumber.trim()) {
    validationError.value = '⚠️ Vui lòng nhập Project Number'
    return false
  }

  if (!general.projectName.trim()) {
    validationError.value = '⚠️ Vui lòng nhập Project Name'
    return false
  }

  // Kiểm tra danh sách công việc
  if (items.value.length === 0) {
    validationError.value = '⚠️ Vui lòng thêm ít nhất một hạng mục'
    return false
  }

  // Kiểm tra từng item
  for (let i = 0; i < items.value.length; i++) {
    const item = items.value[i]
    
    if (!item.main_task.trim()) {
      validationError.value = `⚠️ Vui lòng nhập Hạng mục chính cho Task ${i + 1}`
      return false
    }

    if (!item.budget.trim()) {
      validationError.value = `⚠️ Vui lòng nhập Ngân sách (Budget) cho Task ${i + 1}`
      return false
    }
  }

  return true
}

const createAndEmit = async () => {
  validationError.value = '' // Reset lỗi validation
  saveError.value = ''        // Reset lỗi cũ
  saveSuccess.value = ''      // Reset thông báo thành công cũ

  // Validate form trước khi lưu
  if (!validateForm()) {
    return
  }

  isSaving.value = true       // Bật trạng thái loading

  // Tạo clone dữ liệu để chuẩn bị gửi đi
  const payload = {
    general: { ...general },
    items: items.value.map(i => ({ ...i }))
  }

  try {
    // Gọi service gửi API lên server
    const result = await createProject(payload)
    console.log('Saved project id:', result.id)

    //Nếu thành công, hiển thị thông báo thành công
    saveSuccess.value = 'Dự án đã được tạo thành công!'
    
    // Auto-clear success message after 5 seconds
    setTimeout(() => {
      saveSuccess.value = ''
    }, 5000)

    //Emit event thông báo cho component cha kèm data
    emit('create-project', payload)
  } catch (error) {
    //Nếu lỗi, ghi nhận log và hiển thị thông báo lỗi lên giao diện
    console.error(error)
    saveError.value = error?.message || 'Lưu dự án thất bại.'
  } finally {
    isSaving.value = false      // Bất kể thành công hay thất bại, tắt trạng thái loading
  }
}
</script>
