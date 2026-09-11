<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { ref } from 'vue';
import { useFileStore } from '@/shared/store/fileStore';

const fileStore = useFileStore();

const route = useRoute();
const router = useRouter();

const VITE_BACKEND_URL = import.meta.env.VITE_API_URL;

const selectedFile = ref<string | null>(null);
const openMenu = ref<string | null>(null);
const isMobileMenuOpen = ref(false);

const menuItems = [
  {
    name: 'Upload File',
    icon: 'pi-cloud-upload',
    routes: ['/upload-file'],
  },
  {
    name: 'Raw Files',
    icon: 'pi-file',
    routes: ['/raw-files'],
  },
  {
    name: 'Transformed Files',
    icon: 'pi-file-import',
    routes: ['/transformed-files'],
  },
];

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false;
};

const isActive = (item: (typeof menuItems)[number]) => {
  return item.routes.some((path) => route.path.startsWith(path));
};

const selectFile = async (fileName: string) => {
  selectedFile.value = fileName;
  fileStore.currentFileName = fileName;

  await getSelectedFilePreview(fileName);

  // Close mobile menu after selecting a file
  isMobileMenuOpen.value = false;
};

const getSelectedFilePreview = async (fileName: string) => {
  try {
    const encodedFileName = encodeURIComponent(fileName);

    let endpoint = '';

    if (route.path === '/raw-files') {
      endpoint = `/reads/raw-file-preview/${encodedFileName}`;
    } else {
      endpoint = `/reads/transformed-file-preview/${encodedFileName}`;
    }

    const response = await axios.get(
      `${VITE_BACKEND_URL}${endpoint}`,
    );

    fileStore.currentFile = response.data;
    fileStore.currentFileName = fileName;

  } catch (error: any) {
    if (error.response) {
      console.error('Server Error Data:', error.response.data);
      console.error('Server Status:', error.response.status);
    } else {
      console.error(
        'Preview Read failed:',
        error.message,
      );
    }
  }
};

const clickMenuItem = (menuItem: (typeof menuItems)[number]) => {
  const hasSubMenu =
    menuItem.name === 'Raw Files' ||
    menuItem.name === 'Transformed Files';

  if (hasSubMenu) {
    openMenu.value =
      openMenu.value === menuItem.name
        ? null
        : menuItem.name;

    if (route.path !== menuItem.routes[0]) {
      router.push(menuItem.routes[0]);
    }

    return;
  }

  openMenu.value = null;
  isMobileMenuOpen.value = false;

  router.push(menuItem.routes[0]);
};

const getFilesForMenu = (menuName: string) => {
  if (menuName === 'Raw Files') {
    return fileStore.rawFilesList;
  }

  if (menuName === 'Transformed Files') {
    return fileStore.transformedFilesList;
  }

  return [];
};
</script>

<template>
  <!-- Mobile menu button -->
  <div
    class="tw-sticky tw-left-4 tw-top-4 tw-z-50 tw-mb-10 tw-flex tw-w-3/5 tw-justify-between lg:tw-hidden"
  >
    <button
      @click="isMobileMenuOpen = true"
      class="tw-flex tw-h-10 tw-w-10 tw-items-center tw-justify-center tw-rounded-md tw-bg-blue-600 tw-text-white"
    >
      <i class="pi pi-bars"></i>
    </button>

    <span
      class="tw-text-2xl tw-font-bold tw-text-blue-600"
    >
      Data Forge
    </span>
  </div>

  <!-- Overlay -->
  <div
    v-if="isMobileMenuOpen"
    @click="closeMobileMenu"
    class="tw-fixed tw-inset-0 tw-z-40 tw-bg-black/40 lg:tw-hidden"
  ></div>

  <!-- Sidebar -->
  <aside
    :class="[
      'tw-fixed tw-left-0 tw-top-0 tw-z-50 tw-h-screen tw-w-64 tw-bg-white tw-p-2 tw-transition-transform tw-duration-300 lg:tw-static lg:tw-z-auto lg:tw-h-auto lg:tw-translate-x-0',
      isMobileMenuOpen
        ? 'tw-translate-x-0'
        : '-tw-translate-x-full',
    ]"
  >
    <!-- Header -->
    <div
      class="tw-flex tw-items-center  tw-border-b-[1px] tw-px-2 tw-pb-2"
    >
    <img class="tw-w-10 tw-h-10" src="/images/DataForgeLogo.png" alt="">
      <span
        class="tw-text-2xl tw-font-bold tw-text-blue-600"
      >
        Data-Forge
      </span>

      <!-- Mobile close button -->
      <button
        @click="closeMobileMenu"
        class="tw-flex tw-h-8 tw-w-8 tw-items-center tw-justify-center tw-rounded-md hover:tw-bg-gray-100 lg:tw-hidden"
      >
        <i class="pi pi-times"></i>
      </button>
    </div>

    <!-- Menu -->
    <div
      class="tw-flex tw-flex-col tw-gap-2 tw-border-b-[1px] tw-py-3 tw-text-sm tw-text-blue-600"
    >
      <div
        v-for="(menuItem, index) in menuItems"
        :key="index"
        class="tw-flex tw-flex-col tw-justify-center"
        @click="clickMenuItem(menuItem)"
      >
        <!-- Main menu item -->
        <div
          :class="[
            'tw-flex tw-cursor-pointer tw-justify-between tw-rounded-md tw-p-4 tw-transition-colors tw-duration-300 hover:tw-bg-blue-100',
            isActive(menuItem)
              ? 'tw-bg-blue-600 tw-text-white hover:tw-bg-blue-600'
              : '',
          ]"
        >
          <div class="tw-flex tw-items-center tw-gap-2">
            <i
              :class="[
                menuItem.icon,
                'pi tw-text-sm tw-transition-colors tw-duration-300',
                isActive(menuItem)
                  ? 'tw-text-white'
                  : 'tw-text-blue-600',
              ]"
            ></i>

            <span class="tw-font-semibold">
              {{ menuItem.name }}
            </span>
          </div>

          <!-- Arrow -->
          <i
            v-if="
              menuItem.name === 'Raw Files' ||
              menuItem.name === 'Transformed Files'
            "
            :class="[
              'pi tw-text-sm',
              openMenu === menuItem.name
                ? 'pi-angle-down tw-text-white'
                : 'pi-angle-right',
            ]"
          ></i>
        </div>

        <!-- Raw Files -->
        <div
          v-if="
            openMenu === 'Raw Files' &&
            menuItem.name === 'Raw Files'
          "
          v-for="(file, index) in getFilesForMenu(menuItem.name)"
          :key="index"
          :class="[
            'tw-my-1 tw-flex tw-cursor-pointer tw-flex-col tw-rounded-md tw-py-2 hover:tw-bg-blue-100',
            selectedFile === file
              ? 'tw-bg-blue-200'
              : 'tw-bg-blue-50',
          ]"
        >
          <div
            @click.stop="selectFile(file)"
            class="tw-flex tw-items-center tw-gap-2 tw-pl-3"
          >
            <i
              class="pi pi-arrow-right tw-pt-1 tw-text-[10px]"
            ></i>

            <span>{{ file }}</span>
          </div>
        </div>

        <!-- Transformed Files -->
        <div
          v-if="
            openMenu === 'Transformed Files' &&
            menuItem.name === 'Transformed Files'
          "
          v-for="(file, index) in getFilesForMenu(menuItem.name)"
          :key="index"
          :class="[
            'tw-my-1 tw-flex tw-cursor-pointer tw-flex-col tw-rounded-md tw-py-2 hover:tw-bg-blue-100',
            selectedFile === file
              ? 'tw-bg-blue-200'
              : 'tw-bg-blue-50',
          ]"
        >
          <div
            @click.stop="selectFile(file)"
            class="tw-flex tw-items-center tw-gap-2 tw-pl-3"
          >
            <i
              class="pi pi-arrow-right tw-pt-1 tw-text-[10px]"
            ></i>

            <span>{{ file }}</span>
          </div>
        </div>
      </div>
    </div>
  </aside>
</template>