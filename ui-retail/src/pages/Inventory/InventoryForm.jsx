/**
 * Inventory Form Component
 * Wrapper for EntityForm with inventory-specific configuration
 */

import EntityForm from '../../components/shared/EntityForm';
import { inventoryFormConfig } from '../../config/entities/inventory.config';
import { useCreateInventory } from '../../hooks/mutations/useCreateInventory';
import { useProducts } from '../../hooks/queries/useProducts';
import { generateInventorySampleData } from '../../utils/formSampleData';

const InventoryForm = ({ onSuccess }) => {
  const createMutation = useCreateInventory();
  const { data: productsData } = useProducts();
  const products = productsData?.items || [];

  // Enhance form config with product options
  const enhancedConfig = {
    ...inventoryFormConfig,
    fields: inventoryFormConfig.fields.map(field => {
      if (field.name === 'productId') {
        return {
          ...field,
          component: {
            ...field.component,
            props: {
              ...field.component.props,
              options: field.getOptions(products),
            },
          },
        };
      }
      return field;
    }),
  };

  return (
    <EntityForm
      title="Create Inventory Item"
      fields={enhancedConfig.fields}
      createMutation={createMutation}
      onSuccess={onSuccess}
      onFillSampleData={generateInventorySampleData}
      submitButtonText="Create Inventory Item"
      submitButtonLoadingText="Creating..."
    />
  );
};

export default InventoryForm;
