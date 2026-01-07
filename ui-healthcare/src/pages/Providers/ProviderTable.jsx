/**
 * Provider Table Component
 * Displays providers in a table with mobile responsive view
 */

import EntityTable from '../../components/shared/EntityTable';
import { providerTableConfig, providerMobileFields } from '../../config/entities/providers.config';

const ProviderTable = ({ providers = [], loading = false }) => {
  return (
    <EntityTable
      data={providers}
      loading={loading}
      columns={providerTableConfig.columns}
      mobileFields={providerMobileFields}
      entityName="provider"
      basePath="/providers"
      scrollX={providerTableConfig.scroll.x}
    />
  );
};

export default ProviderTable;
