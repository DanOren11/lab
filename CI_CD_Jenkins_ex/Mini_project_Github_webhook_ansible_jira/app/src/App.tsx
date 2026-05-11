import { useState } from 'react'
import './App.css'

const PIPELINE_STEPS = [
  { label: 'Push to Dev',      desc: 'Code pushed to develop branch'        },
  { label: 'CI Build',         desc: 'Docker image built and tagged with SHA' },
  { label: 'Push to Registry', desc: 'Image pushed to Docker Hub'            },
  { label: 'Open PR',          desc: 'Automated PR created to main'          },
  { label: 'CD Deploy',        desc: 'Container stopped and restarted'       },
]

const STACK = ['Jenkins', 'Docker', 'GitHub', 'React', 'Node 22']

export default function App() {
  const [active, setActive] = useState<number | null>(null)

  return (
    <div className="page">

      <header className="hero">
        <div className="badge">CI / CD</div>
        <h1>Mini Project Pipeline</h1>
        <p className="subtitle">
          GitHub Webhooks · Jenkins · Docker · Jira
        </p>
        <div className="stack-row">
          {STACK.map(s => (
            <span key={s} className="chip">{s}</span>
          ))}
        </div>
      </header>

      <section className="section">
        <h2>Pipeline Flow</h2>
        <p className="section-sub">Click a step to learn more</p>
        <div className="steps">
          {PIPELINE_STEPS.map((step, i) => (
            <>
              <button
                key={step.label}
                className={`step ${active === i ? 'step--active' : ''}`}
                onClick={() => setActive(active === i ? null : i)}
              >
                <span className="step-num">{i + 1}</span>
                <span className="step-label">{step.label}</span>
                {active === i && (
                  <span className="step-desc">{step.desc}</span>
                )}
              </button>
              {i < PIPELINE_STEPS.length - 1 && (
                <span key={`arrow-${i}`} className="arrow">→</span>
              )}
            </>
          ))}
        </div>
      </section>

      <section className="section">
        <h2>Architecture</h2>
        <p className="section-sub">3-server setup running on Docker</p>
        <div className="cards">
          <div className="card">
            <h3>Jenkins Master</h3>
            <p>Manages pipelines and automation</p>
            <span className="port">:8080</span>
          </div>
          <div className="card">
            <h3>Application Slave</h3>
            <p>Runs CD pipeline and hosts the app container</p>
            <span className="port">:3000</span>
          </div>
          <div className="card">
            <h3>Infrastructure Slave</h3>
            <p>Runs CI pipeline, builds and pushes images </p>
            <span className="port">Docker Hub</span>
          </div>
        </div>
      </section>

      <section className="section diagram-section">
        <h2>Architecture Diagram</h2>
        <p className="section-sub">Full CI/CD flow with all components and ports</p>
        <div className="diagram-wrapper">
          <img
            src="/UpdatedMiniProject.drawio.svg"
            alt="CI/CD Architecture Diagram"
            className="architecture-diagram"
          />
        </div>
      </section>

      <footer className="footer">
        <p>Built by <strong>Dan Oren</strong> · Deployed via Jenkins CD</p>
      </footer>

    </div>
  )
}
