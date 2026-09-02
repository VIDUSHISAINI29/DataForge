<script setup lang="ts">
   import { useRoute, useRouter } from 'vue-router';
   import axios, { all } from 'axios';
   import { ref, onMounted, computed, watchEffect, watch } from 'vue';
   import { useFileStore } from '@/shared/store/fileStore';

   const fileStore = useFileStore();

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

   const VITE_BACKEND_URL = import.meta.env.VITE_API_URL;

   const selectedFile = ref<string | null>(null);
   const showFiles = ref(false);

   const route = useRoute();
   const router = useRouter();

   const isActive = (item: (typeof menuItems)[number]) => {
      return item.routes.some((path) => route.path.startsWith(path));
   };

   const selectFile = async (fileName: string) => {
      selectedFile.value = fileName;
      fileStore.currentFileName = fileName;

      await getSelectedFilePreview();
   };

   const getSelectedFilePreview = async () => {
      try {
         let response = null;

         if (route.path === '/raw-files') {
            response = await axios.get(
               `${VITE_BACKEND_URL}/reads/raw-file-preview/${selectedFile.value}`,
            );
         } else {
            response = await axios.get(
               `${VITE_BACKEND_URL}/reads/transformed-file-preview/${selectedFile.value}`,
            );
         }

         fileStore.currentFile = response?.data;

         fileStore.currentFileName = selectedFile.value;
      } catch (error: any) {
         if (error.response) {
            console.error('Server Error Data:', error.response.data);
            console.error('Server Status:', error.response.status);

            console.log(
               'error -',
               error.response ||
                  'Something went wrong while reading preview of the file.',
            );
         } else {
            console.error('Preview Read failed:', error.message);
         }
      }
   };

   const openMenu = ref<string | null>(null);

   // ⭐ Menu click handling
   const clickMenuItem = (menuItem: any) => {
      const hasSubMenu =
         menuItem.name === 'Raw Files' ||
         menuItem.name === 'Transformed Files';

      // Raw Files / Transformed Files
      if (hasSubMenu) {
         openMenu.value =
            openMenu.value === menuItem.name
               ? null
               : menuItem.name;

         // Navigate to the corresponding route
         if (route.path !== menuItem.routes[0]) {
            router.push(menuItem.routes[0]);
         }

         return;
      }

      // Upload File
      openMenu.value = null;
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
   <div class="tw-flex tw-w-full tw-max-w-64 tw-flex-col tw-p-2">

      <div class="tw-flex tw-items-center tw-justify-center tw-border-b-[1px]">
         <!-- <img class="tw-w-40 tw-p-1" src="/images/logo.png" alt=""> -->

         <span class="tw-pb-2 tw-text-2xl tw-font-bold tw-text-blue-600">
            Data-Forge
         </span>
      </div>

      <div
         class="tw-flex tw-flex-col tw-gap-2 tw-border-b-[1px] tw-py-3 tw-text-sm tw-text-blue-600">

         <div
            v-for="(menuItem, index) in menuItems"
            :key="index"
            class="tw-flex tw-flex-col tw-justify-center"
            @click="clickMenuItem(menuItem)"
         >

            <!-- Main menu item -->
            <div
               :class="[
                  'tw-flex tw-cursor-pointer tw-justify-between tw-rounded-md tw-px-4 tw-py-2 tw-transition-colors tw-duration-300 hover:tw-bg-blue-100',
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

               <div>

                  <i
                     v-if="
                        menuItem.name === 'Raw Files' ||
                        menuItem.name === 'Transformed Files'
                     "
                     :class="[
                        'pi tw-text-sm  tw-transition-colors tw-duration-300',

                        openMenu === menuItem.name
                           ? 'pi-angle-down tw-text-white'
                           : 'pi-angle-right',
                     ]"
                  ></i>

               </div>

            </div>


            <!-- Raw Files -->
            <div
               v-if="
                  fileStore.rawFilesList &&
                  openMenu === 'Raw Files' &&
                  menuItem.name === 'Raw Files'
               "
               v-for="(file, index) in getFilesForMenu(menuItem.name)"
               :key="index"
               :class="[
                  'flex tw-my-1 tw-cursor-pointer tw-flex-col tw-rounded-md tw-py-2 tw-transition-colors tw-duration-300 hover:tw-bg-blue-100',
                  selectedFile == file
                     ? 'tw-bg-blue-200'
                     : 'tw-bg-blue-50',
               ]"
            >

               <div
                  @click.stop="selectFile(file)"
                  class="tw-flex tw-items-center tw-gap-2 tw-pl-3"
               >

                  <i
                     class="pi pi-arrow-right tw-pt-1 tw-text-[10px] tw-font-light"
                  ></i>

                  <span>
                     {{ file }}
                  </span>

               </div>

            </div>


            <!-- Transformed Files -->
            <div
               v-if="
                  fileStore.transformedFilesList &&
                  openMenu === 'Transformed Files' &&
                  menuItem.name === 'Transformed Files'
               "
               v-for="(file, index) in getFilesForMenu(menuItem.name)"
               :key="index"
               :class="[
                  'flex tw-my-1 tw-cursor-pointer tw-flex-col tw-rounded-md tw-py-2 tw-transition-colors tw-duration-300 hover:tw-bg-blue-100',
                  selectedFile == file
                     ? 'tw-bg-blue-200'
                     : 'tw-bg-blue-50',
               ]"
            >

               <div
                  @click.stop="selectFile(file)"
                  class="tw-flex tw-items-center tw-gap-2 tw-pl-3"
               >

                  <i
                     class="pi pi-arrow-right tw-pt-1 tw-text-[10px] tw-font-light"
                  ></i>

                  <span>
                     {{ file }}
                  </span>

               </div>

            </div>

         </div>

      </div>

   </div>
</template>