/**
 * Policy Table Component
 * Uses generic EntityTable with policy-specific configuration
 */

import { useNavigate } from 'react-router-dom';
import EntityTable from '../../components/shared/EntityTable';
import { policyTableConfig } from '../../config/entities/policies.config';

const PolicyTable = ({ policies = [], loading = false }) => {
  const navigate = useNavigate();

  return (
    <EntityTable
      data={policies}
      loading={loading}
      columns={policyTableConfig.columns(navigate)}
      mobileFields={policyTableConfig.mobileFields}
      entityName={policyTableConfig.entityName}
      entityNamePlural={policyTableConfig.entityNamePlural}
      basePath={policyTableConfig.basePath}
      scrollX={policyTableConfig.scrollX}
    />
  );
};

export default PolicyTable;
