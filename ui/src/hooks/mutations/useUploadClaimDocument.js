/**
 * React Query mutation hook for uploading claim document
 */

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { message } from 'antd';
import { uploadDocument } from '../../services/claims';

export const useUploadClaimDocument = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, text }) => uploadDocument(id, text),
    onSuccess: (response, variables) => {
      // Invalidate specific claim
      queryClient.invalidateQueries({ queryKey: ['claims', variables.id] });
      message.success('Document uploaded successfully');
    },
    onError: (error) => {
      message.error(`Failed to upload document: ${error.message}`);
    },
  });
};

export default useUploadClaimDocument;
