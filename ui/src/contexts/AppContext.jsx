/**
 * Application Context
 * Manages global UI state (sidebar, filters, user preferences)
 */

import { createContext, useContext, useState, useMemo, useEffect } from 'react';
import { Grid } from 'antd';

const { useBreakpoint } = Grid;

// Create Context
const AppContext = createContext(undefined);

// Custom hook for using the app context
export const useAppContext = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};

// Provider Component
export const AppProvider = ({ children }) => {
  const screens = useBreakpoint();
  const isMobile = !screens.md; // md breakpoint is 768px

  // Sidebar state (desktop)
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  // Mobile drawer state
  const [mobileDrawerOpen, setMobileDrawerOpen] = useState(false);

  // Chat drawer state
  const [chatDrawerOpen, setChatDrawerOpen] = useState(false);

  // Current entity filters (for list pages)
  const [entityFilters, setEntityFilters] = useState({
    quote: {},
    policy: {},
    claim: {},
    payment: {},
    case: {},
  });

  // Table size preference
  const [tableSize, setTableSize] = useState('middle'); // 'small' | 'middle' | 'large'

  // Theme mode (for future dark mode support)
  const [themeMode, setThemeMode] = useState('light'); // 'light' | 'dark'

  // Toggle sidebar collapse (desktop)
  const toggleSidebar = () => {
    setSidebarCollapsed((prev) => !prev);
  };

  // Toggle mobile drawer
  const toggleMobileDrawer = () => {
    setMobileDrawerOpen((prev) => !prev);
  };

  // Close mobile drawer
  const closeMobileDrawer = () => {
    setMobileDrawerOpen(false);
  };

  // Toggle chat drawer
  const toggleChatDrawer = () => {
    setChatDrawerOpen((prev) => !prev);
  };

  // Close chat drawer
  const closeChatDrawer = () => {
    setChatDrawerOpen(false);
  };

  // Auto-collapse sidebar on mobile
  useEffect(() => {
    if (isMobile) {
      setSidebarCollapsed(true);
      setMobileDrawerOpen(false);
    }
  }, [isMobile]);

  // Set filter for specific entity
  const setFilter = (entity, filterKey, filterValue) => {
    setEntityFilters((prev) => ({
      ...prev,
      [entity]: {
        ...prev[entity],
        [filterKey]: filterValue,
      },
    }));
  };

  // Clear all filters for an entity
  const clearFilters = (entity) => {
    setEntityFilters((prev) => ({
      ...prev,
      [entity]: {},
    }));
  };

  // Clear all filters for all entities
  const clearAllFilters = () => {
    setEntityFilters({
      quote: {},
      policy: {},
      claim: {},
      payment: {},
      case: {},
    });
  };

  // Memoize context value to prevent unnecessary re-renders
  const value = useMemo(
    () => ({
      // Responsive
      isMobile,
      screens,

      // Sidebar (desktop)
      sidebarCollapsed,
      setSidebarCollapsed,
      toggleSidebar,

      // Mobile drawer
      mobileDrawerOpen,
      setMobileDrawerOpen,
      toggleMobileDrawer,
      closeMobileDrawer,

      // Chat drawer
      chatDrawerOpen,
      setChatDrawerOpen,
      toggleChatDrawer,
      closeChatDrawer,

      // Filters
      entityFilters,
      setEntityFilters,
      setFilter,
      clearFilters,
      clearAllFilters,

      // Table
      tableSize,
      setTableSize,

      // Theme
      themeMode,
      setThemeMode,
    }),
    [isMobile, screens, sidebarCollapsed, mobileDrawerOpen, chatDrawerOpen, entityFilters, tableSize, themeMode]
  );

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};

export default AppContext;
