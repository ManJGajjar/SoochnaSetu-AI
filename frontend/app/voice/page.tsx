'use client'
import { useState } from 'react'
import { sendChatMessage } from '../../lib/api'

export default function VoicePage() {
  const [isListening, setIsListening] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [response, setResponse] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)
  const [language, setLanguage] = useState<'en' | 'hi'>('en')
  const [textInput, setTextInput] = useState('')

  const handleTextSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!textInput.trim() || isProcessing) return
    handleVoiceInput(textInput.trim())
    setTextInput('')
  }

  const sampleQuestions = [
    { en: 'What schemes can I get?', hi: 'मुझे कौन सी योजनाएं मिल सकती हैं?' },
    { en: 'How to apply for PM-KISAN?', hi: 'PM-KISAN के लिए कैसे apply करें?' },
    { en: 'What is Ayushman Bharat?', hi: 'आयुष्मान भारत क्या है?' },
    { en: 'Student scholarships available?', hi: 'छात्रों के लिए छात्रवृत्ति?' }
  ]

  const handleVoiceInput = async (question: string) => {
    setTranscript(question)
    setIsProcessing(true)
    setResponse('')
    try {
      const result = await sendChatMessage(question, language)
      setResponse(result.response || 'Sorry, I could not process your request.')
    } catch (err) {
      console.error('Chat error:', err)
      setResponse('Could not connect to the backend AWS Lambda service.')
    } finally {
      setIsProcessing(false)
    }
  }

  const startListening = () => {
    setIsListening(true)
    setTimeout(() => {
      const randomQuestion = sampleQuestions[Math.floor(Math.random() * sampleQuestions.length)]
      handleVoiceInput(language === 'hi' ? randomQuestion.hi : randomQuestion.en)
      setIsListening(false)
    }, 2000)
  }

  return (
    <div className="min-h-screen bg-white py-12 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl md:text-6xl font-light text-navy mb-4">
            Voice Assistant
          </h1>
          <p className="text-xl text-gray-600 font-light">Ask questions in English or Hindi</p>
        </div>

        {/* Language Toggle */}
        <div className="flex justify-center gap-4 mb-12">
          <button
            onClick={() => setLanguage('en')}
            className={`px-6 py-3 rounded-full font-medium transition-all ${language === 'en'
                ? 'bg-navy text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
          >
            English
          </button>
          <button
            onClick={() => setLanguage('hi')}
            className={`px-6 py-3 rounded-full font-medium transition-all ${language === 'hi'
                ? 'bg-navy text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
          >
            हिंदी
          </button>
        </div>

        {/* Input Area */}
        <div className="card-clean text-center mb-8">
          <button
            onClick={startListening}
            disabled={isListening || isProcessing}
            className={`w-32 h-32 rounded-full mx-auto flex items-center justify-center text-7xl transition-all duration-300 ${isListening
                ? 'bg-red-500 text-white'
                : isProcessing
                  ? 'bg-gray-300 text-gray-600'
                  : 'bg-navy text-white hover:bg-gray-800'
              } disabled:opacity-50 disabled:cursor-not-allowed`}
          >
            {isListening ? '🎙️' : isProcessing ? '⏳' : '🎤'}
          </button>
          <p className="mt-4 mb-6 text-xl font-light text-navy">
            {isListening ? 'Listening...' : isProcessing ? 'Processing...' : 'Tap to speak'}
          </p>

          <div className="relative max-w-xl mx-auto flex items-center gap-2">
            <div className="flex-1 border-t border-gray-200"></div>
            <span className="text-gray-400 text-sm font-medium uppercase px-2">OR</span>
            <div className="flex-1 border-t border-gray-200"></div>
          </div>

          <form onSubmit={handleTextSubmit} className="mt-6 flex max-w-2xl mx-auto gap-3">
            <input
              type="text"
              value={textInput}
              onChange={e => setTextInput(e.target.value)}
              placeholder={language === 'hi' ? "अपना सवाल यहाँ टाइप करें..." : "Type your question here..."}
              disabled={isProcessing}
              className="flex-1 px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-slate-900 focus:border-transparent outline-none disabled:opacity-50"
            />
            <button
              type="submit"
              disabled={isProcessing || !textInput.trim()}
              className="btn-primary disabled:opacity-50 px-8"
            >
              Ask →
            </button>
          </form>
        </div>

        {/* Transcript */}
        {transcript && (
          <div className="card-clean mb-6">
            <p className="text-sm text-gray-600 mb-2">You asked:</p>
            <p className="text-lg text-navy">{transcript}</p>
          </div>
        )}

        {/* Response */}
        {response && (
          <div className="card-clean mb-8">
            <div className="flex items-start gap-4">
              <div className="text-4xl">🤖</div>
              <div className="flex-1">
                <p className="text-sm text-gray-600 mb-3">Soochna Setu AI:</p>
                <p className="text-lg text-gray-700 leading-relaxed mb-6">{response}</p>
                <div className="flex gap-3">
                  <button className="btn-primary">
                    View Details
                  </button>
                  <button className="btn-secondary">
                    Ask Another
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Quick Questions */}
        <div className="card-clean">
          <h3 className="text-2xl font-light text-navy mb-6">Quick Questions</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {sampleQuestions.map((q, idx) => (
              <button
                key={idx}
                onClick={() => handleVoiceInput(language === 'hi' ? q.hi : q.en)}
                disabled={isProcessing || isListening}
                className="px-6 py-4 bg-gray-50 hover:bg-gray-100 border border-gray-200 rounded-xl text-left transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <p className="font-medium text-navy">{language === 'hi' ? q.hi : q.en}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
          {[
            { icon: '🌐', title: 'Multilingual', desc: 'English & Hindi support' },
            { icon: '⚡', title: 'Instant', desc: 'Real-time responses' },
            { icon: '🎯', title: 'Accurate', desc: 'Official data only' }
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
