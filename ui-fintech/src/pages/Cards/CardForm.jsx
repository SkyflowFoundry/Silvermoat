/**
 * Card Form Component
 * Wrapper for EntityForm with card-specific configuration
 */

import EntityForm from '../../components/shared/EntityForm';
import { cardFormConfig } from '../../config/entities/cards.config';
import { useCreateCard } from '../../hooks/mutations/useCreateCard';
import { useOrders } from '../../hooks/queries/useOrders';
import { generateCardSampleData } from '../../utils/formSampleData';

const CardForm = ({ onSuccess }) => {
  const createMutation = useCreateCard();
  const { data: ordersData } = useOrders();
  const orders = ordersData?.items || [];

  // Enhance form config with order options
  const enhancedConfig = {
    ...cardFormConfig,
    fields: cardFormConfig.fields.map(field => {
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
      title="Create Card"
      fields={enhancedConfig.fields}
      createMutation={createMutation}
      onSuccess={onSuccess}
      onFillSampleData={generateCardSampleData}
      submitButtonText="Create Card"
      submitButtonLoadingText="Creating..."
    />
  );
};

export default CardForm;
