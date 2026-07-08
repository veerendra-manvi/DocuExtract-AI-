import React from 'react';
import { Download } from 'lucide-react';

interface DownloadButtonProps {
  data: any;
  filename?: string;
}

export const DownloadButton: React.FC<DownloadButtonProps> = ({ data, filename = 'extracted_data.json' }) => {
  const handleDownload = () => {
    const jsonString = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <button
      onClick={handleDownload}
      className="flex items-center justify-center gap-2 w-full bg-gray-900 hover:bg-gray-800 text-white font-medium py-3 px-4 rounded-xl transition-colors shadow-sm"
    >
      <Download className="w-5 h-5" />
      Download JSON
    </button>
  );
};
