<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

const selectedFile = ref<File | null>(null)
const isUploading = ref(false)
const uploadSuccess = ref(false)
const uploadError = ref('')
const VITE_BACKEND_URL = import.meta.env.VITE_API_URL

const handleFileUpload = (event: Event) => {
  const input = event.target as HTMLInputElement
  const files = input.files

  uploadSuccess.value = false
  uploadError.value = ''

  if (files && files.length > 0) {
    selectedFile.value = files[0]
  }
}

const removeFile = () => {
  selectedFile.value = null
  uploadSuccess.value = false
  uploadError.value = ''
}

const formatFileSize = (size: number) => {
  if (size < 1024) return `${size} B`
  if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`
  return `${(size / (1024 * 1024)).toFixed(1)} MB`
}

const getFileIcon = (file: File) => {
  const extension = file.name.split('.').pop()?.toLowerCase()

  if (extension === 'csv') return 'pi pi-file'
  if (extension === 'parquet') return 'pi pi-database'
  if (extension === 'xls' || extension === 'xlsx') return 'pi pi-file-excel'

  return 'pi pi-file'
}

const uploadFile = async () => {
  if (!selectedFile.value) return

  isUploading.value = true
  uploadSuccess.value = false
  uploadError.value = ''

  const formData = new FormData()

  formData.append('file', selectedFile.value)

  try {
    const response = await axios.post(
      `${VITE_BACKEND_URL}/uploads/upload-file`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    )

    console.log('Upload success:', response.data)

    uploadSuccess.value = true
    selectedFile.value = null
  } catch (error: any) {
    if (error.response) {
      console.error('Server Error Data:', error.response.data)
      console.error('Server Status:', error.response.status)

      uploadError.value =
        error.response.data?.detail || 'Something went wrong while uploading the file.'
    } else {
      console.error('Upload failed:', error.message)

      uploadError.value = 'Unable to connect to the server.'
    }
  } finally {
    isUploading.value = false
  }
}
</script>

<template>
  <div
    class="tw-min-h-screen tw-bg-slate-50 tw-flex tw-items-center tw-justify-center tw-p-6"
  >
    <div class="tw-w-full tw-max-w-2xl">

      <!-- Header -->
      <div class="tw-text-center tw-mb-8">
        <div
          class="tw-mx-auto tw-mb-4 tw-flex tw-h-16 tw-w-16 tw-items-center tw-justify-center tw-rounded-2xl tw-bg-blue-600 tw-shadow-lg tw-shadow-blue-200"
        >
          <i class="pi pi-cloud-upload tw-text-3xl tw-text-white"></i>
        </div>

        <h1
          class="tw-text-3xl tw-font-bold tw-text-slate-900"
        >
          Upload your data
        </h1>

        <p
          class="tw-mt-2 tw-text-slate-500"
        >
          Upload a dataset to get started with your analysis.
        </p>
      </div>

      <!-- Upload Card -->
      <Card
        class="tw-border tw-border-slate-200 tw-shadow-sm"
      >
        <template #content>

          <!-- Dropzone -->
          <label
            for="file-upload"
            class="tw-group tw-flex tw-cursor-pointer tw-flex-col tw-items-center tw-justify-center tw-rounded-2xl tw-border-2 tw-border-dashed tw-border-slate-300 tw-bg-slate-50 tw-px-6 tw-py-12 tw-transition-all hover:tw-border-blue-400 hover:tw-bg-blue-50"
          >
            <div
              class="tw-mb-4 tw-flex tw-h-14 tw-w-14 tw-items-center tw-justify-center tw-rounded-full tw-bg-blue-100 tw-transition-transform group-hover:tw-scale-110"
            >
              <i
                class="pi pi-upload tw-text-2xl tw-text-blue-600"
              ></i>
            </div>

            <p class="tw-text-base tw-font-semibold tw-text-slate-700">
              Click to choose a file
            </p>

            <p class="tw-mt-1 tw-text-sm tw-text-slate-400">
              CSV, Parquet, XLS or XLSX
            </p>
            <p class="tw-mt-1 tw-text-sm tw-text-slate-600">
              File size limit: 20MB
            </p>

            <input
              id="file-upload"
              type="file"
              accept=".csv,.parquet,.xls,.xlsx"
              class="tw-hidden"
              @change="handleFileUpload"
            />
          </label>

          <!-- Selected File -->
          <div
            v-if="selectedFile"
            class="tw-mt-6 tw-rounded-xl tw-border tw-border-slate-200 tw-bg-white tw-p-4"
          >
            <div class="tw-flex tw-items-center tw-gap-4">

              <!-- File Icon -->
              <div
                class="tw-flex tw-h-12 tw-w-12 tw-shrink-0 tw-items-center tw-justify-center tw-rounded-xl tw-bg-blue-50"
              >
                <i
                  :class="[
                    getFileIcon(selectedFile),
                    'tw-text-xl tw-text-blue-600'
                  ]"
                ></i>
              </div>

              <!-- File Information -->
              <div class="tw-min-w-0 tw-flex-1">
                <p
                  class="tw-truncate tw-font-semibold tw-text-slate-800"
                >
                  {{ selectedFile.name }}
                </p>

                <p class="tw-mt-1 tw-text-sm tw-text-slate-400">
                  {{ formatFileSize(selectedFile.size) }}
                </p>
              </div>

              <!-- Remove -->
              <Button
                icon="pi pi-times"
                severity="secondary"
                text
                rounded
                aria-label="Remove file"
                @click="removeFile"
              />
            </div>
          </div>

          <!-- Success -->
          <Message
            v-if="uploadSuccess"
            severity="success"
            class="tw-mt-5"
          >
            File uploaded successfully!
          </Message>

          <!-- Error -->
          <Message
            v-if="uploadError"
            severity="error"
            class="tw-mt-5"
          >
            {{ uploadError }}
          </Message>

          <!-- Upload Button -->
          <Button
            class="tw-mt-6 tw-w-full tw-bg-blue-600"
            :disabled="!selectedFile || isUploading"
            :loading="isUploading"
            label="Upload File"
            icon="pi pi-cloud-upload"
            size="large"
            @click="uploadFile"
          />

        </template>
      </Card>

      <!-- Supported Formats -->
      <div
        class="tw-mt-6 tw-flex tw-items-center tw-justify-center tw-gap-5 tw-text-xs tw-text-slate-400"
      >
        <span>
          <i class="pi pi-check-circle tw-mr-1"></i>
          CSV
        </span>

        <span>
          <i class="pi pi-check-circle tw-mr-1"></i>
          Parquet
        </span>

        <span>
          <i class="pi pi-check-circle tw-mr-1"></i>
          Excel
        </span>
      </div>

    </div>
  </div>
</template>