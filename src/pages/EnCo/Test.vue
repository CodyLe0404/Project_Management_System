<route>
{
  meta: {
    title: "EnCo API Tester",
    icon: "pi pi-beaker",
    permission: ["admin"],
    hidden: true
  }
}
</route>

<template>
    <div class="p-4">
        <h1 class="text-2xl font-bold mb-4">EnCo API Service Tester</h1>

        <Accordion :multiple="true" :activeIndex="[0]">
            <!-- Call SP -->
            <AccordionTab header="Call SP">
                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">SP Name</label>
                        <InputText v-model="callSp.spName" placeholder="e.g., sp_get_user_data" class="w-full mt-1" />
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">DB Key</label>
                        <InputText v-model="callSp.dbKey" class="w-full mt-1" />
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">SP Query (JSON)</label>
                        <Textarea v-model="callSp.spQuery" rows="5" class="w-full mt-1" placeholder='{ "param1": "value1" }' />
                    </div>
                    <div class="flex items-center">
                        <Checkbox v-model="callSp.logSave" :binary="true" inputId="logSaveSp" />
                        <label for="logSaveSp" class="ml-2">Log Save</label>
                    </div>
                    <Button @click="handleCallSp" label="Execute Call SP" :loading="isLoading" />
                </div>
            </AccordionTab>

            <!-- Call SC -->
            <AccordionTab header="Call SC">
                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">SQL Command (SC)</label>
                        <Textarea v-model="callSc.scQuery" rows="5" class="w-full mt-1" placeholder="e.g., SELECT * FROM Users" />
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">DB Key</label>
                        <InputText v-model="callSc.dbKey" class="w-full mt-1" />
                    </div>
                    <div class="flex items-center">
                        <Checkbox v-model="callSc.logSave" :binary="true" inputId="logSaveSc" />
                        <label for="logSaveSc" class="ml-2">Log Save</label>
                    </div>
                    <Button @click="handleCallSc" label="Execute Call SC" :loading="isLoading" />
                </div>
            </AccordionTab>
            
            <!-- File Ops -->
            <AccordionTab header="File Ops">
                 <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Command</label>
                        <InputText v-model="fileOps.command" placeholder="e.g., list" class="w-full mt-1" />
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Operation (JSON)</label>
                        <Textarea v-model="fileOps.operation" rows="5" class="w-full mt-1" placeholder='{ "path": "/" }' />
                    </div>
                    <Button @click="handleFileOps" label="Execute File Ops" :loading="isLoading" />
                </div>
            </AccordionTab>

            <!-- Upload File -->
            <AccordionTab header="Upload File">
                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">File</label>
                        <input type="file" @change="onFileSelect" class="mt-1" />
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Metadata (JSON)</label>
                        <Textarea v-model="uploadFile.metadata" rows="3" class="w-full mt-1" placeholder='{ "description": "A test file" }' />
                    </div>
                    <Button @click="handleUploadFile" label="Execute Upload" :disabled="!uploadFile.file" :loading="isLoading" />
                </div>
            </AccordionTab>

            <!-- Download File -->
            <AccordionTab header="Download File">
                <div class="space-y-4">
                     <div>
                        <label class="block text-sm font-medium text-gray-700">File Path</label>
                        <InputText v-model="downloadFile.filePath" placeholder="e.g., /path/to/your/file.txt" class="w-full mt-1" />
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">File Name</label>
                        <InputText v-model="downloadFile.fileName" placeholder="e.g., downloaded_file.txt" class="w-full mt-1" />
                    </div>
                    <Button @click="handleDownloadFile" label="Execute Download" :loading="isLoading" />
                </div>
            </AccordionTab>

            <!-- Send Email -->
            <AccordionTab header="Send Email">
                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">To (comma-separated)</label>
                        <InputText v-model="sendEmail.to" class="w-full mt-1" />
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Subject</label>
                        <InputText v-model="sendEmail.subject" class="w-full mt-1" />
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Body</label>
                        <Textarea v-model="sendEmail.body" rows="5" class="w-full mt-1" />
                    </div>
                    <Button @click="handleSendEmail" label="Execute Send Email" :loading="isLoading" />
                </div>
            </AccordionTab>

        </Accordion>

        <!-- Response and Error Display -->
        <div v-if="response || error" class="mt-6">
            <h2 class="text-xl font-semibold" :class="error ? 'text-red-600' : 'text-green-600'">
                {{ error ? 'Error' : 'Response' }}
            </h2>
            <pre class="mt-2 p-3 rounded-md overflow-auto text-sm" :class="error ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-800'">{{ JSON.stringify(response || error, null, 2) }}</pre>
        </div>
    </div>
</template>

<script setup>
import { ref, inject } from 'vue';
import { Accordion, AccordionTab, InputText, Textarea, Button, Checkbox } from 'primevue';

const apiClient = inject('apiClient');

const isLoading = ref(false);
const response = ref(null);
const error = ref(null);

// Data for each API method
const callSp = ref({ spName: '', dbKey: 'CIMitar', spQuery: '{}', logSave: false });
const callSc = ref({ scQuery: '', dbKey: 'CIMitar', logSave: false });
const fileOps = ref({ command: 'list', operation: '{"path": "/"}' });
const uploadFile = ref({ file: null, metadata: '{}' });
const downloadFile = ref({ filePath: '', fileName: '' });
const sendEmail = ref({ to: '', subject: 'Test Email', body: 'This is a test email from the EnCo API Tester.'});


const executeApi = async (apiCall) => {
    isLoading.value = true;
    response.value = null;
    error.value = null;
    try {
        const result = await apiCall();
        response.value = result;
    } catch (e) {
        error.value = e.message || e;
        console.error(e);
    } finally {
        isLoading.value = false;
    }
};

const handleCallSp = () => executeApi(() => {
    const params = JSON.parse(callSp.value.spQuery);
    return apiClient.callSp(callSp.value.spName, params, callSp.value.dbKey, callSp.value.logSave);
});

const handleCallSc = () => executeApi(() => {
    return apiClient.callSc(callSc.value.scQuery, callSc.value.dbKey, callSc.value.logSave);
});

const handleFileOps = () => executeApi(() => {
    const operation = JSON.parse(fileOps.value.operation);
    return apiClient.callFileOps(fileOps.value.command, operation);
});

const onFileSelect = (event) => {
    uploadFile.value.file = event.target.files[0];
};

const handleUploadFile = () => executeApi(() => {
    const metadata = JSON.parse(uploadFile.value.metadata);
    return apiClient.uploadFile(uploadFile.value.file, metadata);
});

const handleDownloadFile = async () => {
    isLoading.value = true;
    response.value = null;
    error.value = null;
    try {
        const { filename, blob } = await apiClient.downloadFile({
            filePath: downloadFile.value.filePath,
            fileName: downloadFile.value.fileName
        });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
        response.value = { message: `File '${filename}' downloaded successfully.`, size: blob.size };
    } catch (e) {
        error.value = e.message || e;
        console.error(e);
    } finally {
        isLoading.value = false;
    }
};

const handleSendEmail = () => executeApi(() => {
    return apiClient.sendEmail({
        toMailList: sendEmail.value.to.split(',').map(e => e.trim()),
        subject: sendEmail.value.subject,
        body: sendEmail.value.body,
        mailPriority: 'Normal',
        sender: 'no-reply@example.com' // You might want to configure this
    });
});

</script>
