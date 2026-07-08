import React, { useCallback } from 'react';
import { UploadCloud } from 'lucide-react';
import { cn } from '../lib/utils';

interface UploadZoneProps {
  onFileSelect: (file: File) => void;
  disabled?: boolean;
}

export const UploadZone: React.FC<UploadZoneProps> = ({ onFileSelect, disabled }) => {
  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (disabled) return;
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      onFileSelect(e.dataTransfer.files[0]);
    }
  }, [disabled, onFileSelect]);

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      onFileSelect(e.target.files[0]);
    }
  }, [onFileSelect]);

  return (
    <div
      onDragOver={(e) => e.preventDefault()}
      onDrop={handleDrop}
      className={cn(
        "border-2 border-dashed rounded-xl p-10 flex flex-col items-center justify-center transition-all bg-white",
        disabled ? "opacity-50 cursor-not-allowed border-gray-300" : "cursor-pointer border-primary/40 hover:border-primary hover:bg-blue-50/30"
      )}
    >
      <div className="w-16 h-16 bg-blue-50 rounded-full flex items-center justify-center mb-4">
        <UploadCloud className="w-8 h-8 text-primary" />
      </div>
      <h3 className="text-lg font-semibold text-gray-800 mb-2">Drag & Drop your document here</h3>
      <p className="text-gray-500 mb-6 text-sm text-center max-w-sm">
        Supports PDF, DOCX, and common image formats. Our AI will automatically extract the relevant data.
      </p>
      
      <label className={cn(
        "px-6 py-2.5 rounded-lg font-medium text-white shadow-sm transition-all",
        disabled ? "bg-gray-400 cursor-not-allowed" : "bg-primary hover:bg-blue-700 cursor-pointer hover:shadow"
      )}>
        Browse Files
        <input
          type="file"
          className="hidden"
          onChange={handleChange}
          disabled={disabled}
          accept=".pdf,.docx,.png,.jpg,.jpeg"
        />
      </label>
    </div>
  );
};
