/**
 * Provider Form Component
 * Form for creating/editing providers
 */

import EntityForm from '../../components/shared/EntityForm';
import { providerFormFields } from '../../config/entities/providers.config';
import { createProvider } from '../../services/providers';

const ProviderForm = ({ initialData, onSuccess, submitLabel = 'Create Provider' }) => {
  return (
    <EntityForm
      initialData={initialData}
      fields={providerFormFields}
      onSubmit={createProvider}
      onSuccess={onSuccess}
      submitLabel={submitLabel}
    />
  );
};

export default ProviderForm;
