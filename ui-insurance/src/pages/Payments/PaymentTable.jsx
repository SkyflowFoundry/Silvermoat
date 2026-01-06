/**
 * Payment Table Component
 * Uses generic EntityTable with payment-specific configuration
 */

import { useNavigate } from 'react-router-dom';
import EntityTable from '../../components/shared/EntityTable';
import { paymentTableConfig } from '../../config/entities/payments.config';

const PaymentTable = ({ payments = [], loading = false }) => {
  const navigate = useNavigate();

  return (
    <EntityTable
      data={payments}
      loading={loading}
      columns={paymentTableConfig.columns(navigate)}
      mobileFields={paymentTableConfig.mobileFields}
      entityName={paymentTableConfig.entityName}
      entityNamePlural={paymentTableConfig.entityNamePlural}
      basePath={paymentTableConfig.basePath}
      scrollX={paymentTableConfig.scrollX}
    />
  );
};

export default PaymentTable;
