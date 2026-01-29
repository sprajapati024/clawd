async function getSchedules() {
  const res = await fetch(
    'https://raw.githubusercontent.com/sprajapati024/clawd/master/CRON.json',
    { next: { revalidate: 60 } }
  )
  if (!res.ok) return null
  return res.json()
}

function ScheduleCard({ job }) {
  return (
    <div style={{
      backgroundColor: '#1a1a1a',
      border: job.enabled ? '2px solid #10b981' : '2px solid #6b7280',
      borderRadius: '8px',
      padding: '16px',
      marginBottom: '12px',
      opacity: job.enabled ? 1 : 0.6
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '8px' }}>
        <h3 style={{ margin: 0, fontSize: '16px', fontWeight: 'bold' }}>
          {job.name}
        </h3>
        <span style={{
          backgroundColor: job.enabled ? '#10b981' : '#6b7280',
          color: '#fff',
          padding: '2px 8px',
          borderRadius: '12px',
          fontSize: '11px',
          fontWeight: 'bold'
        }}>
          {job.enabled ? 'ACTIVE' : 'DISABLED'}
        </span>
      </div>
      <p style={{ margin: '0 0 12px 0', fontSize: '14px', color: '#a0a0a0' }}>
        {job.description}
      </p>
      <div style={{ fontSize: '12px', color: '#707070' }}>
        <div>⏰ {job.nextRun}</div>
        <div style={{ marginTop: '4px', fontFamily: 'monospace', color: '#888' }}>
          {job.schedule}
        </div>
      </div>
    </div>
  )
}

export default async function Schedules() {
  const data = await getSchedules()

  if (!data) {
    return (
      <main style={{ padding: '40px', maxWidth: '1200px', margin: '0 auto' }}>
        <h1>Failed to load schedules</h1>
      </main>
    )
  }

  const { jobs, meta } = data

  // Group jobs by frequency
  const daily = jobs.filter(j => j.nextRun.includes('Daily'))
  const weekly = jobs.filter(j => j.nextRun.includes('Sunday') || j.nextRun.includes('Weekly'))
  const monthly = jobs.filter(j => j.nextRun.includes('Monthly') || j.nextRun.includes('27') || j.nextRun.includes('Jan 31'))

  return (
    <main style={{ padding: '40px', maxWidth: '1400px', margin: '0 auto' }}>
      <div style={{ marginBottom: '40px' }}>
        <h1 style={{ fontSize: '32px', margin: '0 0 16px 0' }}>
          👓 Clarke's Dashboard
        </h1>
        <div style={{ display: 'flex', gap: '16px', marginBottom: '16px' }}>
          <a href="/" style={{
            padding: '8px 16px',
            backgroundColor: '#1a1a1a',
            color: '#fff',
            textDecoration: 'none',
            borderRadius: '6px',
            border: '1px solid #333'
          }}>
            📋 Tasks
          </a>
          <a href="/schedules" style={{
            padding: '8px 16px',
            backgroundColor: '#3b82f6',
            color: '#fff',
            textDecoration: 'none',
            borderRadius: '6px',
            fontWeight: 'bold'
          }}>
            ⏰ Schedules
          </a>
        </div>
        <p style={{ color: '#707070', margin: 0 }}>
          Last updated: {new Date(meta.lastUpdated).toLocaleString()}
        </p>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
        gap: '24px'
      }}>
        <div>
          <h2 style={{ fontSize: '20px', marginBottom: '16px', color: '#10b981' }}>
            📅 Daily ({daily.length})
          </h2>
          {daily.map(job => (
            <ScheduleCard key={job.name} job={job} />
          ))}
        </div>

        <div>
          <h2 style={{ fontSize: '20px', marginBottom: '16px', color: '#8b5cf6' }}>
            📆 Weekly ({weekly.length})
          </h2>
          {weekly.map(job => (
            <ScheduleCard key={job.name} job={job} />
          ))}
        </div>

        <div>
          <h2 style={{ fontSize: '20px', marginBottom: '16px', color: '#f59e0b' }}>
            📆 Monthly ({monthly.length})
          </h2>
          {monthly.map(job => (
            <ScheduleCard key={job.name} job={job} />
          ))}
        </div>
      </div>
    </main>
  )
}
