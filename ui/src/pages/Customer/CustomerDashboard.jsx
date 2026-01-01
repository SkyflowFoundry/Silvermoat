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
      // Load all customer data (no auth required for demo)
      const [policiesRes, claimsRes, paymentsRes] = await Promise.all([
        getCustomerPolicies(),
        getCustomerClaims(),
        getCustomerPayments(),
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
      title: 'Policy Number',
      dataIndex: ['data', 'policyNumber'],
      key: 'policyNumber',
    },
    {
      title: 'Type',
      dataIndex: ['data', 'coverageType'],
      key: 'coverageType',
    },
    {
      title: 'Premium',
      dataIndex: ['data', 'premium_cents'],
      key: 'premium',
      render: (cents) => formatCurrency(cents),
    },
    {
      title: 'Effective Date',
      dataIndex: ['data', 'effectiveDate'],
      key: 'effectiveDate',
      render: (date) => formatDate(date),
    },
    {
      title: 'Status',
      dataIndex: ['data', 'status'],
      key: 'status',
      render: (status) => <Tag color={getStatusColor(status)}>{status}</Tag>,
    },
  ];

  const claimColumns = [
    {
      title: 'Claim Number',
      dataIndex: ['data', 'claimNumber'],
      key: 'claimNumber',
    },
    {
      title: 'Type',
      dataIndex: ['data', 'lossType'],
      key: 'lossType',
      render: (type) => type?.replace(/_/g, ' '),
    },
    {
      title: 'Incident Date',
      dataIndex: ['data', 'incidentDate'],
      key: 'incidentDate',
      render: (date) => formatDate(date),
    },
    {
      title: 'Amount',
      dataIndex: ['data', 'estimatedAmount_cents'],
      key: 'amount',
      render: (cents) => formatCurrency(cents),
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
      title: 'Payment Number',
      dataIndex: ['data', 'paymentNumber'],
      key: 'paymentNumber',
    },
    {
      title: 'Amount',
      dataIndex: ['data', 'amount_cents'],
      key: 'amount',
      render: (cents) => formatCurrency(cents),
    },
    {
      title: 'Method',
      dataIndex: ['data', 'paymentMethod'],
      key: 'method',
      render: (method) => method?.replace(/_/g, ' '),
    },
    {
      title: 'Date',
      dataIndex: ['data', 'paidDate'],
      key: 'date',
      render: (date) => formatDate(date) || 'Pending',
    },
    {
      title: 'Status',
      dataIndex: ['data', 'status'],
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
                {policies.filter(p => p.data?.status === 'ACTIVE').length}
              </Title>
            </Space>
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card>
            <Space direction="vertical" size="small">
              <FileTextOutlined style={{ fontSize: 24, color: '#52c41a' }} />
              <Text type="secondary">Open Claims</Text>
              <Title level={2} style={{ margin: 0 }}>
                {claims.filter(c => ['PENDING', 'REVIEW'].includes(c.status)).length}
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
                  payments
                    .filter(p => p.data?.status === 'COMPLETED')
                    .reduce((sum, p) => sum + (p.data?.amount_cents || 0), 0)
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
