/**
 * Account Table Component
 * Displays accounts in a table with mobile responsive view
 */

import EntityTable from '../../components/shared/EntityTable';
import { accountTableConfig } from '../../config/entities/accounts.config';

const AccountTable = ({ accounts = [], loading = false }) => {
  return (
    <EntityTable
      data={accounts}
      loading={loading}
      columns={accountTableConfig.columns}
      mobileFields={accountTableConfig.mobileFields}
      entityName="account"
      basePath="/accounts"
      scrollX={accountTableConfig.scroll?.x}
    />
  );
};

export default AccountTable;
