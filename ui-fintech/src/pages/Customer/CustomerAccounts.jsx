/**
 * Customer Accounts Page
 * Patient view of their accounts
 */

import { useState, useEffect } from 'react';
import { Card, Table, Tag, Typography, Button, Space, Spin, Alert } from 'antd';
import { useNavigate } from 'react-router-dom';
import { ArrowLeftOutlined, CalendarOutlined } from '@ant-design/icons';
import { useAccounts } from '../../hooks/queries/useAccounts';
import { formatTimestamp } from '../../utils/formatters';

const { Title, Paragraph } = Typography;

const STATUS_COLORS = {
  SCHEDULED: 'blue',
  CONFIRMED: 'cyan',
  COMPLETED: 'green',
  CANCELLED: 'red',
  NO_SHOW: 'orange',
};

const CustomerAccounts = () => {
  const navigate = useNavigate();
  const { data, isLoading, error } = useAccounts();
  const accounts = data?.items || [];

  // In a real app, filter by logged-in patient email
  // For now, show all accounts
  const myAccounts = accounts;

  const columns = [
    {
      title: 'Date & Time',
      dataIndex: ['data', 'date'],
      key: 'date',
      render: (date) => date || '-',
    },
    {
      title: 'Provider',
      dataIndex: ['data', 'provider'],
      key: 'provider',
      render: (provider) => provider || '-',
    },
    {
      title: 'Type',
      dataIndex: ['data', 'type'],
      key: 'type',
      render: (type) => type || '-',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status) => (
        <Tag color={STATUS_COLORS[status] || 'default'}>
          {status || 'SCHEDULED'}
        </Tag>
      ),
    },
    {
      title: 'Created',
      dataIndex: 'createdAt',
      key: 'createdAt',
      render: (timestamp) => formatTimestamp(timestamp),
    },
  ];

  if (error) {
    return (
      <Alert
        message="Error"
        description="Failed to load accounts"
        type="error"
        showIcon
      />
    );
  }

  return (
    <div style={{ minHeight: '100vh', background: '#f5f5f5', padding: '24px' }}>
      <Card style={{ maxWidth: 1200, margin: '0 auto' }}>
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <div>
            <Button
              icon={<ArrowLeftOutlined />}
              onClick={() => navigate('/customer/dashboard')}
              style={{ marginBottom: 16 }}
            >
              Back to Dashboard
            </Button>
            <Title level={2}>
              <CalendarOutlined /> My Accounts
            </Title>
            <Paragraph type="secondary">
              View all your scheduled and past accounts.
            </Paragraph>
          </div>

          {isLoading ? (
            <div style={{ textAlign: 'center', padding: '48px' }}>
              <Spin size="large" />
            </div>
          ) : (
            <Table
              columns={columns}
              dataSource={myAccounts}
              rowKey="id"
              pagination={{ pageSize: 10 }}
              scroll={{ x: 800 }}
            />
          )}
        </Space>
      </Card>
    </div>
  );
};

export default CustomerAccounts;
