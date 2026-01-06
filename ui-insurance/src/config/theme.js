/**
 * Ant Design Theme Configuration
 * Insurance Industry Standard - Conservative, Trustworthy, Data-Dense
 */

export const theme = {
  token: {
    // Primary Colors (Trust & Stability)
    colorPrimary: '#003d82',       // Primary blue
    colorSuccess: '#52c41a',       // Success green (approved)
    colorWarning: '#faad14',       // Warning orange (pending)
    colorError: '#ff4d4f',         // Error red (denied)
    colorInfo: '#0066cc',          // Info blue (lighter primary)

    // Typography
    fontFamily: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    fontSize: 14,
    fontSizeHeading1: 32,
    fontSizeHeading2: 24,
    fontSizeHeading3: 20,
    fontSizeHeading4: 16,
    fontSizeHeading5: 14,

    // Layout & Spacing
    borderRadius: 4,
    controlHeight: 36,
    padding: 16,
    margin: 16,

    // Colors
    colorBgLayout: '#f5f5f5',
    colorBgContainer: '#ffffff',
    colorBorder: '#d9d9d9',
    colorBorderSecondary: '#f0f0f0',
    colorText: '#1a1a1a',
    colorTextSecondary: '#595959',
    colorTextTertiary: '#8c8c8c',
    colorTextDisabled: '#bfbfbf',

    // Link Colors
    colorLink: '#003d82',
    colorLinkHover: '#0066cc',
    colorLinkActive: '#002855',
  },

  components: {
    // Layout
    Layout: {
      headerBg: '#002855',           // Dark blue header
      headerHeight: 64,
      headerPadding: '0 24px',
      headerColor: '#ffffff',
      siderBg: '#ffffff',
      bodyBg: '#f5f5f5',
      footerBg: '#ffffff',
      footerPadding: '24px 50px',
    },

    // Menu
    Menu: {
      itemBg: '#ffffff',
      itemColor: '#1a1a1a',
      itemHoverBg: '#f0f7ff',
      itemHoverColor: '#003d82',
      itemSelectedBg: '#e6f4ff',
      itemSelectedColor: '#003d82',
      itemActiveBg: '#e6f4ff',
      iconSize: 18,
      iconMarginInlineEnd: 12,
    },

    // Table
    Table: {
      headerBg: '#fafafa',
      headerColor: '#1a1a1a',
      headerSortActiveBg: '#f0f0f0',
      headerSortHoverBg: '#f5f5f5',
      rowHoverBg: '#f0f7ff',
      rowSelectedBg: '#e6f4ff',
      rowSelectedHoverBg: '#d9edff',
      borderColor: '#d9d9d9',
      fontSize: 14,
      cellPaddingBlock: 12,
      cellPaddingInline: 16,
    },

    // Form
    Form: {
      labelFontSize: 14,
      labelColor: '#1a1a1a',
      labelRequiredMarkColor: '#ff4d4f',
      itemMarginBottom: 24,
    },

    // Input
    Input: {
      paddingBlock: 8,
      paddingInline: 12,
      borderRadius: 4,
      activeBorderColor: '#003d82',
      hoverBorderColor: '#0066cc',
      activeShadow: '0 0 0 2px rgba(0, 61, 130, 0.1)',
    },

    // Button
    Button: {
      primaryColor: '#ffffff',
      primaryShadow: 'none',
      borderRadius: 4,
      controlHeight: 36,
      controlHeightLG: 40,
      controlHeightSM: 32,
      paddingContentHorizontal: 16,
      fontWeight: 500,
    },

    // Card
    Card: {
      borderRadiusLG: 8,
      paddingLG: 24,
      boxShadow: '0 2px 8px rgba(0, 0, 0, 0.06)',
      headerBg: '#fafafa',
      headerFontSize: 16,
      headerHeight: 56,
    },

    // Breadcrumb
    Breadcrumb: {
      fontSize: 14,
      iconFontSize: 14,
      itemColor: '#595959',
      lastItemColor: '#1a1a1a',
      linkColor: '#595959',
      linkHoverColor: '#003d82',
      separatorColor: '#8c8c8c',
      separatorMargin: 8,
    },

    // Tag
    Tag: {
      defaultBg: '#fafafa',
      defaultColor: '#1a1a1a',
      borderRadiusSM: 4,
      fontSizeSM: 12,
    },

    // Modal
    Modal: {
      headerBg: '#ffffff',
      titleFontSize: 20,
      titleLineHeight: 1.4,
      contentBg: '#ffffff',
      footerBg: '#ffffff',
    },

    // Notification
    Notification: {
      width: 384,
    },

    // Badge
    Badge: {
      dotSize: 8,
      fontSize: 12,
      fontWeight: 500,
    },

    // Descriptions
    Descriptions: {
      labelBg: '#fafafa',
      titleColor: '#1a1a1a',
      titleMarginBottom: 16,
      itemPaddingBottom: 12,
      colonMarginRight: 8,
      colonMarginLeft: 2,
      contentColor: '#1a1a1a',
    },
  },
};

export default theme;
