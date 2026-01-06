/**
 * Ant Design Theme Configuration
 * Insurance Industry Standard - Conservative, Trustworthy, Data-Dense
 */

export const theme = {
  token: {
    // Primary Colors (Trust & Stability)
    colorPrimary: '#0052A3',       // Primary blue (modernized)
    colorSuccess: '#52c41a',       // Success green (approved)
    colorWarning: '#faad14',       // Warning orange (pending)
    colorError: '#ff4d4f',         // Error red (denied)
    colorInfo: '#0066CC',          // Info blue (lighter primary)

    // Secondary/Accent Colors (Teal)
    colorSecondary: '#14B8A6',     // Teal accent
    colorSecondaryHover: '#2DD4BF', // Teal hover
    colorSecondaryActive: '#0F9B8E', // Teal active

    // Typography
    fontFamily: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    fontSize: 14,
    fontSizeHeading1: 32,
    fontSizeHeading2: 24,
    fontSizeHeading3: 20,
    fontSizeHeading4: 16,
    fontSizeHeading5: 14,
    fontWeightStrong: 600,
    fontWeightMedium: 500,
    fontWeightNormal: 400,
    fontWeightLight: 400,

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
    colorLink: '#0052A3',
    colorLinkHover: '#0066CC',
    colorLinkActive: '#003D7A',
  },

  components: {
    // Layout
    Layout: {
      headerBg: '#003D7A',           // Dark blue header (modernized)
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
      itemHoverColor: '#0052A3',
      itemSelectedBg: '#e6f4ff',
      itemSelectedColor: '#0052A3',
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
      activeBorderColor: '#0052A3',
      hoverBorderColor: '#0066CC',
      activeShadow: '0 0 0 2px rgba(0, 82, 163, 0.1)',
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
      boxShadow: '0 2px 4px rgba(0,0,0,0.06)',  // elevation.level2
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
      linkHoverColor: '#0052A3',
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

/**
 * Elevation System (8 levels)
 * Standardized box shadows for consistent depth and hierarchy
 */
export const elevation = {
  level0: 'none',
  level1: '0 1px 2px rgba(0,0,0,0.05)',
  level2: '0 2px 4px rgba(0,0,0,0.06)',
  level3: '0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06)',
  level4: '0 6px 12px rgba(0,0,0,0.08)',
  level5: '0 10px 20px rgba(0,0,0,0.1)',
  level6: '0 15px 30px rgba(0,0,0,0.12)',
  level7: '0 20px 40px rgba(0,0,0,0.15)',
};

/**
 * Gradient System
 * Modern gradient patterns for headers, buttons, cards, and backgrounds
 */
export const gradients = {
  header: 'linear-gradient(135deg, #003D7A 0%, #0052A3 100%)',
  primaryButton: 'linear-gradient(135deg, #0052A3 0%, #0066CC 100%)',
  secondaryButton: 'linear-gradient(135deg, #14B8A6 0%, #2DD4BF 100%)',
  cardAccent: 'linear-gradient(135deg, rgba(20,184,166,0.02) 0%, rgba(0,82,163,0.02) 100%)',
  heroBackground: 'linear-gradient(135deg, #0052A3 0%, #14B8A6 100%)',
};

export default theme;
