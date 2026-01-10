/**
 * Case Table Component
 * Displays cases in a table with mobile responsive view
 */

import EntityTable from '../../components/shared/EntityTable';
import { caseTableConfig } from '../../config/entities/cases.config';

const CaseTable = ({ cases = [], loading = false }) => {
  return (
    <EntityTable
      data={cases}
      loading={loading}
      columns={caseTableConfig.columns}
      mobileFields={caseTableConfig.mobileFields}
      entityName="case"
      basePath="/cases"
      scrollX={caseTableConfig.scroll?.x}
    />
  );
};

export default CaseTable;
