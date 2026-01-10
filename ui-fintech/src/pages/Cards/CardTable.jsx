/**
 * Card Table Component
 * Displays cards in a table with mobile responsive view
 */

import EntityTable from '../../components/shared/EntityTable';
import { cardTableConfig } from '../../config/entities/cards.config';

const CardTable = ({ cards = [], loading = false }) => {
  return (
    <EntityTable
      data={cards}
      loading={loading}
      columns={cardTableConfig.columns}
      mobileFields={cardTableConfig.mobileFields}
      entityName="card"
      basePath="/cards"
    />
  );
};

export default CardTable;
