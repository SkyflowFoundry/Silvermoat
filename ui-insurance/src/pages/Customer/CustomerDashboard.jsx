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
  Select,
  Drawer,
  Grid,
} from 'antd';
import {
  SafetyOutlined,
  FileTextOutlined,
  DollarOutlined,
  PlusOutlined,
  UserOutlined,
  HomeOutlined,
  MessageOutlined,
} from '@ant-design/icons';
import CustomerChatInterface from '../../components/customer-chat/CustomerChatInterface';
import {
  getCustomerPolicies,
  getCustomerClaims,
  getCustomerPayments,
  getDefaultCustomer,
  getAvailableCustomers,
} from '../../services/customer';
import { formatCurrency, formatDate } from '../../utils/format';

const { Title, Text } = Typography;
const { useBreakpoint } = Grid;

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
  const [availableCustomers, setAvailableCustomers] = useState([]);
  const [policies, setPolicies] = useState([]);
  const [claims, setClaims] = useState([]);
  const [payments, setPayments] = useState([]);
  const [chatDrawerOpen, setChatDrawerOpen] = useState(false);
  const navigate = useNavigate();
  const screens = useBreakpoint();
  const isMobile = !screens.md;

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    setLoading(true);
    try {
      // Get all available customers
      const customers = await getAvailableCustomers();
      setAvailableCustomers(customers);

      // Set default customer and load their data
      if (customers.length > 0) {
        const defaultCustomer = customers[0];
        setCustomer(defaultCustomer);
        await loadCustomerData(defaultCustomer.email);
      }
    } catch (error) {
      message.error('Failed to load customer data');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const loadCustomerData = async (email) => {
    try {
      // Load all customer data filtered by email
      const [policiesRes, claimsRes, paymentsRes] = await Promise.all([
        getCustomerPolicies(email),
        getCustomerClaims(email),
        getCustomerPayments(email),
      ]);

      setPolicies(policiesRes.policies || []);
      setClaims(claimsRes.claims || []);
      setPayments(paymentsRes.payments || []);
    } catch (error) {
      message.error('Failed to load customer information');
      console.error(error);
    }
  };

  const handleCustomerChange = async (email) => {
    const selectedCustomer = availableCustomers.find(c => c.email === email);
    if (selectedCustomer) {
      setCustomer(selectedCustomer);
      setLoading(true);
      await loadCustomerData(email);
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
      dataIndex: ['data', 'coverageLimit_cents'],
      key: 'coverage',
      render: (amount) => formatCurrency(amount),
    },
    {
      title: 'Premium',
      dataIndex: ['data', 'premium'],
      key: 'premium',
      render: (amount) => formatCurrency(amount),
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
      render: (amount) => formatCurrency(amount),
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
      render: (amount) => formatCurrency(amount),
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
    <div style={{ padding: '16px', background: '#f0f2f5', minHeight: '100vh', position: 'relative' }}>
      <Button
        type="text"
        icon={<HomeOutlined />}
        onClick={() => navigate('/')}
        style={{
          position: 'fixed',
          top: '16px',
          left: '16px',
          zIndex: 1000,
          fontSize: '16px',
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          padding: '8px 16px',
          height: 'auto',
          background: 'rgba(255, 255, 255, 0.95)',
          border: '1px solid #d9d9d9',
          borderRadius: '6px',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
        }}
      >
        Home
      </Button>

      {/* Floating Chat Button */}
      {customer && (
        <Button
          type="primary"
          icon={<MessageOutlined />}
          onClick={() => setChatDrawerOpen(true)}
          style={{
            position: 'fixed',
            bottom: '24px',
            right: '24px',
            zIndex: 1000,
            width: isMobile ? '56px' : '60px',
            height: isMobile ? '56px' : '60px',
            borderRadius: '50%',
            fontSize: isMobile ? '20px' : '24px',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
          aria-label="Open chat assistant"
        />
      )}
      <Card style={{ marginBottom: 16 }}>
        <Row justify="space-between" align="middle">
          <Col>
            <Title level={3} style={{ marginBottom: 4 }}>
              Customer Portal
            </Title>
            <Text type="secondary">Manage your policies, claims, and payments</Text>
          </Col>
        </Row>
        {customer && (
          <div style={{ marginTop: 16, display: 'flex', alignItems: 'center', gap: 12, flexWrap: 'wrap' }}>
            <UserOutlined style={{ fontSize: 16, color: '#1890ff' }} />
            <Text strong>Viewing as:</Text>
            <Select
              value={customer.email}
              onChange={handleCustomerChange}
              style={{ minWidth: 200, maxWidth: '100%', flex: '1 1 auto' }}
              placeholder="Select a customer"
              loading={loading}
            >
              {availableCustomers.map(c => (
                <Select.Option key={c.email} value={c.email}>
                  {c.name} ({c.email})
                </Select.Option>
              ))}
            </Select>
            <Tag color="blue">{policies.length} policies</Tag>
          </div>
        )}
      </Card>

      <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
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
                  payments.reduce((sum, p) => sum + (p.data?.amount || 0), 0)
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
                  scroll={{ x: true }}
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
                    scroll={{ x: true }}
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
                  scroll={{ x: true }}
                />
              ),
            },
          ]}
        />
      </Card>

      {/* Chat Drawer */}
      {customer && (
        <Drawer
          title={null}
          placement="right"
          width={isMobile ? '100%' : 450}
          onClose={() => setChatDrawerOpen(false)}
          open={chatDrawerOpen}
          closable={false}
          bodyStyle={{ padding: 0, height: '100%' }}
          style={{ height: '100%' }}
        >
          <CustomerChatInterface
            customerEmail={customer.email}
            onClose={() => setChatDrawerOpen(false)}
            isMobile={isMobile}
          />
        </Drawer>
      )}
    </div>
  );
};

export default CustomerDashboard;
