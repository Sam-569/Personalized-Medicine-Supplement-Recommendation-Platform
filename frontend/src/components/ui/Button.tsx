import React from 'react';
import { Loader2 } from 'lucide-react';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      children,
      variant = 'primary',
      size = 'md',
      isLoading = false,
      leftIcon,
      rightIcon,
      className = '',
      disabled,
      ...props
    },
    ref
  ) => {
    const baseStyles =
      'inline-flex items-center justify-center font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#244B38] focus-visible:ring-offset-1 disabled:opacity-50 disabled:cursor-not-allowed select-none rounded-lg cursor-pointer';

    const sizeStyles = {
      sm: 'h-8 px-3 text-xs gap-1.5',
      md: 'h-10 px-4 text-sm gap-2',
      lg: 'h-11 px-5 text-sm font-semibold gap-2.5',
    };

    const variantStyles = {
      primary:
        'bg-[#244B38] text-white shadow-2xs hover:bg-[#1B382A] active:bg-[#14291F]',
      secondary:
        'bg-white text-[#252923] border border-[#E5E5DD] shadow-2xs hover:bg-[#F7F7F2] hover:border-[#D0D0C5] active:bg-[#EFEFE8]',
      outline:
        'bg-transparent text-[#244B38] border border-[#244B38] hover:bg-[#EEF3EE] active:bg-[#DCE6DE]',
      ghost:
        'bg-transparent text-[#252923] hover:bg-[#F7F7F2] hover:text-[#1B382A] active:bg-[#EFEFE8]',
      danger:
        'bg-[#FDF2F2] text-[#9E2A2B] border border-[#F5C8C8] hover:bg-[#FCE6E6] active:bg-[#F8D4D4]',
    };

    return (
      <button
        ref={ref}
        disabled={disabled || isLoading}
        className={`${baseStyles} ${sizeStyles[size]} ${variantStyles[variant]} ${className}`}
        {...props}
      >
        {isLoading ? (
          <Loader2 className="h-4 w-4 animate-spin shrink-0" aria-hidden="true" />
        ) : (
          leftIcon
        )}
        <span>{children}</span>
        {!isLoading && rightIcon}
      </button>
    );
  }
);

Button.displayName = 'Button';
