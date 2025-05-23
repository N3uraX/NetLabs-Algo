import { forwardRef } from 'react';
import { cn } from '../../lib/utils';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'link' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, children, variant = 'primary', size = 'md', isLoading, disabled, ...props }, ref) => {
    return (
      <button
        className={cn(
          'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed',
          {
            'bg-primary hover:bg-primary-600 active:bg-primary-700 text-white': variant === 'primary',
            'bg-secondary hover:bg-secondary-600 active:bg-secondary-700 text-white': variant === 'secondary',
            'border border-input bg-transparent hover:bg-muted hover:text-foreground': variant === 'outline',
            'bg-transparent hover:bg-muted hover:text-foreground': variant === 'ghost',
            'bg-transparent underline-offset-4 hover:underline text-primary': variant === 'link',
            'bg-error hover:bg-error/90 active:bg-error/80 text-white': variant === 'danger',
            'h-9 px-3 text-sm': size === 'sm',
            'h-10 px-4 py-2': size === 'md',
            'h-11 px-6 text-lg': size === 'lg',
          },
          className
        )}
        ref={ref}
        disabled={isLoading || disabled}
        {...props}
      >
        {isLoading ? (
          <div className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
        ) : null}
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';

export default Button;