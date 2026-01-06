/**
 * Quote Table Component
 * Uses generic EntityTable with quote-specific configuration
 */

import { useNavigate } from 'react-router-dom';
import EntityTable from '../../components/shared/EntityTable';
import { quoteTableConfig } from '../../config/entities/quotes.config';

const QuoteTable = ({ quotes = [], loading = false }) => {
  const navigate = useNavigate();

  return (
    <EntityTable
      data={quotes}
      loading={loading}
      columns={quoteTableConfig.columns(navigate)}
      mobileFields={quoteTableConfig.mobileFields}
      entityName={quoteTableConfig.entityName}
      entityNamePlural={quoteTableConfig.entityNamePlural}
      basePath={quoteTableConfig.basePath}
      scrollX={quoteTableConfig.scrollX}
    />
  );
};

export default QuoteTable;
