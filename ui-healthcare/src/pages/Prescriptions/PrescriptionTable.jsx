/**
 * Prescription Table Component
 * Displays prescriptions in a table with mobile responsive view
 */

import EntityTable from '../../components/shared/EntityTable';
import { prescriptionTableConfig, prescriptionMobileFields } from '../../config/entities/prescriptions.config';

const PrescriptionTable = ({ prescriptions = [], loading = false }) => {
  return (
    <EntityTable
      data={prescriptions}
      loading={loading}
      columns={prescriptionTableConfig.columns}
      mobileFields={prescriptionMobileFields}
      entityName="prescription"
      basePath="/prescriptions"
      scrollX={prescriptionTableConfig.scroll.x}
    />
  );
};

export default PrescriptionTable;
