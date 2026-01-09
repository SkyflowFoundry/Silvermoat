/**
 * Transaction Form Component
 * Form for creating/editing transactions
 */

import EntityForm from '../../components/shared/EntityForm';
import { transactionFormFields } from '../../config/entities/transactions.config';
import { createTransaction } from '../../services/transactions';

const TransactionForm = ({ initialData, onSuccess, submitLabel = 'Create Transaction' }) => {
  return (
    <EntityForm
      initialData={initialData}
      fields={transactionFormFields}
      onSubmit={createTransaction}
      onSuccess={onSuccess}
      submitLabel={submitLabel}
    />
  );
};

export default TransactionForm;
