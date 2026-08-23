import { apiGet, apiPost } from '@/plugins/api';

interface fileList {
    files: string[];
}

interface queryFilePayload {
   file_name: string | null;
   query: string;
}

export interface QueryFileResponse {
   message: string;
   result: {
      columns: string[];
      data: Record<string, any>[];
   };
}

export interface TransformQueryFileResponse {
   message: string | null;
}

interface FilePreview {
  columns: string[]
  data: Record<string, unknown>[]
}

export const getSelectedRawFilePreview = async (file_name:string|null) => {
   return apiGet<FilePreview>(`/reads/raw-file-preview/${file_name}`);
};

export const getRawFilesList = async () => {
   return apiGet<fileList>('/reads/read-raw-files-list');
};


export const queryFile = async (payload: queryFilePayload,): Promise<QueryFileResponse> => {
   return apiPost<QueryFileResponse>('/query/query-raw-file', payload);
};

export const TransformFile = async (payload: queryFilePayload) => {
   return apiPost<TransformQueryFileResponse>('/query/transform-file', payload);
};
