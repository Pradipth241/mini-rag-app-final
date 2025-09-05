// Full Path: C:\Users\pradi\mini-rag-app\frontend\app\page.tsx
'use client';

import { useState } from 'react';

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [documentText, setDocumentText] = useState('');
  const [query, setQuery] = useState('');
  const [answer, setAnswer] = useState('');
  const [sources, setSources] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState('');

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setSelectedFile(event.target.files[0]);
      setDocumentText('');
    }
  };

  const handleTextChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
      setDocumentText(event.target.value);
      setSelectedFile(null);
  }

  const handleProcess = async () => {
    setIsLoading(true);
    setStatusMessage('Processing document...');

    let endpoint = '';
    let body: FormData | string = '';
    let headers: HeadersInit = {};

    if (selectedFile) {
        endpoint = `${API_URL}/process-text`;
        const formData = new FormData();
        formData.append('file', selectedFile);
        body = formData;
    } else if (documentText.trim()) {
        endpoint = `${API_URL}/process-text-input`;
        body = JSON.stringify({ text: documentText });
        headers = { 'Content-Type': 'application/json' };
    } else {
        alert('Please select a file or paste some text.');
        setIsLoading(false);
        return;
    }

    try {
      const response = await fetch(endpoint, { method: 'POST', body, headers });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Failed to process document');
      setStatusMessage('Document processed successfully! You can now ask a question.');
    } catch (error) {
       if (error instanceof Error) setStatusMessage(`Error: ${error.message}`);
       else setStatusMessage('An unknown error occurred.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuery = async () => {
    if (!query.trim()) {
      alert('Please enter a query.');
      return;
    }
    setIsLoading(true);
    setAnswer('');
    setSources([]);
    setStatusMessage('Thinking...');
    try {
      const response = await fetch(`${API_URL}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: query }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Failed to get answer');
      setAnswer(data.result.answer);
      setSources(data.result.sources);
      setStatusMessage('');
    } catch (error) {
       if (error instanceof Error) setStatusMessage(`Error: ${error.message}`);
       else setStatusMessage('An unknown error occurred.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main style={{ fontFamily: 'sans-serif', padding: '2rem', maxWidth: '800px', margin: 'auto' }}>
      <h1 style={{ textAlign: 'center' }}>Mini RAG Application</h1>

      <div style={{ marginBottom: '2rem', padding: '1rem', border: '1px solid #ccc', borderRadius: '8px' }}>
        <h2>Step 1: Process a Document</h2>

        <div style={{marginBottom: '1rem'}}>
            <p><strong>Option A:</strong> Upload a .txt or .pdf file.</p>
            <input type="file" accept=".txt,.pdf" onChange={handleFileChange} style={{ display: 'block' }}/>
        </div>

        <p style={{textAlign: 'center', fontWeight: 'bold'}}>OR</p>

        <div style={{marginTop: '1rem'}}>
            <p><strong>Option B:</strong> Paste text directly.</p>
            <textarea
              value={documentText}
              onChange={handleTextChange}
              placeholder="Paste the full text of a document here..."
              style={{ width: '100%', minHeight: '150px', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
            />
        </div>

        <button onClick={handleProcess} disabled={isLoading} style={{ marginTop: '1rem', padding: '10px 15px', cursor: 'pointer', width: '100%' }}>
          {isLoading ? 'Processing...' : 'Process Document'}
        </button>
      </div>

      <div style={{ marginBottom: '2rem', padding: '1rem', border: '1px solid #ccc', borderRadius: '8px' }}>
        <h2>Step 2: Ask a Question</h2>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a question about the document..."
          style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
        />
        <button onClick={handleQuery} disabled={isLoading} style={{ marginTop: '0.5rem', padding: '10px 15px', cursor: 'pointer' }}>
          {isLoading ? 'Thinking...' : 'Ask Question'}
        </button>
      </div>

      {statusMessage && <p style={{ textAlign: 'center', fontStyle: 'italic', color: '#282e73ff' }}>{statusMessage}</p>}

      {answer && (
        <div style={{ padding: '1rem', border: '1px solid #ccc', borderRadius: '8px', background: '#2a6d5bff' }}>
          <h2>Answer</h2>
          <p style={{ whiteSpace: 'pre-wrap', lineHeight: '1.6' }}>{answer}</p>
          {sources.length > 0 && (
            <div>
              <h3>Sources:</h3>
              {sources.map((source, index) => (
                <div key={index} style={{ borderLeft: '3px solid #ccc', paddingLeft: '1rem', margin: '1rem 0', fontStyle: 'italic', fontSize: '0.9em' }}>
                  <p>{source}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </main>
  );
}