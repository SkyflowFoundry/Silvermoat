/**
 * Quote Form Component
 * Uses generic EntityForm with quote-specific configuration
 */

import { useCreateQuote } from '../../hooks/mutations/useCreateQuote';
import EntityForm from '../../components/shared/EntityForm';
import { quoteFormConfig } from '../../config/entities/quotes.config';

const QuoteForm = ({ onSuccess }) => {
  const createQuoteMutation = useCreateQuote();

  return (
    <EntityForm
      title={quoteFormConfig.title}
      fields={quoteFormConfig.fields}
      onSuccess={onSuccess}
      onFillSampleData={quoteFormConfig.onFillSampleData}
      createMutation={createQuoteMutation}
      submitButtonText={quoteFormConfig.submitButtonText}
      submitButtonLoadingText={quoteFormConfig.submitButtonLoadingText}
    />
  );
};

export default QuoteForm;
