/**
 * Product Form Component
 * Uses generic EntityForm with product-specific configuration
 */

import { useCreateProduct } from '../../hooks/mutations/useCreateProduct';
import EntityForm from '../../components/shared/EntityForm';
import { productFormConfig } from '../../config/entities/products.config';

const ProductForm = ({ onSuccess }) => {
  const createProductMutation = useCreateProduct();

  return (
    <EntityForm
      title={productFormConfig.title}
      fields={productFormConfig.fields}
      onSuccess={onSuccess}
      onFillSampleData={productFormConfig.onFillSampleData}
      createMutation={createProductMutation}
      submitButtonText={productFormConfig.submitButtonText}
      submitButtonLoadingText={productFormConfig.submitButtonLoadingText}
    />
  );
};

export default ProductForm;
