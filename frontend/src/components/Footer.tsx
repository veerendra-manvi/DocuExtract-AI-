import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-white border-t border-gray-200 mt-12">
      <div className="max-w-5xl mx-auto px-4 h-16 flex items-center justify-between text-sm text-gray-500">
        <p>&copy; {new Date().getFullYear()} DocuExtract AI. All rights reserved.</p>
        <div className="flex gap-4">
          <a href="#" className="hover:text-gray-900 transition-colors">Privacy</a>
          <a href="#" className="hover:text-gray-900 transition-colors">Terms</a>
        </div>
      </div>
    </footer>
  );
};
