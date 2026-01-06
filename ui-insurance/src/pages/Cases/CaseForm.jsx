/**
 * Case Form Component
 * Uses generic EntityForm with case-specific configuration
 */

import { useCreateCase } from '../../hooks/mutations/useCreateCase';
import EntityForm from '../../components/shared/EntityForm';
import { caseFormConfig } from '../../config/entities/cases.config';

const CaseForm = ({ onSuccess }) => {
  const createCaseMutation = useCreateCase();

  return (
    <EntityForm
      title={caseFormConfig.title}
      fields={caseFormConfig.fields}
      onSuccess={onSuccess}
      initialValues={caseFormConfig.initialValues}
      onFillSampleData={caseFormConfig.onFillSampleData}
      createMutation={createCaseMutation}
      submitButtonText={caseFormConfig.submitButtonText}
      submitButtonLoadingText={caseFormConfig.submitButtonLoadingText}
    />
  );
};

export default CaseForm;
