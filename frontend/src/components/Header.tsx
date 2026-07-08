import React from 'react';
import { BrainCircuit } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <header className="bg-white border-b border-gray-200">
      <div className="max-w-5xl mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center gap-2 text-primary">
          <BrainCircuit className="w-8 h-8" />
          <span className="text-xl font-bold text-gray-900 tracking-tight">DocuExtract <span className="text-primary">AI</span></span>
        </div>
        <nav>
          <a href="#" className="text-sm font-medium text-gray-500 hover:text-gray-900 transition-colors">Documentation</a>
        </nav>
      </div>
    </header>
  );
};
