import React from 'react';
import { Shield, ExternalLink } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="mt-16 border-t border-[#E5E5DD] bg-white py-10 text-[#73796F] text-xs">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          <div>
            <div className="flex items-center gap-2 text-[#252923] font-bold mb-2">
              <Shield className="h-4 w-4 text-[#244B38]" aria-hidden="true" />
              <span className="text-sm font-semibold">Personalized Supplement Guidance</span>
            </div>
            <p className="leading-relaxed text-[#73796F]">
              Open-source academic engineering project demonstrating deterministic recommendation logic, transparent weighted scoring, and safety-aware filtering without black-box ML models.
            </p>
          </div>

          <div>
            <h4 className="font-semibold text-[#252923] text-xs uppercase tracking-wider mb-2.5">
              Academic and Project Specifications
            </h4>
            <ul className="space-y-1.5 text-[#73796F]">
              <li><strong className="text-[#252923]">Degree:</strong> B.Tech Computer Engineering</li>
              <li><strong className="text-[#252923]">SRS Version:</strong> 1.0 (September 2026)</li>
              <li><strong className="text-[#252923]">Project Group:</strong> Group 101</li>
              <li><strong className="text-[#252923]">Methodology:</strong> Multi-Criteria Decision Analysis (WSM)</li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold text-[#252923] text-xs uppercase tracking-wider mb-2.5">
              Knowledge Base Sources
            </h4>
            <ul className="space-y-1.5 text-[#73796F]">
              <li>
                <a
                  href="https://ods.od.nih.gov/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1 hover:text-[#244B38] transition-colors"
                >
                  <span>NIH Office of Dietary Supplements (ODS)</span>
                  <ExternalLink className="h-3 w-3" aria-hidden="true" />
                </a>
              </li>
              <li>
                <a
                  href="https://dsld.od.nih.gov/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1 hover:text-[#244B38] transition-colors"
                >
                  <span>Dietary Supplement Label Database (DSLD)</span>
                  <ExternalLink className="h-3 w-3" aria-hidden="true" />
                </a>
              </li>
              <li>
                <a
                  href="https://www.nccih.nih.gov/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1 hover:text-[#244B38] transition-colors"
                >
                  <span>NCCIH Herbs at a Glance monographs</span>
                  <ExternalLink className="h-3 w-3" aria-hidden="true" />
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-[#E5E5DD] pt-6 flex flex-col sm:flex-row items-center justify-between gap-2 text-[#9A9F96]">
          <span>&copy; {new Date().getFullYear()} Group 101. Open Source Health Informatics Guidance Platform.</span>
          <span>Deterministic. Transparent. Safety-First.</span>
        </div>
      </div>
    </footer>
  );
};
