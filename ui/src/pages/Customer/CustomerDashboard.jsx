/**
 * Customer Dashboard Page
 * Shows policies, claims, and payments for authenticated customer
 */

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Card,
  Row,
  Col,
  Typography,
  Tabs,
  Button,
  Table,
  Tag,
  Space,
  message,
  Spin,
} from 'antd';
import {
  SafetyOutlined,
  FileTextOutlined,
  DollarOutlined,
  PlusOutlined,
} from '@ant-design/icons';
import {
  getCustomerPolicies,
  getCustomerClaims,
  getCustomerPayments,
  getDefaultCustomer,
} from '../../services/customer';
import { formatCurrency, formatDate } from '../../utils/format';

const { Title, Text } = Typography;

const getStatusColor = (status) => {
  const colors = {
    ACTIVE: 'green',
    PENDING: 'orange',
    APPROVED: 'green',
    DENIED: 'red',
    COMPLETED: 'green',
    FAILED: 'red',
  };
  return colors[status] || 'default';
};

const CustomerDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [customer, setCustomer] = useState(null);
  const [policies, setPolicies] = useState([]);
  const [claims, setClaims] = useState([]);
  const [payments, setPayments] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    loadCustomerData();
  }, []);

  const loadCustomerData = async () => {
    setLoading(true);
    try {
      // Get default demo customer
      const customerInfo = await getDefaultCustomer();
      setCustomer(customerInfo);

      // Load all customer data filtered by email
      const [policiesRes, claimsRes, paymentsRes] = await Promise.all([
        getCustomerPolicies(customerInfo.email),
        getCustomerClaims(customerInfo.email),
        getCustomerPayments(customerInfo.email),
      ]);

      setPolicies(policiesRes.policies || []);
      setClaims(claimsRes.claims || []);
      setPayments(paymentsRes.payments || []);
    } catch (error) {
      message.error('Failed to load your information');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const policyColumns = [
    {
      title: 'Policy ID',
      dataIndex: 'id',
      key: 'id',
      render: (id) => id.substring(0, 12) + '...',
    },
    {
      title: 'Coverage',
      dataIndex: ['data', 'coverage_amount'],
      key: 'coverage',
      render: (amount) => formatCurrency(amount * 100),
    },
    {
      title: 'Premium',
      dataIndex: ['data', 'premium_annual'],
      key: 'premium',
      render: (amount) => formatCurrency(amount * 100),
    },
    {
      title: 'Effective Date',
      dataIndex: ['data', 'effective_date'],
      key: 'effective_date',
      render: (date) => formatDate(date),
    },
    {
      title: 'Expiration Date',
      dataIndex: ['data', 'expiration_date'],
      key: 'expiration_date',
      render: (date) => formatDate(date),
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status) => <Tag color={getStatusColor(status)}>{status}</Tag>,
    },
  ];

  const claimColumns = [
    {
      title: 'Claim ID',
      dataIndex: 'id',
      key: 'id',
      render: (id) => id.substring(0, 12) + '...',
    },
    {
      title: 'Type',
      dataIndex: ['data', 'claim_type'],
      key: 'claim_type',
      render: (type) => type?.replace(/_/g, ' ').toUpperCase(),
    },
    {
      title: 'Date of Loss',
      dataIndex: ['data', 'date_of_loss'],
      key: 'date_of_loss',
      render: (date) => formatDate(date),
    },
    {
      title: 'Amount',
      dataIndex: ['data', 'claim_amount'],
      key: 'claim_amount',
      render: (amount) => formatCurrency(amount * 100),
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status) => <Tag color={getStatusColor(status)}>{status}</Tag>,
    },
  ];

  const paymentColumns = [
    {
      title: 'Payment ID',
      dataIndex: 'id',
      key: 'id',
      render: (id) => id.substring(0, 12) + '...',
    },
    {
      title: 'Amount',
      dataIndex: ['data', 'amount'],
      key: 'amount',
      render: (amount) => formatCurrency(amount * 100),
    },
    {
      title: 'Method',
      dataIndex: ['data', 'payment_method'],
      key: 'payment_method',
      render: (method) => method?.replace(/_/g, ' ').toUpperCase(),
    },
    {
      title: 'Card Last 4',
      dataIndex: ['data', 'card_last_four'],
      key: 'card_last_four',
      render: (last4) => last4 ? `•••• ${last4}` : 'N/A',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status) => <Tag color={getStatusColor(status)}>{status}</Tag>,
    },
  ];

  return (
    <div style={{ padding: '24px', background: '#f0f2f5', minHeight: '100vh' }}>
      <Card style={{ marginBottom: 24 }}>
        <Row justify="space-between" align="middle">
          <Col>
            <Title level={3} style={{ marginBottom: 4 }}>
              Customer Portal
            </Title>
            <Text type="secondary">Manage your policies, claims, and payments</Text>
            {customer && (
              <div style={{ marginTop: 8 }}>
                <Tag color="blue">
                  Viewing as: {customer.name} ({customer.email})
                </Tag>
              </div>
            )}
          </Col>
        </Row>
      </Card>

      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={8}>
          <Card>
            <Space direction="vertical" size="small">
              <SafetyOutlined style={{ fontSize: 24, color: '#1890ff' }} />
              <Text type="secondary">Active Policies</Text>
              <Title level={2} style={{ margin: 0 }}>
                {policies.filter(p => p.status === 'ACTIVE').length}
              </Title>
            </Space>
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card>
            <Space direction="vertical" size="small">
              <FileTextOutlined style={{ fontSize: 24, color: '#52c41a' }} />
              <Text type="secondary">Total Claims</Text>
              <Title level={2} style={{ margin: 0 }}>
                {claims.length}
              </Title>
            </Space>
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card>
            <Space direction="vertical" size="small">
              <DollarOutlined style={{ fontSize: 24, color: '#faad14' }} />
              <Text type="secondary">Total Payments</Text>
              <Title level={2} style={{ margin: 0 }}>
                {formatCurrency(
                  payments.reduce((sum, p) => sum + ((p.data?.amount || 0) * 100), 0)
                )}
              </Title>
            </Space>
          </Card>
        </Col>
      </Row>

      <Card>
        <Tabs
          defaultActiveKey="policies"
          items={[
            {
              key: 'policies',
              label: (
                <span>
                  <SafetyOutlined />
                  Policies
                </span>
              ),
              children: loading ? (
                <div style={{ textAlign: 'center', padding: '40px' }}>
                  <Spin size="large" />
                </div>
              ) : (
                <Table
                  columns={policyColumns}
                  dataSource={policies}
                  rowKey="id"
                  pagination={{ pageSize: 10 }}
                />
              ),
            },
            {
              key: 'claims',
              label: (
                <span>
                  <FileTextOutlined />
                  Claims
                </span>
              ),
              children: loading ? (
                <div style={{ textAlign: 'center', padding: '40px' }}>
                  <Spin size="large" />
                </div>
              ) : (
                <div>
                  <div style={{ marginBottom: 16 }}>
                    <Button
                      type="primary"
                      icon={<PlusOutlined />}
                      onClick={() => navigate('/customer/claims/new')}
                    >
                      Submit New Claim
                    </Button>
                  </div>
                  <Table
                    columns={claimColumns}
                    dataSource={claims}
                    rowKey="id"
                    pagination={{ pageSize: 10 }}
                  />
                </div>
              ),
            },
            {
              key: 'payments',
              label: (
                <span>
                  <DollarOutlined />
                  Payments
                </span>
              ),
              children: loading ? (
                <div style={{ textAlign: 'center', padding: '40px' }}>
                  <Spin size="large" />
                </div>
              ) : (
                <Table
                  columns={paymentColumns}
                  dataSource={payments}
                  rowKey="id"
                  pagination={{ pageSize: 10 }}
                />
              ),
            },
          ]}
        />
      </Card>
    </div>
  );
};

export default CustomerDashboard;
