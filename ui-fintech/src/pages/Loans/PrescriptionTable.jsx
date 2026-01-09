/**
 * Loan Table Component
 * Displays loans in a table with mobile responsive view
 */

import EntityTable from '../../components/shared/EntityTable';
import { loanTableConfig, loanMobileFields } from '../../config/entities/loans.config';

const LoanTable = ({ loans = [], loading = false }) => {
  return (
    <EntityTable
      data={loans}
      loading={loading}
      columns={loanTableConfig.columns}
      mobileFields={loanMobileFields}
      entityName="loan"
      basePath="/loans"
      scrollX={loanTableConfig.scroll.x}
    />
  );
};

export default LoanTable;
