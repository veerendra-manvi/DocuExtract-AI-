import React from 'react';
import { Database } from 'lucide-react';

interface ExtractedJSONViewerProps {
  data: any;
}

export const ExtractedJSONViewer: React.FC<ExtractedJSONViewerProps> = ({ data }) => {
  return (
    <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden flex flex-col">
      <div className="bg-gray-50 border-b border-gray-200 px-4 py-3 flex items-center gap-2">
        <Database className="w-5 h-5 text-gray-500" />
        <h3 className="font-semibold text-gray-800 text-sm">Extracted Results</h3>
      </div>
      <div className="p-0 overflow-auto max-h-[500px]">
        <pre className="p-4 text-sm text-gray-800 font-mono">
          {JSON.stringify(data, null, 2)}
        </pre>
      </div>
    </div>
  );
};
