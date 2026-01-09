/**
 * Customer Table Component
 * Displays customers in a table with mobile responsive view
 */

import EntityTable from '../../components/shared/EntityTable';
import { customerTableConfig, customerMobileFields } from '../../config/entities/customers.config';

const CustomerTable = ({ customers = [], loading = false }) => {
  return (
    <EntityTable
      data={customers}
      loading={loading}
      columns={customerTableConfig.columns}
      mobileFields={customerMobileFields}
      entityName="customer"
      basePath="/customers"
      scrollX={customerTableConfig.scroll.x}
    />
  );
};

export default CustomerTable;
