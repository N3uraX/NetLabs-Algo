/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: {
          DEFAULT: 'hsl(210 20% 98%)',
          dark: 'hsl(224 71% 4%)',
        },
        foreground: {
          DEFAULT: 'hsl(222.2 47.4% 11.2%)',
          dark: 'hsl(210 40% 98%)',
        },
        primary: {
          DEFAULT: 'hsl(210 100% 50%)',
          foreground: 'hsl(210 40% 98%)',
          50: 'hsl(210 100% 95%)',
          100: 'hsl(210 100% 90%)',
          200: 'hsl(210 100% 80%)',
          300: 'hsl(210 100% 70%)',
          400: 'hsl(210 100% 60%)',
          500: 'hsl(210 100% 50%)',
          600: 'hsl(210 100% 45%)',
          700: 'hsl(210 100% 40%)',
          800: 'hsl(210 100% 35%)',
          900: 'hsl(210 100% 30%)',
          950: 'hsl(210 100% 20%)',
        },
        secondary: {
          DEFAULT: 'hsl(186 100% 40%)',
          foreground: 'hsl(210 40% 98%)',
          50: 'hsl(186 100% 95%)',
          100: 'hsl(186 100% 90%)',
          200: 'hsl(186 100% 80%)',
          300: 'hsl(186 100% 70%)',
          400: 'hsl(186 100% 60%)',
          500: 'hsl(186 100% 50%)',
          600: 'hsl(186 100% 45%)',
          700: 'hsl(186 100% 40%)',
          800: 'hsl(186 100% 35%)',
          900: 'hsl(186 100% 30%)',
          950: 'hsl(186 100% 25%)',
        },
        accent: {
          DEFAULT: 'hsl(280 100% 45%)',
          foreground: 'hsl(210 40% 98%)',
        },
        success: {
          DEFAULT: 'hsl(142 72% 29%)',
          foreground: 'hsl(210 40% 98%)',
        },
        warning: {
          DEFAULT: 'hsl(48 96% 53%)',
          foreground: 'hsl(222.2 47.4% 11.2%)',
        },
        error: {
          DEFAULT: 'hsl(0 84% 60%)',
          foreground: 'hsl(210 40% 98%)',
        },
        card: {
          DEFAULT: 'hsl(0 0% 100%)',
          dark: 'hsl(224 71% 8%)',
          foreground: 'hsl(222.2 47.4% 11.2%)',
          'foreground-dark': 'hsl(210 40% 98%)',
        },
        border: {
          DEFAULT: 'hsl(214.3 31.8% 91.4%)',
          dark: 'hsl(217.2 32.6% 17.5%)',
        },
        input: {
          DEFAULT: 'hsl(214.3 31.8% 91.4%)',
          dark: 'hsl(217.2 32.6% 17.5%)',
        },
        muted: {
          DEFAULT: 'hsl(210 40% 96.1%)',
          dark: 'hsl(223 47% 11%)',
          foreground: 'hsl(215.4 16.3% 46.9%)',
          'foreground-dark': 'hsl(215 20.2% 65.1%)',
        },
        ring: {
          DEFAULT: 'hsl(215 20.2% 65.1%)',
          dark: 'hsl(212.7 26.8% 83.9%)',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      fontSize: {
        xs: ['0.75rem', '1rem'],
        sm: ['0.875rem', '1.25rem'],
        base: ['1rem', '1.5rem'],
        lg: ['1.125rem', '1.75rem'],
        xl: ['1.25rem', '1.875rem'],
        '2xl': ['1.5rem', '2rem'],
        '3xl': ['1.875rem', '2.25rem'],
        '4xl': ['2.25rem', '2.5rem'],
      },
      borderRadius: {
        DEFAULT: '0.375rem',
        sm: '0.25rem',
        md: '0.375rem',
        lg: '0.5rem',
        xl: '0.75rem',
        '2xl': '1rem',
      },
      boxShadow: {
        'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        DEFAULT: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
      },
      animation: {
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'bounce-slow': 'bounce 2s infinite',
      },
      transitionDuration: {
        '2000': '2000ms',
      },
    },
  },
  plugins: [],
};