/**
 * Product Table Component
 * Uses generic EntityTable with product-specific configuration
 */

import { useNavigate } from 'react-router-dom';
import EntityTable from '../../components/shared/EntityTable';
import { productTableConfig } from '../../config/entities/products.config';

const ProductTable = ({ products = [], loading = false }) => {
  const navigate = useNavigate();

  return (
    <EntityTable
      data={products}
      loading={loading}
      columns={productTableConfig.columns(navigate)}
      mobileFields={productTableConfig.mobileFields}
      entityName={productTableConfig.entityName}
      entityNamePlural={productTableConfig.entityNamePlural}
      basePath={productTableConfig.basePath}
      scrollX={productTableConfig.scrollX}
    />
  );
};

export default ProductTable;
