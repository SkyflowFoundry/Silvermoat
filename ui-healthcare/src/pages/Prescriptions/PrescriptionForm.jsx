/**
 * Prescription Form Component
 * Form for creating/editing prescriptions
 */

import EntityForm from '../../components/shared/EntityForm';
import { prescriptionFormFields } from '../../config/entities/prescriptions.config';
import { createPrescription } from '../../services/prescriptions';

const PrescriptionForm = ({ initialData, onSuccess, submitLabel = 'Create Prescription' }) => {
  return (
    <EntityForm
      initialData={initialData}
      fields={prescriptionFormFields}
      onSubmit={createPrescription}
      onSuccess={onSuccess}
      submitLabel={submitLabel}
    />
  );
};

export default PrescriptionForm;
