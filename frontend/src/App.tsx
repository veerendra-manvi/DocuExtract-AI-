import { useState } from 'react';
import axios from 'axios';
import { Header } from './components/Header';
import { Footer } from './components/Footer';
import { UploadZone } from './components/UploadZone';
import { DocumentPreview } from './components/DocumentPreview';
import { ProcessingLoader } from './components/ProcessingLoader';
import { ExtractedJSONViewer } from './components/ExtractedJSONViewer';
import { ValidationCard } from './components/ValidationCard';
import { MetadataCard } from './components/MetadataCard';
import { DownloadButton } from './components/DownloadButton';
import { ErrorBoundary } from './components/ErrorBoundary';
import type { ExtractionResponse } from './types';

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<ExtractionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileSelect = async (selectedFile: File) => {
    if (isProcessing) return;
    
    setFile(selectedFile);
    setIsProcessing(true);
    setResult(null);
    setError(null);

    const formData = new FormData();
    formData.append('file', selectedFile);
    console.log("File appended to FormData:", formData.get("file"));

    try {
      console.log("Uploading...");
      const response = await axios.post<ExtractionResponse>('http://localhost:8000/extract', formData);
      console.log(response);

      if (response.data && response.data.success) {
        setResult(response.data);
      } else {
        setError("Failed to extract data. Missing success confirmation from server.");
      }
    } catch (err: any) {
      console.error(err);
      if (axios.isAxiosError(err) && err.response?.data) {
        const data = err.response.data;
        if (Array.isArray(data.detail)) {
           // Handle FastAPI RequestValidationError (e.g. missing fields)
           setError(`Error: ${data.detail.map((d: any) => `${d.loc.join('.')}: ${d.msg}`).join(', ')}`);
        } else if (data.message && typeof data.message === 'object' && data.message.error) {
           setError(`Error: ${data.message.error}`);
        } else if (data.detail && typeof data.detail === 'object' && data.detail.error) {
           setError(`Error: ${data.detail.error}`);
        } else if (data.message && typeof data.message === 'string') {
           setError(`Error: ${data.message}`);
        } else if (data.detail && typeof data.detail === 'string') {
           setError(`Error: ${data.detail}`);
        } else {
           setError("Failed to extract data. Please try again.");
        }
      } else if (err.message) {
        setError(`Error: ${err.message}`);
      } else {
        setError("Failed to extract data. Please check your connection.");
      }
    } finally {
      setIsProcessing(false);
    }
  };

  const handleClear = () => {
    setFile(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-background flex flex-col font-sans">
      <Header />
      
      <main className="flex-grow max-w-3xl mx-auto w-full px-4 py-12 space-y-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4 tracking-tight">Extract Data with AI Precision</h1>
          <p className="text-gray-500 max-w-xl mx-auto">
            Upload your documents and let our advanced AI models instantly extract, validate, and structure the data for you.
          </p>
        </div>

        {!file && !isProcessing && !result && (
          <UploadZone onFileSelect={handleFileSelect} disabled={isProcessing} />
        )}

        {file && (
          <DocumentPreview file={file} onClear={handleClear} disabled={isProcessing} />
        )}

        {isProcessing && <ProcessingLoader />}

        {error && (
          <div className="bg-red-50 text-red-700 p-4 rounded-xl border border-red-100 flex items-center justify-center">
            {error}
          </div>
        )}

        {result && result.success && !isProcessing && (
          <ErrorBoundary>
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500 ease-out">
              <ExtractedJSONViewer data={result.document} />
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <ValidationCard validation={result.validation} />
                <MetadataCard metadata={result.metadata} />
              </div>

              <div className="pt-4">
                <DownloadButton data={result.document} />
              </div>
            </div>
          </ErrorBoundary>
        )}
      </main>

      <Footer />
    </div>
  );
}

export default App;
