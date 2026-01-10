/**
 * Transaction Table Component
 * Displays transactions in a table with mobile responsive view
 */

import EntityTable from '../../components/shared/EntityTable';
import { transactionTableConfig } from '../../config/entities/transactions.config';

const TransactionTable = ({ transactions = [], loading = false }) => {
  return (
    <EntityTable
      data={transactions}
      loading={loading}
      columns={transactionTableConfig.columns}
      mobileFields={transactionTableConfig.mobileFields}
      entityName="transaction"
      basePath="/transactions"
    />
  );
};

export default TransactionTable;
