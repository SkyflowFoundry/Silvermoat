/**
 * Appointment Form Component
 * Form for creating/editing appointments
 */

import EntityForm from '../../components/shared/EntityForm';
import { appointmentFormFields } from '../../config/entities/appointments.config';
import { createAppointment } from '../../services/appointments';

const AppointmentForm = ({ initialData, onSuccess, submitLabel = 'Create Appointment' }) => {
  return (
    <EntityForm
      initialData={initialData}
      fields={appointmentFormFields}
      onSubmit={createAppointment}
      onSuccess={onSuccess}
      submitLabel={submitLabel}
    />
  );
};

export default AppointmentForm;
