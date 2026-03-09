'use client'
import { useState } from 'react'
import { uploadDocument, askDocument } from '../../lib/api'

export default function ExplainerPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [explanation, setExplanation] = useState<any>(null)
  const [dragActive, setDragActive] = useState(false)
  const [chatMessages, setChatMessages] = useState<{role: string; text: string}[]>([])
  const [chatInput, setChatInput] = useState('')
  const [chatLoading, setChatLoading] = useState(false)

  const exampleDocs = [
    { 
      name: 'Union Budget 2024', 
      icon: '💰',
      summary: 'Key allocations and policy changes',
      size: '2.4 MB'
    },
    { 
      name: 'PM-KISAN Guidelines', 
      icon: '🌾',
      summary: 'Eligibility and application process',
      size: '1.8 MB'
    },
    { 
      name: 'National Health Policy', 
      icon: '🏥',
      summary: 'Healthcare initiatives and coverage',
      size: '3.1 MB'
    }
  ]

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0])
    }
  }

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0])
    }
  }

  const handleFile = (file: File) => {
    setSelectedFile(file)
    processDocument(file)
  }

  const processDocument = async (file: File) => {
    setIsProcessing(true)
    try {
      const result = await uploadDocument(file)
      setExplanation({
        title: file.name,
        summary: result.summary || 'Document processed successfully. The AI has extracted and analyzed the content.',
        keyPoints: [
          { icon: '📄', title: 'Pages', content: `${result.pageCount || 'N/A'} pages extracted` },
          { icon: '📝', title: 'Words', content: `${result.wordCount || 'N/A'} words analyzed` },
          { icon: '🔍', title: 'Method', content: `Processed via ${result.extractionMethod || 'AI OCR'}` },
          { icon: '✅', title: 'Confidence', content: `${((result.confidence || 0.85) * 100).toFixed(0)}% extraction confidence` },
        ],
        sections: [
          { title: 'AI Summary', content: result.summary || 'Processing complete.' },
        ],
        confidence: result.confidence || 0.85,
        documentId: result.documentId,
      })
    } catch (err: any) {
      console.error('Upload error:', err)
      alert(err.message || 'Could not connect to the backend. Please ensure the AWS Lambda service is active.')
    } finally {
      setIsProcessing(false)
    }
  }

  const handleExampleDoc = (doc: any) => {
    const mockFile = new File([''], doc.name, { type: 'application/pdf' })
    handleFile(mockFile)
  }

  if (isProcessing) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-gray-200 border-t-navy rounded-full animate-spin mx-auto mb-6"></div>
          <h2 className="text-2xl font-light text-navy mb-4">Analyzing document...</h2>
          <div className="space-y-2 text-sm text-gray-600">
            <p>Extracting text from PDF</p>
            <p>Identifying key sections</p>
            <p>Simplifying language</p>
          </div>
        </div>
      </div>
    )
  }

  if (explanation) {
    return (
      <div className="min-h-screen bg-white py-12 px-4">
        <div className="max-w-5xl mx-auto">
          <button
            onClick={() => { setExplanation(null); setSelectedFile(null); }}
            className="mb-8 text-navy hover:text-gray-700 font-light flex items-center gap-2 transition-colors"
          >
            ← Upload Another Document
          </button>

          <div className="mb-12">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h1 className="text-5xl font-light text-navy mb-2">{explanation.title}</h1>
                <p className="text-gray-600">Simplified explanation in plain language</p>
              </div>
              <div className="text-right">
                <div className="text-sm text-gray-600 mb-1">Confidence</div>
                <div className="text-3xl font-light text-navy">{(explanation.confidence * 100).toFixed(0)}%</div>
              </div>
            </div>
          </div>

          {/* Summary */}
          <div className="card-clean mb-8">
            <h2 className="text-2xl font-light text-navy mb-4">Summary</h2>
            <p className="text-lg text-gray-700 leading-relaxed">{explanation.summary}</p>
          </div>

          {/* Key Points */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            {explanation.keyPoints.map((point: any, idx: number) => (
              <div key={idx} className="card-clean">
                <div className="text-4xl mb-3">{point.icon}</div>
                <h3 className="text-xl font-medium text-navy mb-2">{point.title}</h3>
                <p className="text-gray-700">{point.content}</p>
              </div>
            ))}
          </div>

          {/* Detailed Sections */}
          <div className="space-y-6 mb-8">
            {explanation.sections.map((section: any, idx: number) => (
              <div key={idx} className="card-clean">
                <h3 className="text-2xl font-light text-navy mb-4">{section.title}</h3>
                <p className="text-lg text-gray-700 leading-relaxed">{section.content}</p>
              </div>
            ))}
          </div>

          {/* Document Q&A Chat */}
          {explanation.documentId && (
            <div className="card-clean mb-8">
              <h2 className="text-2xl font-light text-navy mb-4">💬 Ask Questions About This Document</h2>
              <div className="space-y-4 mb-6 max-h-96 overflow-y-auto">
                {chatMessages.length === 0 && (
                  <div className="text-center py-6">
                    <p className="text-gray-500 mb-4">Ask anything about this document</p>
                    <div className="flex flex-wrap gap-2 justify-center">
                      {[
                        'What is this document about?',
                        'What are the key points?',
                        'Who benefits from this?',
                        'What are the eligibility criteria?',
                      ].map((q, i) => (
                        <button
                          key={i}
                          onClick={() => { setChatInput(q); }}
                          className="text-sm px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-full transition-colors"
                        >
                          {q}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
                {chatMessages.map((msg, idx) => (
                  <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[80%] px-4 py-3 rounded-2xl ${
                      msg.role === 'user'
                        ? 'bg-slate-900 text-white rounded-br-md'
                        : 'bg-slate-100 text-slate-800 rounded-bl-md'
                    }`}>
                      {msg.role !== 'user' && <p className="text-xs text-slate-500 mb-1">🤖 Soochna Setu AI</p>}
                      <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.text}</p>
                    </div>
                  </div>
                ))}
                {chatLoading && (
                  <div className="flex justify-start">
                    <div className="bg-slate-100 text-slate-600 px-4 py-3 rounded-2xl rounded-bl-md">
                      <p className="text-sm animate-pulse">Thinking...</p>
                    </div>
                  </div>
                )}
              </div>
              <form
                onSubmit={async (e) => {
                  e.preventDefault()
                  if (!chatInput.trim() || chatLoading) return
                  const question = chatInput.trim()
                  setChatInput('')
                  setChatMessages(msgs => [...msgs, { role: 'user', text: question }])
                  setChatLoading(true)
                  try {
                    const result = await askDocument(explanation.documentId, question)
                    setChatMessages(msgs => [...msgs, {
                      role: 'assistant',
                      text: result.answer || result.response || 'Sorry, I could not find an answer in this document.',
                    }])
                  } catch {
                    setChatMessages(msgs => [...msgs, {
                      role: 'assistant',
                      text: 'Could not connect to the backend AWS Lambda service. Please try again.',
                    }])
                  } finally {
                    setChatLoading(false)
                  }
                }}
                className="flex gap-3"
              >
                <input
                  type="text"
                  value={chatInput}
                  onChange={e => setChatInput(e.target.value)}
                  placeholder="Ask a question about this document..."
                  className="flex-1 px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-slate-900 focus:border-transparent outline-none"
                />
                <button
                  type="submit"
                  disabled={chatLoading || !chatInput.trim()}
                  className="btn-primary disabled:opacity-50"
                >
                  Ask →
                </button>
              </form>
            </div>
          )}

          {/* Actions */}
          <div className="flex flex-wrap gap-4">
            <button className="btn-primary">
              Download Summary
            </button>
            <button className="btn-secondary">
              Share
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-white py-12 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl md:text-6xl font-light text-navy mb-4">
            Document Explainer
          </h1>
          <p className="text-xl text-gray-600 font-light">Upload any government document for simple explanations</p>
        </div>

        {/* Upload Area */}
        <div 
          className={`card-clean text-center mb-8 transition-all duration-300 ${
            dragActive ? 'border-navy border-2' : ''
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <div className="py-12">
            <div className="text-7xl mb-6">📄</div>
            <h3 className="text-2xl font-light text-navy mb-3">
              Drop your PDF here
            </h3>
            <p className="text-gray-600 mb-8">or click to browse</p>
            <input
              type="file"
              accept=".pdf"
              onChange={handleFileInput}
              className="hidden"
              id="file-upload"
            />
            <label htmlFor="file-upload">
              <span className="btn-primary cursor-pointer inline-block">
                Choose File
              </span>
            </label>
            <p className="text-sm text-gray-500 mt-6">Supported: PDF files up to 50MB</p>
          </div>
        </div>

        {/* Example Documents */}
        <div className="card-clean">
          <h3 className="text-2xl font-light text-navy mb-6">Try with example documents</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {exampleDocs.map((doc, idx) => (
              <button
                key={idx}
                onClick={() => handleExampleDoc(doc)}
                className="bg-gray-50 hover:bg-gray-100 border border-gray-200 rounded-xl p-6 transition-all text-left"
              >
                <div className="text-5xl mb-4">{doc.icon}</div>
                <h4 className="font-medium text-navy text-lg mb-2">{doc.name}</h4>
                <p className="text-sm text-gray-600 mb-3">{doc.summary}</p>
                <p className="text-xs text-gray-500">{doc.size}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
          {[
            { icon: '🤖', title: 'AI-Powered', desc: 'Advanced NLP analysis' },
            { icon: '📖', title: 'Simple Language', desc: 'Grade-5 reading level' },
            { icon: '⚡', title: 'Fast', desc: 'Results in seconds' }
          ].map((feature, idx) => (
            <div key={idx} className="card-clean text-center">
              <div className="text-5xl mb-3">{feature.icon}</div>
              <h4 className="text-lg font-medium text-navy mb-2">{feature.title}</h4>
              <p className="text-gray-600 text-sm">{feature.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
