'use client'

export default function Home() {
  return (
    <div className="bg-slate-50">
      {/* Hero Section */}
      <section className="section bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <div className="badge mb-6 inline-flex">
              <span className="w-2 h-2 bg-slate-900 rounded-full"></span>
              <span>Government of India</span>
            </div>
            
            <h1 className="text-5xl md:text-7xl font-bold mb-6 text-slate-900">
              सूचना सेतु AI
            </h1>
            
            <p className="text-xl md:text-2xl text-slate-600 mb-10 max-w-3xl mx-auto">
              Discover government schemes tailored for you.
              <br />
              Simple, accurate, and accessible to all.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a href="/schemes" className="btn-primary text-lg">
                Find Your Schemes →
              </a>
              <a href="/voice" className="btn-secondary text-lg">
                Voice Assistant
              </a>
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-8 max-w-3xl mx-auto mt-16">
            <div className="text-center">
              <div className="text-3xl font-bold text-slate-900 mb-1">850M+</div>
              <div className="text-sm text-slate-600">Citizens</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-slate-900 mb-1">2,000+</div>
              <div className="text-sm text-slate-600">Schemes</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-slate-900 mb-1">12</div>
              <div className="text-sm text-slate-600">Languages</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="section">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="section-title">Three Simple Tools</h2>
            <p className="section-subtitle">Everything you need in one place</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              {
                icon: '🔍',
                title: 'Scheme Finder',
                desc: 'Answer 4 questions to find schemes you qualify for',
                link: '/schemes'
              },
              {
                icon: '🎤',
                title: 'Voice Assistant',
                desc: 'Ask questions in English or Hindi, get instant answers',
                link: '/voice'
              },
              {
                icon: '📄',
                title: 'Document Explainer',
                desc: 'Upload PDFs and get simple explanations',
                link: '/explainer'
              }
            ].map((feature, idx) => (
              <a key={idx} href={feature.link} className="card group cursor-pointer">
                <div className="text-5xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-bold text-slate-900 mb-2 group-hover:text-slate-700 transition-colors">
                  {feature.title}
                </h3>
                <p className="text-slate-600 mb-4">{feature.desc}</p>
                <div className="text-slate-900 font-medium group-hover:translate-x-1 transition-transform inline-flex items-center gap-1">
                  Learn more <span>→</span>
                </div>
              </a>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="section bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="section-title">How It Works</h2>
            <p className="section-subtitle">Four simple steps</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            {[
              { step: '1', title: 'Share Profile', desc: 'Tell us about yourself' },
              { step: '2', title: 'AI Analysis', desc: 'We match you with schemes' },
              { step: '3', title: 'Get Results', desc: 'View recommendations' },
              { step: '4', title: 'Apply Online', desc: 'Direct links to portals' }
            ].map((item, idx) => (
              <div key={idx} className="text-center">
                <div className="w-12 h-12 bg-slate-900 text-white rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
                  {item.step}
                </div>
                <h3 className="text-lg font-bold text-slate-900 mb-2">{item.title}</h3>
                <p className="text-slate-600 text-sm">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Trust */}
      <section className="section">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="section-title">Why Trust Us</h2>
            <p className="section-subtitle">Built on transparency and accuracy</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {[
              {
                icon: '📚',
                title: 'Official Sources',
                desc: 'All data from government portals'
              },
              {
                icon: '🔒',
                title: 'Secure & Private',
                desc: 'Your data is never stored'
              },
              {
                icon: '✓',
                title: 'Verified Data',
                desc: 'Cross-checked with multiple sources'
              },
              {
                icon: '🌐',
                title: 'Accessible',
                desc: 'Works on 2G, 12 languages, free'
              }
            ].map((item, idx) => (
              <div key={idx} className="card flex gap-4">
                <div className="text-4xl flex-shrink-0">{item.icon}</div>
                <div>
                  <h3 className="text-lg font-bold text-slate-900 mb-2">{item.title}</h3>
                  <p className="text-slate-600">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="section bg-slate-900 text-white">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Ready to Get Started?
          </h2>
          <p className="text-xl mb-10 text-slate-300">
            Join thousands finding schemes they never knew existed
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a href="/schemes" className="bg-white text-slate-900 font-medium px-8 py-4 rounded-xl hover:bg-slate-100 transition-all text-lg">
              Start Now - It's Free
            </a>
            <a href="/voice" className="bg-slate-800 text-white font-medium px-8 py-4 rounded-xl hover:bg-slate-700 transition-all text-lg border border-slate-700">
              Try Voice Assistant
            </a>
          </div>
          <p className="text-sm text-slate-400 mt-6">
            No registration • 100% free • Works on any device
          </p>
        </div>
      </section>
    </div>
  )
}
