import React from 'react';
import { FileText, X } from 'lucide-react';

interface DocumentPreviewProps {
  file: File;
  onClear: () => void;
  disabled?: boolean;
}

export const DocumentPreview: React.FC<DocumentPreviewProps> = ({ file, onClear, disabled }) => {
  const formatSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-4 flex items-center justify-between shadow-sm">
      <div className="flex items-center gap-4 overflow-hidden">
        <div className="w-12 h-12 bg-blue-50 text-primary rounded-lg flex items-center justify-center shrink-0">
          <FileText className="w-6 h-6" />
        </div>
        <div className="truncate">
          <p className="text-sm font-semibold text-gray-800 truncate">{file.name}</p>
          <p className="text-xs text-gray-500">{formatSize(file.size)}</p>
        </div>
      </div>
      <button
        onClick={onClear}
        disabled={disabled}
        className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        title="Remove file"
      >
        <X className="w-5 h-5" />
      </button>
    </div>
  );
};
