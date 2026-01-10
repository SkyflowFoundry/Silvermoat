/**
 * Customer Table Component
 * Displays customers in a table with mobile responsive view
 */

import EntityTable from '../../components/shared/EntityTable';
import { customerTableConfig } from '../../config/entities/customers.config';

const CustomerTable = ({ customers = [], loading = false }) => {
  return (
    <EntityTable
      data={customers}
      loading={loading}
      columns={customerTableConfig.columns}
      mobileFields={customerTableConfig.mobileFields}
      entityName="customer"
      basePath="/customers"
      scrollX={customerTableConfig.scroll?.x}
    />
  );
};

export default CustomerTable;
