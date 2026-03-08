import './globals.css'

export const metadata = {
  title: 'सूचना सेतु AI | Government Schemes Platform',
  description: 'Discover 2,000+ government schemes tailored for you',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <header className="sticky top-0 bg-white/95 backdrop-blur-sm border-b border-slate-200 z-50">
          <div className="max-w-6xl mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <a href="/" className="text-xl font-bold text-slate-900">
                सूचना सेतु AI
              </a>
              
              <nav className="hidden md:flex items-center space-x-6">
                <a href="/" className="text-slate-700 hover:text-slate-900 transition-colors font-medium">Home</a>
                <a href="/schemes" className="text-slate-700 hover:text-slate-900 transition-colors font-medium">Schemes</a>
                <a href="/explainer" className="text-slate-700 hover:text-slate-900 transition-colors font-medium">Explainer</a>
                <a href="/voice" className="text-slate-700 hover:text-slate-900 transition-colors font-medium">Voice</a>
                <a href="/profile" className="text-slate-700 hover:text-slate-900 transition-colors font-medium">Profile</a>
                <a href="/schemes" className="bg-slate-900 text-white px-5 py-2 rounded-lg font-medium hover:bg-slate-800 transition-all">
                  Get Started
                </a>
              </nav>
              
              <button className="md:hidden text-slate-900">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
          </div>
        </header>
        
        <main>{children}</main>
        
        <footer className="bg-slate-900 text-white py-12">
          <div className="max-w-6xl mx-auto px-4">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
              <div>
                <div className="text-lg font-bold mb-3">सूचना सेतु AI</div>
                <p className="text-slate-400 text-sm">
                  Connecting Indians to government benefits
                </p>
              </div>
              
              <div>
                <h3 className="font-bold mb-3">Features</h3>
                <div className="space-y-2 text-sm">
                  <a href="/schemes" className="block text-slate-400 hover:text-white transition-colors">Scheme Finder</a>
                  <a href="/voice" className="block text-slate-400 hover:text-white transition-colors">Voice Assistant</a>
                  <a href="/explainer" className="block text-slate-400 hover:text-white transition-colors">Document Explainer</a>
                </div>
              </div>
              
              <div>
                <h3 className="font-bold mb-3">Resources</h3>
                <div className="space-y-2 text-sm">
                  <a href="https://india.gov.in" target="_blank" rel="noopener noreferrer" className="block text-slate-400 hover:text-white transition-colors">Government of India</a>
                  <a href="https://mygov.in" target="_blank" rel="noopener noreferrer" className="block text-slate-400 hover:text-white transition-colors">MyGov India</a>
                  <a href="https://digitalindia.gov.in" target="_blank" rel="noopener noreferrer" className="block text-slate-400 hover:text-white transition-colors">Digital India</a>
                </div>
              </div>
              
              <div>
                <h3 className="font-bold mb-3">Contact</h3>
                <div className="space-y-2 text-sm">
                  <div className="text-slate-400">Helpline: <span className="text-white font-medium">155261</span></div>
                  <div className="text-slate-400">USSD: <span className="text-white font-medium">*123#</span></div>
                </div>
              </div>
            </div>
            
            <div className="border-t border-slate-800 pt-6 flex flex-col md:flex-row justify-between items-center gap-4 text-sm">
              <p className="text-slate-400">
                © 2024 Soochna Setu AI | Team: <span className="text-white font-medium">THE CHOSEN ONES</span>
              </p>
              <div className="flex gap-3">
                <span className="text-slate-400 px-3 py-1 bg-slate-800 rounded-full text-xs">AWS Powered</span>
                <span className="text-slate-400 px-3 py-1 bg-slate-800 rounded-full text-xs">AI for Bharat</span>
              </div>
            </div>
          </div>
        </footer>
      </body>
    </html>
  )
}
