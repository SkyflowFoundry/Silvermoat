/**
 * Orders Statistics Component
 * Mini-dashboard showing order-specific metrics
 */

import { Row, Col, Card, Statistic, Space, Typography, Spin } from 'antd';
import {
  ShoppingCartOutlined,
  DollarOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
} from '@ant-design/icons';
import { useOrders } from '../../hooks/queries/useOrders';
import { formatCurrency } from '../../utils/formatters';

const { Text } = Typography;

const OrdersStats = () => {
  const { data: ordersData, isLoading } = useOrders();
  const orders = ordersData?.items || [];

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '24px' }}>
        <Spin size="large" />
      </div>
    );
  }

  // Calculate statistics
  const totalOrders = orders.length;
  const totalRevenue = orders.reduce((sum, order) => sum + (order.data?.totalAmount || 0), 0);
  const avgOrderValue = totalOrders > 0 ? totalRevenue / totalOrders : 0;

  // Status counts
  const pendingOrders = orders.filter(o => o.data?.status === 'PENDING').length;
  const processingOrders = orders.filter(o => o.data?.status === 'PROCESSING').length;
  const shippedOrders = orders.filter(o => o.data?.status === 'SHIPPED').length;
  const deliveredOrders = orders.filter(o => o.data?.status === 'DELIVERED').length;
  const completedOrders = deliveredOrders; // Consider delivered as completed

  return (
    <div>
      <Row gutter={[16, 16]}>
        {/* Total Orders */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f0f5ff' }}>
            <Statistic
              title={<Text strong>Total Orders</Text>}
              value={totalOrders}
              prefix={<ShoppingCartOutlined style={{ color: '#531dab' }} />}
              valueStyle={{ color: '#531dab' }}
            />
          </Card>
        </Col>

        {/* Total Revenue */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f6ffed' }}>
            <Statistic
              title={<Text strong>Total Revenue</Text>}
              value={totalRevenue}
              prefix={<DollarOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#52c41a' }}
              precision={2}
            />
          </Card>
        </Col>

        {/* Avg Order Value */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#fffbe6' }}>
            <Statistic
              title={<Text strong>Avg Order Value</Text>}
              value={avgOrderValue}
              prefix={<DollarOutlined style={{ color: '#faad14' }} />}
              valueStyle={{ color: '#faad14' }}
              precision={2}
            />
          </Card>
        </Col>

        {/* Completed Orders */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f6ffed' }}>
            <Statistic
              title={<Text strong>Completed</Text>}
              value={completedOrders}
              prefix={<CheckCircleOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#52c41a' }}
              suffix={`/ ${totalOrders}`}
            />
          </Card>
        </Col>
      </Row>

      {/* Status Breakdown */}
      <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
        <Col xs={24}>
          <Card size="small" bordered={false}>
            <Space direction="horizontal" size="large" wrap>
              <div>
                <Text type="secondary">Pending</Text>
                <div>
                  <Text strong style={{ fontSize: 16, color: '#faad14' }}>
                    {pendingOrders}
                  </Text>
                </div>
              </div>
              <div>
                <Text type="secondary">Processing</Text>
                <div>
                  <Text strong style={{ fontSize: 16, color: '#1890ff' }}>
                    {processingOrders}
                  </Text>
                </div>
              </div>
              <div>
                <Text type="secondary">Shipped</Text>
                <div>
                  <Text strong style={{ fontSize: 16, color: '#13c2c2' }}>
                    {shippedOrders}
                  </Text>
                </div>
              </div>
              <div>
                <Text type="secondary">Delivered</Text>
                <div>
                  <Text strong style={{ fontSize: 16, color: '#52c41a' }}>
                    {deliveredOrders}
                  </Text>
                </div>
              </div>
            </Space>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default OrdersStats;
