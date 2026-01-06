/**
 * Payment Form Component
 * Uses generic EntityForm with payment-specific configuration
 */

import { useCreatePayment } from '../../hooks/mutations/useCreatePayment';
import EntityForm from '../../components/shared/EntityForm';
import { paymentFormConfig } from '../../config/entities/payments.config';

const PaymentForm = ({ onSuccess }) => {
  const createPaymentMutation = useCreatePayment();

  return (
    <EntityForm
      title={paymentFormConfig.title}
      fields={paymentFormConfig.fields}
      onSuccess={onSuccess}
      initialValues={paymentFormConfig.initialValues}
      onFillSampleData={paymentFormConfig.onFillSampleData}
      createMutation={createPaymentMutation}
      submitButtonText={paymentFormConfig.submitButtonText}
      submitButtonLoadingText={paymentFormConfig.submitButtonLoadingText}
    />
  );
};

export default PaymentForm;
