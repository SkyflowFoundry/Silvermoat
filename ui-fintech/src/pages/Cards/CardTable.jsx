/**
 * Card Table Component
 * Displays cards in a table with mobile responsive view
 */

import EntityTable from '../../components/shared/EntityTable';
import { cardTableConfig, cardMobileFields } from '../../config/entities/cards.config';

const CardTable = ({ cards = [], loading = false }) => {
  return (
    <EntityTable
      data={cards}
      loading={loading}
      columns={cardTableConfig.columns}
      mobileFields={cardMobileFields}
      entityName="card"
      basePath="/cards"
      scrollX={cardTableConfig.scroll.x}
    />
  );
};

export default CardTable;
