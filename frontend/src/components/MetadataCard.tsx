import React from 'react';
import { Info, Clock, FileType, Hash } from 'lucide-react';
import type { ExtractionMetadata } from '../types';

interface MetadataCardProps {
  metadata: ExtractionMetadata;
}

export const MetadataCard: React.FC<MetadataCardProps> = ({ metadata }) => {
  if (!metadata) return null;

  const filename = metadata?.filename ?? "Unknown";
  const processingTime = metadata?.pipeline_time_sec ?? 0;
  const aiModel = metadata?.ai_metadata?.model ?? "Unknown";
  const wordCount = metadata?.ai_metadata?.usage?.total_tokens ?? "N/A";

  return (
    <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
      <div className="bg-gray-50 border-b border-gray-200 px-4 py-3 flex items-center gap-2">
        <Info className="w-5 h-5 text-gray-500" />
        <h3 className="font-semibold text-gray-800 text-sm">Processing Metadata</h3>
      </div>
      <div className="p-4 grid grid-cols-2 gap-4">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded bg-blue-50 flex items-center justify-center text-primary">
            <FileType className="w-4 h-4" />
          </div>
          <div>
            <p className="text-xs text-gray-500 font-medium">Filename</p>
            <p className="text-sm font-semibold text-gray-900 truncate max-w-[100px]" title={filename}>{filename}</p>
          </div>
        </div>
        
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded bg-blue-50 flex items-center justify-center text-primary">
            <Hash className="w-4 h-4" />
          </div>
          <div>
            <p className="text-xs text-gray-500 font-medium">Tokens Used</p>
            <p className="text-sm font-semibold text-gray-900">{wordCount}</p>
          </div>
        </div>
        
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded bg-blue-50 flex items-center justify-center text-primary">
            <Clock className="w-4 h-4" />
          </div>
          <div>
            <p className="text-xs text-gray-500 font-medium">Processing Time</p>
            <p className="text-sm font-semibold text-gray-900">{typeof processingTime === 'number' ? processingTime.toFixed(2) : "0.00"}s</p>
          </div>
        </div>
        
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded bg-blue-50 flex items-center justify-center text-primary">
            <Info className="w-4 h-4" />
          </div>
          <div>
            <p className="text-xs text-gray-500 font-medium">Model</p>
            <p className="text-sm font-semibold text-gray-900 truncate max-w-[100px]" title={aiModel}>{aiModel}</p>
          </div>
        </div>
      </div>
    </div>
  );
};
