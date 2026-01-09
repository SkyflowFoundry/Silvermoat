/**
 * Account Form Component
 * Form for creating/editing accounts
 */

import EntityForm from '../../components/shared/EntityForm';
import { accountFormFields } from '../../config/entities/accounts.config';
import { createAccount } from '../../services/accounts';

const AccountForm = ({ initialData, onSuccess, submitLabel = 'Create Account' }) => {
  return (
    <EntityForm
      initialData={initialData}
      fields={accountFormFields}
      onSubmit={createAccount}
      onSuccess={onSuccess}
      submitLabel={submitLabel}
    />
  );
};

export default AccountForm;
