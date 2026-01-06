/**
 * Claim Table Component
 * Uses generic EntityTable with claim-specific configuration
 */

import { useNavigate } from 'react-router-dom';
import EntityTable from '../../components/shared/EntityTable';
import { claimTableConfig } from '../../config/entities/claims.config';

const ClaimTable = ({ claims = [], loading = false }) => {
  const navigate = useNavigate();

  return (
    <EntityTable
      data={claims}
      loading={loading}
      columns={claimTableConfig.columns(navigate)}
      mobileFields={claimTableConfig.mobileFields}
      entityName={claimTableConfig.entityName}
      entityNamePlural={claimTableConfig.entityNamePlural}
      basePath={claimTableConfig.basePath}
      scrollX={claimTableConfig.scrollX}
    />
  );
};

export default ClaimTable;
