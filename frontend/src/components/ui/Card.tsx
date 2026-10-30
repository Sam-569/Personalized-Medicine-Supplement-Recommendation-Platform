import React from 'react';

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  bordered?: boolean;
}

export const Card: React.FC<CardProps> = ({
  children,
  bordered = true,
  className = '',
  ...props
}) => {
  return (
    <div
      className={`rounded-xl bg-white ${
        bordered ? 'border border-[#E5E5DD]' : ''
      } shadow-2xs ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};

export const CardHeader: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({
  children,
  className = '',
  ...props
}) => {
  return (
    <div className={`p-5 sm:p-6 border-b border-[#E5E5DD] ${className}`} {...props}>
      {children}
    </div>
  );
};

export const CardTitle: React.FC<React.HTMLAttributes<HTMLHeadingElement>> = ({
  children,
  className = '',
  ...props
}) => {
  return (
    <h3
      className={`text-base font-bold text-[#252923] tracking-tight ${className}`}
      {...props}
    >
      {children}
    </h3>
  );
};

export const CardDescription: React.FC<React.HTMLAttributes<HTMLParagraphElement>> = ({
  children,
  className = '',
  ...props
}) => {
  return (
    <p className={`text-xs text-[#73796F] mt-1 ${className}`} {...props}>
      {children}
    </p>
  );
};

export const CardContent: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({
  children,
  className = '',
  ...props
}) => {
  return (
    <div className={`p-5 sm:p-6 ${className}`} {...props}>
      {children}
    </div>
  );
};

export const CardFooter: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({
  children,
  className = '',
  ...props
}) => {
  return (
    <div
      className={`p-4 sm:px-6 bg-[#F7F7F2]/50 border-t border-[#E5E5DD] rounded-b-xl flex items-center justify-between ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};
