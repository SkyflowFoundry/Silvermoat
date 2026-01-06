/**
 * Empty State Component
 * Displays friendly empty state when no data is available
 */

import { Empty, Button } from 'antd';
import { PlusOutlined } from '@ant-design/icons';

const EmptyState = ({
  description = 'No data available',
  actionLabel,
  onAction,
  icon,
  style = {},
}) => {
  return (
    <div
      style={{
        textAlign: 'center',
        padding: '50px 20px',
        ...style,
      }}
    >
      <Empty
        image={Empty.PRESENTED_IMAGE_SIMPLE}
        imageStyle={{
          height: 60,
        }}
        description={<span style={{ color: '#8c8c8c' }}>{description}</span>}
      >
        {actionLabel && onAction && (
          <Button
            type="primary"
            icon={icon || <PlusOutlined />}
            onClick={onAction}
          >
            {actionLabel}
          </Button>
        )}
      </Empty>
    </div>
  );
};

export default EmptyState;
