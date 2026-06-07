/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      colors: {
        fifa: {
          50: '#fefce8',
          100: '#fef9c3',
          200: '#fef08a',
          300: '#fde047',
          400: '#facc15',
          500: '#eab308',
          600: '#ca8a04',
        },
        pitch: {
          50: '#f0fdf4',
          100: '#dcfce7',
          200: '#bbf7d0',
          300: '#86efac',
          400: '#4ade80',
          500: '#22c55e',
          600: '#16a34a',
          700: '#15803d',
          800: '#166534',
          900: '#14532d',
          950: '#052e16',
        },
        neon: {
          blue: '#00d4ff',
          purple: '#a855f7',
          pink: '#ff6b9d',
          green: '#4ade80',
          gold: '#facc15',
        },
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'shimmer': 'shimmer 2s infinite',
        'pitch-scan': 'pitchScan 3s ease-in-out infinite',
        'player-idle': 'playerIdle 2s ease-in-out infinite',
        'player-celebrate': 'playerCelebrate 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55)',
        'glow-pulse': 'glowPulse 2s ease-in-out infinite',
        'scanner-line': 'scannerLine 2s ease-in-out infinite',
        '3d-rotate': 'rotate3d 6s linear infinite',
        'float-fast': 'floatFast 2s ease-in-out infinite',
        'goal-spark': 'goalSpark 0.8s ease-out forwards',
      },
      keyframes: {
        shimmer: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' },
        },
        pulseSlow: {
          '0%, 100%': { opacity: '1', transform: 'scale(1)' },
          '50%': { opacity: '0.8', transform: 'scale(0.98)' },
        },
        pitchScan: {
          '0%, 100%': { 'background-position': '0% 50%' },
          '50%': { 'background-position': '100% 50%' },
        },
        playerIdle: {
          '0%, 100%': { transform: 'translateY(0) scale(1)', filter: 'brightness(1)' },
          '50%': { transform: 'translateY(-6px) scale(1.02)', filter: 'brightness(1.1)' },
        },
        playerCelebrate: {
          '0%': { transform: 'scale(1) rotate(0deg)', filter: 'brightness(1)' },
          '25%': { transform: 'scale(1.15) rotate(-8deg)', filter: 'brightness(1.5) drop-shadow(0 0 20px rgba(250, 204, 21, 0.8))' },
          '75%': { transform: 'scale(1.1) rotate(8deg)', filter: 'brightness(1.3) drop-shadow(0 0 15px rgba(250, 204, 21, 0.6))' },
          '100%': { transform: 'scale(1) rotate(0deg)', filter: 'brightness(1) drop-shadow(0 0 0px rgba(250, 204, 21, 0))' },
        },
        glowPulse: {
          '0%, 100%': { boxShadow: '0 0 10px rgba(250, 204, 21, 0.2), 0 0 30px rgba(250, 204, 21, 0.05)' },
          '50%': { boxShadow: '0 0 25px rgba(250, 204, 21, 0.4), 0 0 60px rgba(250, 204, 21, 0.15)' },
        },
        scannerLine: {
          '0%': { transform: 'translateY(-100%)', opacity: '0' },
          '20%, 80%': { opacity: '1' },
          '100%': { transform: 'translateY(100%)', opacity: '0' },
        },
        rotate3d: {
          '0%': { transform: 'perspective(800px) rotateX(0deg) rotateY(0deg)' },
          '25%': { transform: 'perspective(800px) rotateX(5deg) rotateY(-5deg)' },
          '50%': { transform: 'perspective(800px) rotateX(0deg) rotateY(0deg)' },
          '75%': { transform: 'perspective(800px) rotateX(-5deg) rotateY(5deg)' },
          '100%': { transform: 'perspective(800px) rotateX(0deg) rotateY(0deg)' },
        },
        floatFast: {
          '0%, 100%': { transform: 'translateY(0) scale(1)', filter: 'brightness(1)' },
          '50%': { transform: 'translateY(-15px) scale(1.05)', filter: 'brightness(1.2)' },
        },
        goalSpark: {
          '0%': { transform: 'scale(0) rotate(0deg)', opacity: '1' },
          '50%': { transform: 'scale(1.3) rotate(180deg)', opacity: '0.8' },
          '100%': { transform: 'scale(0) rotate(360deg)', opacity: '0' },
        },
      },
    },
  },
  plugins: [],
}
