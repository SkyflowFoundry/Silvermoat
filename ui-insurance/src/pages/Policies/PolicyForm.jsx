/**
 * Policy Form Component
 * Uses generic EntityForm with policy-specific configuration
 */

import { useCreatePolicy } from '../../hooks/mutations/useCreatePolicy';
import EntityForm from '../../components/shared/EntityForm';
import { policyFormConfig } from '../../config/entities/policies.config';

const PolicyForm = ({ onSuccess }) => {
  const createPolicyMutation = useCreatePolicy();

  return (
    <EntityForm
      title={policyFormConfig.title}
      fields={policyFormConfig.fields}
      onSuccess={onSuccess}
      initialValues={policyFormConfig.initialValues}
      onFillSampleData={policyFormConfig.onFillSampleData}
      createMutation={createPolicyMutation}
      submitButtonText={policyFormConfig.submitButtonText}
      submitButtonLoadingText={policyFormConfig.submitButtonLoadingText}
    />
  );
};

export default PolicyForm;
