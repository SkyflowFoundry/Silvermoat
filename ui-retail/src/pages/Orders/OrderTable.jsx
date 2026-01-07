/**
 * Order Table Component
 * Displays orders in a table with mobile responsive view
 */

import EntityTable from '../../components/shared/EntityTable';
import { orderTableConfig, orderMobileFields } from '../../config/entities/orders.config';

const OrderTable = ({ orders = [], loading = false }) => {
  return (
    <EntityTable
      data={orders}
      loading={loading}
      columns={orderTableConfig.columns}
      mobileFields={orderMobileFields}
      entityName="order"
      basePath="/orders"
      scrollX={orderTableConfig.scroll.x}
    />
  );
};

export default OrderTable;
