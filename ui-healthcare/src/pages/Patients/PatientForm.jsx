/**
 * Patient Form Component
 * Form for creating/editing patients
 */

import EntityForm from '../../components/shared/EntityForm';
import { patientFormFields } from '../../config/entities/patients.config';
import { createPatient } from '../../services/patients';

const PatientForm = ({ initialData, onSuccess, submitLabel = 'Create Patient' }) => {
  return (
    <EntityForm
      initialData={initialData}
      fields={patientFormFields}
      onSubmit={createPatient}
      onSuccess={onSuccess}
      submitLabel={submitLabel}
    />
  );
};

export default PatientForm;
