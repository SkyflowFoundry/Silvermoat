/**
 * Order Form Component
 * Wrapper for EntityForm with order-specific configuration
 */

import EntityForm from '../../components/shared/EntityForm';
import { orderFormConfig } from '../../config/entities/orders.config';
import { useCreateOrder } from '../../hooks/mutations/useCreateOrder';
import { generateOrderSampleData } from '../../utils/formSampleData';

const OrderForm = ({ onSuccess }) => {
  const createMutation = useCreateOrder();

  // Pre-process sample data to convert items to JSON string
  const handleFillSampleData = () => {
    const sampleData = generateOrderSampleData();
    return {
      ...sampleData,
      items: JSON.stringify(sampleData.items || [], null, 2),
    };
  };

  return (
    <EntityForm
      title="Create Order"
      fields={orderFormConfig.fields}
      createMutation={createMutation}
      onSuccess={onSuccess}
      onFillSampleData={handleFillSampleData}
      submitButtonText="Create Order"
      submitButtonLoadingText="Creating..."
    />
  );
};

export default OrderForm;
