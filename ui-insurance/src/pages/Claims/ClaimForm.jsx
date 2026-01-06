/**
 * Claim Form Component
 * Uses generic EntityForm with claim-specific configuration
 */

import { useCreateClaim } from '../../hooks/mutations/useCreateClaim';
import EntityForm from '../../components/shared/EntityForm';
import { claimFormConfig } from '../../config/entities/claims.config';

const ClaimForm = ({ onSuccess }) => {
  const createClaimMutation = useCreateClaim();

  return (
    <EntityForm
      title={claimFormConfig.title}
      fields={claimFormConfig.fields}
      onSuccess={onSuccess}
      initialValues={claimFormConfig.initialValues}
      onFillSampleData={claimFormConfig.onFillSampleData}
      createMutation={createClaimMutation}
      submitButtonText={claimFormConfig.submitButtonText}
      submitButtonLoadingText={claimFormConfig.submitButtonLoadingText}
    />
  );
};

export default ClaimForm;
