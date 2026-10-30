import React from 'react';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  helperText?: string;
  error?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  (
    {
      label,
      helperText,
      error,
      leftIcon,
      rightIcon,
      id,
      className = '',
      disabled,
      ...props
    },
    ref
  ) => {
    const inputId = id || (label ? label.toLowerCase().replace(/\s+/g, '-') : undefined);

    return (
      <div className="w-full space-y-1.5">
        {label && (
          <label
            htmlFor={inputId}
            className="block text-xs font-semibold text-[#252923]"
          >
            {label}
          </label>
        )}

        <div className="relative flex items-center">
          {leftIcon && (
            <div className="absolute left-3 flex items-center pointer-events-none text-[#73796F]">
              {leftIcon}
            </div>
          )}

          <input
            ref={ref}
            id={inputId}
            disabled={disabled}
            aria-invalid={Boolean(error)}
            aria-describedby={
              error ? `${inputId}-error` : helperText ? `${inputId}-helper` : undefined
            }
            className={`w-full rounded-lg border bg-white py-2 text-sm text-[#252923] placeholder:text-[#9A9F96] transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#244B38] focus-visible:ring-offset-1 disabled:bg-[#F7F7F2] disabled:text-[#9A9F96] disabled:cursor-not-allowed ${
              leftIcon ? 'pl-9' : 'pl-3'
            } ${rightIcon ? 'pr-9' : 'pr-3'} ${
              error
                ? 'border-[#9E2A2B] focus-visible:ring-[#9E2A2B]'
                : 'border-[#E5E5DD] hover:border-[#D0D0C5]'
            } ${className}`}
            {...props}
          />

          {rightIcon && (
            <div className="absolute right-3 flex items-center pointer-events-none text-[#73796F]">
              {rightIcon}
            </div>
          )}
        </div>

        {error ? (
          <p id={`${inputId}-error`} className="text-xs text-[#9E2A2B] font-medium">
            {error}
          </p>
        ) : helperText ? (
          <p id={`${inputId}-helper`} className="text-xs text-[#73796F]">
            {helperText}
          </p>
        ) : null}
      </div>
    );
  }
);

Input.displayName = 'Input';
