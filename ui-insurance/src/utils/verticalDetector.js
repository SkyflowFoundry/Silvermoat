/**
 * Vertical detection from subdomain
 * Extracts vertical from window.location.hostname
 */

/**
 * Detect vertical from current hostname
 * @returns {string} Vertical name: "insurance" or "retail" (defaults to "insurance")
 *
 * Examples:
 *   insurance.silvermoat.net -> insurance
 *   retail.silvermoat.net -> retail
 *   silvermoat.net -> insurance (default)
 *   localhost -> insurance (local dev)
 */
export const detectVertical = () => {
  const hostname = window.location.hostname.toLowerCase();

  // localhost or IP address -> default to insurance
  if (hostname.includes('localhost') || hostname.match(/^\d+\.\d+\.\d+\.\d+$/)) {
    return 'insurance';
  }

  // Extract subdomain
  const parts = hostname.split('.');

  // Check if first part is a known vertical
  const subdomain = parts.length > 1 ? parts[0] : '';

  const validVerticals = ['insurance', 'retail'];

  if (validVerticals.includes(subdomain)) {
    return subdomain;
  }

  // Default to insurance (covers silvermoat.net, unknown subdomains, etc.)
  return 'insurance';
};
