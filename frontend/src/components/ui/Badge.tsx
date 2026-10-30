import React from 'react';
import { CheckCircle2, AlertTriangle, AlertCircle, Info, Shield } from 'lucide-react';

export type BadgeVariant = 'safe' | 'review' | 'excluded' | 'info' | 'neutral';

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: BadgeVariant;
  size?: 'sm' | 'md';
  icon?: boolean | React.ReactNode;
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = 'neutral',
  size = 'md',
  icon = false,
  className = '',
  ...props
}) => {
  const variantStyles: Record<BadgeVariant, string> = {
    safe: 'bg-[#F0F7F3] text-[#235E3F] border-[#CBE3D4]',
    review: 'bg-[#FEF9EE] text-[#8A5C00] border-[#F3E0B5]',
    excluded: 'bg-[#FDF2F2] text-[#9E2A2B] border-[#F5C8C8]',
    info: 'bg-[#F1F6F9] text-[#2B5876] border-[#CCE0EC]',
    neutral: 'bg-[#F3F3EE] text-[#5E645A] border-[#E2E2D9]',
  };

  const sizeStyles = {
    sm: 'text-[11px] px-2 py-0.5 gap-1',
    md: 'text-xs px-2.5 py-1 gap-1.5',
  };

  const defaultIcons: Record<BadgeVariant, React.ReactNode> = {
    safe: <CheckCircle2 className="h-3 w-3 shrink-0" aria-hidden="true" />,
    review: <AlertTriangle className="h-3 w-3 shrink-0" aria-hidden="true" />,
    excluded: <AlertCircle className="h-3 w-3 shrink-0" aria-hidden="true" />,
    info: <Info className="h-3 w-3 shrink-0" aria-hidden="true" />,
    neutral: <Shield className="h-3 w-3 shrink-0" aria-hidden="true" />,
  };

  const renderIcon = () => {
    if (typeof icon === 'boolean') {
      return icon ? defaultIcons[variant] : null;
    }
    return icon;
  };

  return (
    <span
      className={`inline-flex items-center font-medium border rounded-md select-none ${variantStyles[variant]} ${sizeStyles[size]} ${className}`}
      {...props}
    >
      {renderIcon()}
      <span>{children}</span>
    </span>
  );
};
