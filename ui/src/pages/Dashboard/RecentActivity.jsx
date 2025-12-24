/**
 * Recent Activity Component
 * Displays a table of recently created entities across all types
 */

import { Table, Tag, Button, Spin } from 'antd';
import { EyeOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { formatTimestamp, formatCurrencyFromCents, formatCoverageType } from '../../utils/formatters';
import { ENTITY_LABELS } from '../../config/constants';
import { useQuotes } from '../../hooks/queries/useQuotes';
import { usePolicies } from '../../hooks/queries/usePolicies';
import { useClaims } from '../../hooks/queries/useClaims';
import { usePayments } from '../../hooks/queries/usePayments';
import { useCases } from '../../hooks/queries/useCases';
import { useMemo } from 'react';

const RecentActivity = () => {
  const navigate = useNavigate();

  // Fetch all entity types
  const { data: quotes, isLoading: quotesLoading } = useQuotes();
  const { data: policies, isLoading: policiesLoading } = usePolicies();
  const { data: claims, isLoading: claimsLoading } = useClaims();
  const { data: payments, isLoading: paymentsLoading } = usePayments();
  const { data: cases, isLoading: casesLoading } = useCases();

  // Combine and sort all items by creation time
  const recentItems = useMemo(() => {
    const allItems = [
      ...(quotes?.items || []).map(q => ({ type: 'quote', ...q })),
      ...(policies?.items || []).map(p => ({ type: 'policy', ...p })),
      ...(claims?.items || []).map(c => ({ type: 'claim', ...c })),
      ...(payments?.items || []).map(p => ({ type: 'payment', ...p })),
      ...(cases?.items || []).map(c => ({ type: 'case', ...c }))
    ];

    // Sort by createdAt descending and take top 20
    return allItems
      .sort((a, b) => (b.createdAt || 0) - (a.createdAt || 0))
      .slice(0, 20);
  }, [quotes, policies, claims, payments, cases]);

  const isLoading = quotesLoading || policiesLoading || claimsLoading || paymentsLoading || casesLoading;

  const columns = [
    {
      title: 'Type',
      dataIndex: 'type',
      key: 'type',
      width: 100,
      render: (type) => {
        const colorMap = {
          quote: 'blue',
          policy: 'green',
          claim: 'orange',
          payment: 'cyan',
          case: 'purple',
        };
        return (
          <Tag color={colorMap[type]}>
            {ENTITY_LABELS[type] || type}
          </Tag>
        );
      },
    },
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 200,
      ellipsis: true,
      render: (id) => (
        <span style={{ fontFamily: 'monospace', fontSize: 12 }}>
          {id?.substring(0, 8)}...
        </span>
      ),
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true,
      render: (_, record) => {
        // Generate a description based on the entity type and data
        if (record.type === 'quote') {
          const coverage = record.data?.coverageType ? formatCoverageType(record.data.coverageType) : '';
          const premium = record.data?.premium_cents ? formatCurrencyFromCents(record.data.premium_cents) : '';
          return `${record.data?.quoteNumber || 'Quote'} - ${record.data?.name || 'N/A'} ${coverage} ${premium}`.trim();
        } else if (record.type === 'policy') {
          const coverage = record.data?.coverageType ? formatCoverageType(record.data.coverageType) : '';
          return `${record.data?.policyNumber || 'Policy'} - ${record.data?.holderName || 'N/A'} (${coverage})`;
        } else if (record.type === 'claim') {
          const amount = record.data?.estimatedAmount_cents ? formatCurrencyFromCents(record.data.estimatedAmount_cents) : '';
          const lossType = record.data?.lossType || '';
          return `${record.data?.claimNumber || 'Claim'} - ${lossType.replace(/_/g, ' ')} ${amount}`.trim();
        } else if (record.type === 'payment') {
          const amount = record.data?.amount_cents ? formatCurrencyFromCents(record.data.amount_cents) : '$0';
          const method = record.data?.paymentMethod || 'N/A';
          return `${amount} via ${method}`;
        } else if (record.type === 'case') {
          const priority = record.data?.priority ? `[${record.data.priority}]` : '';
          return `${priority} ${record.data?.title || 'N/A'}`.trim();
        }
        return '-';
      },
    },
    {
      title: 'Created',
      dataIndex: 'createdAt',
      key: 'createdAt',
      width: 180,
      sorter: (a, b) => (a.createdAt || 0) - (b.createdAt || 0),
      render: (timestamp) => formatTimestamp(timestamp),
      defaultSortOrder: 'descend',
    },
    {
      title: 'Actions',
      key: 'actions',
      width: 100,
      fixed: 'right',
      render: (_, record) => (
        <Button
          type="link"
          size="small"
          icon={<EyeOutlined />}
          onClick={() => navigate(`/${record.type}s/${record.id}`)}
        >
          View
        </Button>
      ),
    },
  ];

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '40px 0' }}>
        <Spin size="large" tip="Loading recent activity..." />
      </div>
    );
  }

  return (
    <Table
      columns={columns}
      dataSource={recentItems}
      rowKey={(record) => `${record.type}-${record.id}`}
      pagination={false}
      size="small"
      locale={{
        emptyText: 'No recent activity. Start by creating a quote, policy, claim, payment, or case.',
      }}
    />
  );
};

export default RecentActivity;
