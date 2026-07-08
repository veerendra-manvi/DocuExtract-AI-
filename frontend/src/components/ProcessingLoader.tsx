import React from 'react';
import { Loader2 } from 'lucide-react';

export const ProcessingLoader: React.FC = () => {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-8 flex flex-col items-center justify-center shadow-sm py-12">
      <Loader2 className="w-12 h-12 text-primary animate-spin mb-4" />
      <h3 className="text-lg font-semibold text-gray-900 mb-2">Analyzing Document...</h3>
      <p className="text-gray-500 text-sm text-center max-w-sm">
        Our AI is reading and extracting the structured information from your document. This usually takes just a few seconds.
      </p>
      
      <div className="w-64 h-1.5 bg-gray-100 rounded-full mt-6 overflow-hidden">
        <div className="h-full bg-primary rounded-full w-full animate-[pulse_1.5s_ease-in-out_infinite] origin-left" style={{ animation: 'progress 2s ease-in-out infinite' }}></div>
      </div>
      <style>{`
        @keyframes progress {
          0% { transform: scaleX(0); transform-origin: left; }
          50% { transform: scaleX(1); transform-origin: left; }
          50.1% { transform: scaleX(1); transform-origin: right; }
          100% { transform: scaleX(0); transform-origin: right; }
        }
      `}</style>
    </div>
  );
};
