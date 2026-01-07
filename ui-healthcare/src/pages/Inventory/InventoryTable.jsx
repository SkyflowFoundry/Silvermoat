/**
 * Inventory Table Component
 * Displays inventory items in a table with mobile responsive view
 */

import EntityTable from '../../components/shared/EntityTable';
import { inventoryTableConfig, inventoryMobileFields } from '../../config/entities/inventory.config';

const InventoryTable = ({ inventory = [], loading = false }) => {
  return (
    <EntityTable
      data={inventory}
      loading={loading}
      columns={inventoryTableConfig.columns}
      mobileFields={inventoryMobileFields}
      entityName="inventory item"
      basePath="/inventory"
      scrollX={inventoryTableConfig.scroll.x}
    />
  );
};

export default InventoryTable;
