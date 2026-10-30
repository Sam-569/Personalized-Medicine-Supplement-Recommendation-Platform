import React from 'react';
import { AlertCircle, AlertTriangle, CheckCircle2, Info } from 'lucide-react';

export type AlertVariant = 'info' | 'success' | 'warning' | 'danger';

export interface AlertProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: AlertVariant;
  title?: string;
  icon?: React.ReactNode;
}

export const Alert: React.FC<AlertProps> = ({
  children,
  variant = 'info',
  title,
  icon,
  className = '',
  ...props
}) => {
  const styles: Record<AlertVariant, { container: string; title: string; text: string; icon: React.ReactNode }> = {
    info: {
      container: 'bg-[#F1F6F9] border-[#CCE0EC] text-[#252923]',
      title: 'text-[#2B5876]',
      text: 'text-[#3B454E]',
      icon: <Info className="h-4 w-4 text-[#2B5876] shrink-0" aria-hidden="true" />,
    },
    success: {
      container: 'bg-[#F0F7F3] border-[#CBE3D4] text-[#252923]',
      title: 'text-[#235E3F]',
      text: 'text-[#2E4738]',
      icon: <CheckCircle2 className="h-4 w-4 text-[#235E3F] shrink-0" aria-hidden="true" />,
    },
    warning: {
      container: 'bg-[#FEF9EE] border-[#F3E0B5] text-[#252923]',
      title: 'text-[#8A5C00]',
      text: 'text-[#5E4300]',
      icon: <AlertTriangle className="h-4 w-4 text-[#8A5C00] shrink-0" aria-hidden="true" />,
    },
    danger: {
      container: 'bg-[#FDF2F2] border-[#F5C8C8] text-[#252923]',
      title: 'text-[#9E2A2B]',
      text: 'text-[#5C1A1B]',
      icon: <AlertCircle className="h-4 w-4 text-[#9E2A2B] shrink-0" aria-hidden="true" />,
    },
  };

  const current = styles[variant];

  return (
    <div
      role="alert"
      className={`rounded-xl border p-4 flex items-start gap-3 text-sm ${current.container} ${className}`}
      {...props}
    >
      <div className="mt-0.5">{icon || current.icon}</div>
      <div className="space-y-1 flex-1 min-w-0">
        {title && <h4 className={`text-xs font-bold uppercase tracking-wider ${current.title}`}>{title}</h4>}
        <div className={`text-xs leading-relaxed ${current.text}`}>{children}</div>
      </div>
    </div>
  );
};
