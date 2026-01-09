/**
 * Cards Statistics Component
 * Mini-dashboard showing card-specific metrics
 */

import { Row, Col, Card, Statistic, Space, Typography, Spin } from 'antd';
import {
  DollarOutlined,
  CreditCardOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
} from '@ant-design/icons';
import { useCards } from '../../hooks/queries/useCards';
import { formatCurrency } from '../../utils/formatters';

const { Text } = Typography;

const CardsStats = () => {
  const { data: cardsData, isLoading } = useCards();
  const cards = cardsData?.items || [];

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '24px' }}>
        <Spin size="large" />
      </div>
    );
  }

  // Calculate statistics
  const totalCards = cards.length;
  const totalAmount = cards.reduce((sum, card) => sum + (card.data?.amount || 0), 0);
  const completedCards = cards.filter(p => p.data?.status === 'COMPLETED');
  const completedAmount = completedCards.reduce((sum, p) => sum + (p.data?.amount || 0), 0);
  const failedCards = cards.filter(p => p.data?.status === 'FAILED').length;
  const pendingCards = cards.filter(p => p.data?.status === 'PENDING').length;

  // Card method distribution
  const methods = {};
  cards.forEach(p => {
    const method = p.data?.method || 'Unknown';
    methods[method] = (methods[method] || 0) + 1;
  });
  const topMethod = Object.entries(methods).sort((a, b) => b[1] - a[1])[0];

  return (
    <div>
      <Row gutter={[16, 16]}>
        {/* Total Cards */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f0f5ff' }}>
            <Statistic
              title={<Text strong>Total Cards</Text>}
              value={totalCards}
              prefix={<CreditCardOutlined style={{ color: '#531dab' }} />}
              valueStyle={{ color: '#531dab' }}
            />
          </Card>
        </Col>

        {/* Total Amount */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f6ffed' }}>
            <Statistic
              title={<Text strong>Total Amount</Text>}
              value={totalAmount}
              prefix={<DollarOutlined style={{ color: '#13c2c2' }} />}
              valueStyle={{ color: '#13c2c2' }}
              precision={2}
            />
          </Card>
        </Col>

        {/* Completed Amount */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f6ffed' }}>
            <Statistic
              title={<Text strong>Completed</Text>}
              value={completedAmount}
              prefix={<CheckCircleOutlined style={{ color: '#13c2c2' }} />}
              valueStyle={{ color: '#13c2c2' }}
              precision={2}
              suffix={`(${completedCards.length})`}
            />
          </Card>
        </Col>

        {/* Failed Cards */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: failedCards > 0 ? '#fff1f0' : '#f6ffed' }}>
            <Statistic
              title={<Text strong>Failed</Text>}
              value={failedCards}
              prefix={failedCards > 0 ? <CloseCircleOutlined style={{ color: '#ff4d4f' }} /> : null}
              valueStyle={{ color: failedCards > 0 ? '#ff4d4f' : '#13c2c2' }}
              suffix={`/ ${totalCards}`}
            />
          </Card>
        </Col>
      </Row>

      {/* Card Methods */}
      <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
        <Col xs={24}>
          <Card size="small" bordered={false}>
            <Space direction="horizontal" size="large" wrap>
              <div>
                <Text type="secondary">Pending</Text>
                <div>
                  <Text strong style={{ fontSize: 16, color: '#faad14' }}>
                    {pendingCards}
                  </Text>
                </div>
              </div>
              {topMethod && (
                <div>
                  <Text type="secondary">Top Method</Text>
                  <div>
                    <Text strong style={{ fontSize: 16, color: '#531dab' }}>
                      {topMethod[0]} ({topMethod[1]})
                    </Text>
                  </div>
                </div>
              )}
            </Space>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default CardsStats;
