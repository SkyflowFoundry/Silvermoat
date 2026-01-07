/**
 * Payment Table Component
 * Displays payments in a table with mobile responsive view
 */

import EntityTable from '../../components/shared/EntityTable';
import { paymentTableConfig, paymentMobileFields } from '../../config/entities/payments.config';

const PaymentTable = ({ payments = [], loading = false }) => {
  return (
    <EntityTable
      data={payments}
      loading={loading}
      columns={paymentTableConfig.columns}
      mobileFields={paymentMobileFields}
      entityName="payment"
      basePath="/payments"
      scrollX={paymentTableConfig.scroll.x}
    />
  );
};

export default PaymentTable;
