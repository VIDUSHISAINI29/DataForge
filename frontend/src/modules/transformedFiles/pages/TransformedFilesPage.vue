<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useFileStore } from '@/shared/store/fileStore';
import {
  getTransformedFilesList,
  queryTransformedFile,
} from '../api/transformedFiles.api';

const fileStore = useFileStore();

const VITE_BACKEND_URL = import.meta.env.VITE_API_URL;

const rows = computed(() => {
  return fileStore.currentFile?.data ?? [];
});

const columns = computed(() => {
  return fileStore.currentFile?.columns ?? [];
});

// Export API
const showExportDialog = ref(false);
const copied = ref(false);

const exportedApiUrl = computed(() => {
  const fileName = fileStore.currentFileName;

  if (!fileName) {
    return '';
  }

  return `${VITE_BACKEND_URL}/reads/export/${encodeURIComponent(fileName)}`;
});

const openExportDialog = () => {
  copied.value = false;
  showExportDialog.value = true;
};

const copyApiUrl = async () => {
  const text = exportedApiUrl.value;

  if (!text) {
    return;
  }

  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
    } else {
      const textArea = document.createElement('textarea');

      textArea.value = text;
      textArea.style.position = 'fixed';
      textArea.style.left = '-999999px';
      textArea.style.top = '-999999px';

      document.body.appendChild(textArea);

      textArea.focus();
      textArea.select();

      document.execCommand('copy');

      document.body.removeChild(textArea);
    }

    copied.value = true;

    setTimeout(() => {
      copied.value = false;
    }, 2000);
  } catch (error) {
    console.error('Failed to copy API URL:', error);
    copied.value = false;
  }
};

// SQL Query
const query = ref(`
SELECT *
FROM data
LIMIT 2
`);

const loading = ref(false);
const error = ref('');

const queryResult = ref<{
  columns: string[];
  data: Record<string, any>[];
} | null>(null);

const runQuery = async () => {
  if (!query.value.trim()) {
    return;
  }
  if (fileStore.currentFileName === null) {
    error.value =
      'No file selected. Please select a transformed file to run the query.';
    return;
  }

  loading.value = true;
  error.value = '';

  try {
    const response = await queryTransformedFile({
      file_name: fileStore.currentFileName,
      query: query.value,
    });

    queryResult.value = response.result;

    // Show query result in the table
    fileStore.currentFile = queryResult.value;

   //  console.log('query result - ', response.result);
  } catch (err: any) {
    console.log('err in querying transformed file - ', err);
   if (fileStore.currentFileName === null) {
    error.value =
      'No file selected. Please select a transformed file to run the query.';
    return;
  } else{
     error.value =
       err.response?.data?.detail ||
       'Failed to execute query';
  }
  } finally {
    loading.value = false;
  }
};

// Get transformed files list
const getTransformedFilesListFunction = async () => {
  try {
    const res = await getTransformedFilesList();

    fileStore.transformedFilesList = res?.files;

   //  console.log('files transformed list - ',res?.files);
   
  } catch (err: any) {
    if (err.response) {
      console.error(
        'Server Error Data:',
        err.response.data
      );

      console.error(
        'Server Status:',
        err.response.status
      );
    } else {
      console.error(
        'Read failed:',
        err.message
      );
    }
  }
};

onMounted(async () => {
  await getTransformedFilesListFunction();
});
</script>

<template>
  <div class="tw-m-1 tw-flex tw-flex-col tw-gap-2 tw-p-2">
    <!-- SQL Editor -->
    <div class="tw-flex tw-flex-col tw-gap-2">
      <div class="tw-flex tw-items-center tw-justify-between">
        <span class="tw-font-semibold">
          SQL Query
        </span>

        <div class="tw-flex tw-gap-2">
          <Button
            label="Run Query"
            icon="pi pi-play"
            class="tw-border-blue-600 tw-bg-blue-600"
            :loading="loading"
            @click="runQuery"
          />

          <Button
            label="Export API"
            icon="pi pi-link"
            class="tw-border-blue-200 tw-bg-blue-200 tw-text-blue-600"
            severity="secondary"
            :disabled="!fileStore.currentFileName"
            @click="openExportDialog"
          />
        </div>
      </div>

      <div>
        <p class="tw-text-sm tw-text-gray-600">
          Use "data" to reference the selected transformed file.
        </p>
        <p class="tw-text-sm tw-text-gray-700">
                  Here only select queries are allowed
               </p>
      </div>

      <textarea
        v-model="query"
        class="tw-min-h-[220px] tw-w-full tw-rounded-lg tw-border tw-p-4 tw-font-mono tw-text-sm"
        placeholder="Write your SQL query..."
        spellcheck="false"
      />
    </div>

    <!-- Error -->
    <Message
      v-if="error"
      severity="error"
    >
      {{ error }}
    </Message>

    <!-- Selected File -->
    <div
      v-if="fileStore.currentFile"
      class="tw-overflow-x-auto"
    >
      <span
        class="tw-mt-6 tw-px-1 tw-text-lg tw-font-semibold"
      >
        {{ fileStore.currentFileName }}
      </span>
    </div>

    <!-- Result -->
    <div
      v-if="fileStore.currentFile"
      class="tw-w-full tw-overflow-x-auto"
    >
      <DataTable
        :value="rows"
        paginator
        :rows="5"
        tableStyle="min-width: 50rem"
      >
        <Column
          v-for="col in columns"
          :key="col"
          :field="col"
          :header="col"
        />
      </DataTable>
    </div>

    <!-- Empty State -->
    <div
      v-else
      class="tw-flex tw-h-52 tw-w-full tw-items-center tw-justify-center"
    >
      <span class="tw-font-semibold">
        Select transformed file to see data.
      </span>
    </div>
  </div>

  <!-- Export Dialog -->
  <Dialog
    v-model:visible="showExportDialog"
    modal
    header="Export API"
    :style="{ width: '40rem' }"
  >
    <div class="tw-flex tw-flex-col tw-gap-4">
      <div>
        <p class="tw-m-0 tw-text-sm tw-text-gray-500">
          Your transformed file is available through this API:
        </p>
      </div>

      <div class="tw-flex tw-items-center tw-gap-2">
        <InputText
          :value="exportedApiUrl"
          readonly
          class="tw-flex-1"
        />

        <Button
          class="tw-border-blue-600 tw-bg-blue-600 tw-text-white"
          :label="copied ? 'Copied!' : 'Copy'"
          :icon="copied ? 'pi pi-check' : 'pi pi-copy'"
          @click="copyApiUrl"
        />
      </div>

      <div class="tw-flex tw-justify-end">
        <Button
          label="Close"
          severity="secondary"
          @click="showExportDialog = false"
        />
      </div>
    </div>
  </Dialog>
</template>

<style scoped>
</style>