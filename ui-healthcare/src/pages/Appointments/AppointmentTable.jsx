/**
 * Appointment Table Component
 * Displays appointments in a table with mobile responsive view
 */

import EntityTable from '../../components/shared/EntityTable';
import { appointmentTableConfig, appointmentMobileFields } from '../../config/entities/appointments.config';

const AppointmentTable = ({ appointments = [], loading = false }) => {
  return (
    <EntityTable
      data={appointments}
      loading={loading}
      columns={appointmentTableConfig.columns}
      mobileFields={appointmentMobileFields}
      entityName="appointment"
      basePath="/appointments"
      scrollX={appointmentTableConfig.scroll.x}
    />
  );
};

export default AppointmentTable;
