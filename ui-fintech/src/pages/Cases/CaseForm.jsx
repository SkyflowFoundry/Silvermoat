/**
 * Case Form Component
 * Wrapper for EntityForm with case-specific configuration
 */

import EntityForm from '../../components/shared/EntityForm';
import { caseFormConfig } from '../../config/entities/cases.config';
import { useCreateCase } from '../../hooks/mutations/useCreateCase';
import { generateCaseSampleData } from '../../utils/formSampleData';

const CaseForm = ({ onSuccess }) => {
  const createMutation = useCreateCase();

  return (
    <EntityForm
      title="Create Case"
      fields={caseFormConfig.fields}
      createMutation={createMutation}
      onSuccess={onSuccess}
      onFillSampleData={generateCaseSampleData}
      submitButtonText="Create Case"
      submitButtonLoadingText="Creating..."
    />
  );
};

export default CaseForm;
