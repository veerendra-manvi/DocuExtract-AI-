import React from 'react';
import { CheckCircle2, AlertTriangle, XCircle } from 'lucide-react';
import type { ValidationReport } from '../types';
import { cn } from '../lib/utils';

interface ValidationCardProps {
  validation: ValidationReport;
}

export const ValidationCard: React.FC<ValidationCardProps> = ({ validation }) => {
  if (!validation) return null;

  const isValid = Boolean(validation?.is_valid);
  const errors = Array.isArray(validation?.errors) ? validation.errors : [];
  const warnings = Array.isArray(validation?.warnings) ? validation.warnings : [];
  
  const isSuccess = isValid && errors.length === 0 && warnings.length === 0;
  
  return (
    <div className={cn(
      "rounded-xl border p-4 shadow-sm",
      isValid ? "bg-emerald-50/50 border-emerald-100" : "bg-red-50/50 border-red-100"
    )}>
      <div className="flex items-center gap-3 mb-4">
        {isSuccess ? (
          <CheckCircle2 className="w-6 h-6 text-success" />
        ) : isValid ? (
          <AlertTriangle className="w-6 h-6 text-warning" />
        ) : (
          <XCircle className="w-6 h-6 text-error" />
        )}
        <h3 className="font-semibold text-gray-900">
          {isValid ? "Validation Passed" : "Validation Failed"}
        </h3>
      </div>
      
      {(errors.length > 0 || warnings.length > 0) && (
        <div className="space-y-3">
          {errors.length > 0 && (
            <div>
              <h4 className="text-xs font-semibold text-error uppercase tracking-wider mb-2">Errors</h4>
              <ul className="space-y-1">
                {errors.map((error, idx) => (
                  <li key={idx} className="text-sm text-red-700 flex items-start gap-2">
                    <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-red-400 shrink-0"></span>
                    {error}
                  </li>
                ))}
              </ul>
            </div>
          )}
          
          {warnings.length > 0 && (
            <div>
              <h4 className="text-xs font-semibold text-warning uppercase tracking-wider mb-2">Warnings</h4>
              <ul className="space-y-1">
                {warnings.map((warning, idx) => (
                  <li key={idx} className="text-sm text-amber-700 flex items-start gap-2">
                    <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-amber-400 shrink-0"></span>
                    {warning}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
      
      {isSuccess && (
        <p className="text-sm text-emerald-700">All data points extracted and validated successfully.</p>
      )}
    </div>
  );
};
