/**
 * Loan Form Component
 * Form for creating/editing loans
 */

import EntityForm from '../../components/shared/EntityForm';
import { loanFormFields } from '../../config/entities/loans.config';
import { createLoan } from '../../services/loans';

const LoanForm = ({ initialData, onSuccess, submitLabel = 'Create Loan' }) => {
  return (
    <EntityForm
      initialData={initialData}
      fields={loanFormFields}
      onSubmit={createLoan}
      onSuccess={onSuccess}
      submitLabel={submitLabel}
    />
  );
};

export default LoanForm;
