/**
 * Generic Entity Table Component
 * Reusable table component for displaying entity data with sorting, filtering, and actions
 * Supports both desktop table view and mobile card view
 */

import { Table, Button, Space, Card, List, Typography } from 'antd';
import { EyeOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { DEFAULT_PAGE_SIZE } from '../../config/constants';
import { useAppContext } from '../../contexts/AppContext';

const { Text } = Typography;

const EntityTable = ({
  data = [],
  loading = false,
  columns = [],
  mobileFields = [],
  entityName = 'item',
  entityNamePlural = 'items',
  basePath = '',
  scrollX = 800,
}) => {
  const navigate = useNavigate();
  const { isMobile } = useAppContext();

  // Add View action to columns if not already present
  const columnsWithActions = columns.some(col => col.key === 'actions')
    ? columns
    : [
        ...columns,
        {
          title: 'Actions',
          key: 'actions',
          width: 120,
          fixed: 'right',
          render: (_, record) => (
            <Space size="small">
              <Button
                type="default"
                size="small"
                icon={<EyeOutlined />}
                onClick={() => navigate(`${basePath}/${record.id}`)}
              >
                View
              </Button>
            </Space>
          ),
        },
      ];

  // Mobile card view
  if (isMobile) {
    return (
      <List
        loading={loading}
        dataSource={data}
        pagination={{
          pageSize: DEFAULT_PAGE_SIZE,
          showSizeChanger: false,
          size: 'small',
        }}
        renderItem={(item) => (
          <Card
            size="small"
            style={{ marginBottom: 12 }}
            onClick={() => navigate(`${basePath}/${item.id}`)}
            hoverable
          >
            <Space direction="vertical" size="small" style={{ width: '100%' }}>
              {mobileFields.map((field, index) => (
                <div
                  key={index}
                  style={
                    field.layout === 'row'
                      ? { display: 'flex', justifyContent: 'space-between', gap: 16 }
                      : {}
                  }
                >
                  {field.layout === 'row' ? (
                    field.items.map((subField, subIndex) => (
                      <div key={subIndex} style={{ flex: subField.flex || 1 }}>
                        <Text type="secondary" style={{ fontSize: 12 }}>
                          {subField.label}
                        </Text>
                        <div>
                          {subField.render
                            ? subField.render(item)
                            : <Text style={{ fontSize: 14 }}>{subField.getValue(item)}</Text>
                          }
                        </div>
                      </div>
                    ))
                  ) : (
                    <>
                      <Text type="secondary" style={{ fontSize: 12 }}>
                        {field.label}
                      </Text>
                      <div>
                        {field.render
                          ? field.render(item)
                          : <Text style={{ fontSize: 14 }}>{field.getValue(item)}</Text>
                        }
                      </div>
                    </>
                  )}
                </div>
              ))}
              <Button
                type="primary"
                size="small"
                icon={<EyeOutlined />}
                onClick={(e) => {
                  e.stopPropagation();
                  navigate(`${basePath}/${item.id}`);
                }}
                block
              >
                View Details
              </Button>
            </Space>
          </Card>
        )}
      />
    );
  }

  // Desktop table view
  return (
    <Table
      columns={columnsWithActions}
      dataSource={data}
      loading={loading}
      rowKey="id"
      pagination={{
        pageSize: DEFAULT_PAGE_SIZE,
        showSizeChanger: true,
        showTotal: (total, range) =>
          `${range[0]}-${range[1]} of ${total} ${entityNamePlural}`,
        pageSizeOptions: ['10', '20', '50', '100'],
      }}
      scroll={{ x: scrollX }}
      size="middle"
      bordered
    />
  );
};

export default EntityTable;
