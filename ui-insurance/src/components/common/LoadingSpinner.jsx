/**
 * Loading Spinner Component
 * Reusable loading spinner with optional tip text
 */

import { Spin } from 'antd';

const LoadingSpinner = ({ tip = 'Loading...', size = 'large', style = {} }) => {
  return (
    <div
      style={{
        textAlign: 'center',
        padding: '50px 20px',
        ...style,
      }}
    >
      <Spin size={size} tip={tip} />
    </div>
  );
};

export default LoadingSpinner;
