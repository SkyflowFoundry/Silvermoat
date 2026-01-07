/**
 * Patient Table Component
 * Displays patients in a table with mobile responsive view
 */

import EntityTable from '../../components/shared/EntityTable';
import { patientTableConfig, patientMobileFields } from '../../config/entities/patients.config';

const PatientTable = ({ patients = [], loading = false }) => {
  return (
    <EntityTable
      data={patients}
      loading={loading}
      columns={patientTableConfig.columns}
      mobileFields={patientMobileFields}
      entityName="patient"
      basePath="/patients"
      scrollX={patientTableConfig.scroll.x}
    />
  );
};

export default PatientTable;
