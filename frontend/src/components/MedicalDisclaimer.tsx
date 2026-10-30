import React from 'react';
import { AlertTriangle } from 'lucide-react';

export const MedicalDisclaimer: React.FC<{ compact?: boolean }> = ({ compact = false }) => {
  if (compact) {
    return (
      <div className="flex items-center gap-2 rounded-lg border border-[#F3E0B5] bg-[#FEF9EE] px-3 py-2 text-xs text-[#5E4300]">
        <AlertTriangle className="h-3.5 w-3.5 shrink-0 text-[#8A5C00]" aria-hidden="true" />
        <span>Informational guidance only. Not medical advice, diagnosis, or prescription.</span>
      </div>
    );
  }

  return (
    <div className="my-6 rounded-xl border border-[#F3E0B5] bg-[#FEF9EE] p-4 text-xs text-[#5E4300] shadow-2xs">
      <div className="flex items-start gap-3">
        <div className="rounded-lg bg-[#FDF1D8] p-2 text-[#8A5C00] shrink-0 mt-0.5">
          <AlertTriangle className="h-4 w-4" aria-hidden="true" />
        </div>
        <div className="space-y-1">
          <h4 className="font-bold text-[#8A5C00] uppercase tracking-wider text-[11px]">
            Important Medical and Regulatory Notice
          </h4>
          <p className="leading-relaxed text-[#5E4300]">
            This platform provides structured health and supplement educational information based on a deterministic, rule-based algorithm and a curated knowledge base. It is <strong>not a medical diagnostic tool</strong>, does not prescribe medications or supplements, and does not replace consultation with a qualified healthcare professional.
          </p>
          <p className="text-[11px] text-[#724C00]">
            Relevance scores represent configured project-defined rankings (Group 101 SRS v1.0), not probabilities of clinical efficacy or health outcomes. Always consult a physician before beginning any supplement regimen.
          </p>
        </div>
      </div>
    </div>
  );
};
