/**
 * Customer Form Component
 * Form for creating/editing customers
 */

import EntityForm from '../../components/shared/EntityForm';
import { customerFormFields } from '../../config/entities/customers.config';
import { createCustomer } from '../../services/customers';

const CustomerForm = ({ initialData, onSuccess, submitLabel = 'Create Customer' }) => {
  return (
    <EntityForm
      initialData={initialData}
      fields={customerFormFields}
      onSubmit={createCustomer}
      onSuccess={onSuccess}
      submitLabel={submitLabel}
    />
  );
};

export default CustomerForm;
