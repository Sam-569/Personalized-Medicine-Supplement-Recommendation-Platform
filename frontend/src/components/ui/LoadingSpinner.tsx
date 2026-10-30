import React from 'react';
import { Loader2 } from 'lucide-react';

export interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  label?: string;
  className?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'md',
  label = 'Loading...',
  className = '',
}) => {
  const sizeMap = {
    sm: 'h-4 w-4',
    md: 'h-6 w-6',
    lg: 'h-8 w-8',
  };

  return (
    <div
      role="status"
      className={`inline-flex items-center gap-2 text-[#73796F] ${className}`}
    >
      <Loader2
        className={`${sizeMap[size]} animate-spin text-[#244B38] shrink-0`}
        aria-hidden="true"
      />
      {label && <span className="text-xs font-medium">{label}</span>}
      <span className="sr-only">{label}</span>
    </div>
  );
};

export const LoadingScreen: React.FC<{ message?: string }> = ({
  message = 'Loading data...',
}) => {
  return (
    <div
      role="status"
      className="flex flex-col items-center justify-center py-20 px-4 text-center space-y-3"
    >
      <Loader2 className="h-8 w-8 animate-spin text-[#244B38]" aria-hidden="true" />
      <p className="text-sm text-[#73796F] font-medium">{message}</p>
      <span className="sr-only">{message}</span>
    </div>
  );
};
