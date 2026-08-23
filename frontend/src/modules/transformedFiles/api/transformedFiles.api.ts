import { apiGet, apiPost } from "@/plugins/api";

export interface QueryFileResponse {
   message: string;
   result: {
      columns: string[];
      data: Record<string, any>[];
   };
}

interface queryFilePayload {
    file_name: string|null,
    query: string
}

interface fileList {
    files: string[];
}

export const getTransformedFilesList = async() => {
    return apiGet<fileList>('/reads/read-transformed-files-list');
}

export const queryTransformedFile = async(payload: queryFilePayload) => {
    return apiPost<QueryFileResponse>('/query/query-transformed-file', payload);
}