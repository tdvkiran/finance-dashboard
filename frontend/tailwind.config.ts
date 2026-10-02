import type { Config } from 'tailwindcss';
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        background: '#0f172a',
        card: '#1e293b',
        border: '#334155',
        primary: '#f8fafc',
        secondary: '#94a3b8',
        accent: '#6366f1',
        success: '#22c55e',
        danger: '#ef4444',
        info: '#3b82f6',
      }
    },
  },
  plugins: [],
} satisfies Config;