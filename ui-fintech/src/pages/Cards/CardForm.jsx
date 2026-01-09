/**
 * Card Form Component
 * Wrapper for EntityForm with card-specific configuration
 */

import EntityForm from '../../components/shared/EntityForm';
import { cardFormConfig } from '../../config/entities/cards.config';
import { useCreateCard } from '../../hooks/mutations/useCreateCard';
import { generateCardSampleData } from '../../utils/formSampleData';

const CardForm = ({ onSuccess }) => {
  const createMutation = useCreateCard();

  return (
    <EntityForm
      title="Create Card"
      fields={cardFormConfig.fields}
      createMutation={createMutation}
      onSuccess={onSuccess}
      onFillSampleData={generateCardSampleData}
      submitButtonText="Create Card"
      submitButtonLoadingText="Creating..."
    />
  );
};

export default CardForm;
