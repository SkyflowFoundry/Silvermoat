/**
 * Payment Form Component
 * Wrapper for EntityForm with payment-specific configuration
 */

import EntityForm from '../../components/shared/EntityForm';
import { paymentFormConfig } from '../../config/entities/payments.config';
import { useCreatePayment } from '../../hooks/mutations/useCreatePayment';
import { useOrders } from '../../hooks/queries/useOrders';
import { generatePaymentSampleData } from '../../utils/formSampleData';

const PaymentForm = ({ onSuccess }) => {
  const createMutation = useCreatePayment();
  const { data: ordersData } = useOrders();
  const orders = ordersData?.items || [];

  // Enhance form config with order options
  const enhancedConfig = {
    ...paymentFormConfig,
    fields: paymentFormConfig.fields.map(field => {
      if (field.name === 'orderId') {
        return {
          ...field,
          component: {
            ...field.component,
            props: {
              ...field.component.props,
              options: field.getOptions(orders),
            },
          },
        };
      }
      return field;
    }),
  };

  return (
    <EntityForm
      title="Create Payment"
      fields={enhancedConfig.fields}
      createMutation={createMutation}
      onSuccess={onSuccess}
      onFillSampleData={generatePaymentSampleData}
      submitButtonText="Create Payment"
      submitButtonLoadingText="Creating..."
    />
  );
};

export default PaymentForm;
