/**
 * Case Table Component
 * Uses generic EntityTable with case-specific configuration
 */

import { useNavigate } from 'react-router-dom';
import EntityTable from '../../components/shared/EntityTable';
import { caseTableConfig } from '../../config/entities/cases.config';

const CaseTable = ({ cases = [], loading = false }) => {
  const navigate = useNavigate();

  return (
    <EntityTable
      data={cases}
      loading={loading}
      columns={caseTableConfig.columns(navigate)}
      mobileFields={caseTableConfig.mobileFields}
      entityName={caseTableConfig.entityName}
      entityNamePlural={caseTableConfig.entityNamePlural}
      basePath={caseTableConfig.basePath}
      scrollX={caseTableConfig.scrollX}
    />
  );
};

export default CaseTable;
