async function getTasks() {
  const res = await fetch(
    'https://raw.githubusercontent.com/sprajapati024/clawd/master/TASKS.json',
    { next: { revalidate: 60 } }
  )
  if (!res.ok) return null
  return res.json()
}

function TaskCard({ task, status }) {
  const statusColors = {
    in_progress: '#3b82f6',
    planned: '#8b5cf6',
    completed: '#10b981',
    backburner: '#6b7280'
  }

  const priorityEmoji = {
    high: '🔴',
    medium: '🟡',
    low: '🟢'
  }

  return (
    <div style={{
      backgroundColor: '#1a1a1a',
      border: `2px solid ${statusColors[status]}`,
      borderRadius: '8px',
      padding: '16px',
      marginBottom: '12px'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
        <h3 style={{ margin: '0 0 8px 0', fontSize: '16px' }}>
          {task.priority && priorityEmoji[task.priority]} {task.title}
        </h3>
        {task.status && (
          <span style={{
            backgroundColor: statusColors[status],
            color: '#fff',
            padding: '2px 8px',
            borderRadius: '12px',
            fontSize: '11px',
            fontWeight: 'bold'
          }}>
            {task.status.toUpperCase()}
          </span>
        )}
      </div>
      <p style={{ margin: '0 0 12px 0', fontSize: '14px', color: '#a0a0a0' }}>
        {task.description}
      </p>
      <div style={{ fontSize: '12px', color: '#707070' }}>
        {task.scheduledFor && <div>📅 Scheduled: {task.scheduledFor}</div>}
        {task.estimatedDuration && <div>⏱️ Est: {task.estimatedDuration}</div>}
        {task.completedAt && <div>✅ Completed: {new Date(task.completedAt).toLocaleDateString()}</div>}
        {task.outcome && <div style={{ marginTop: '4px', color: '#10b981' }}>→ {task.outcome}</div>}
        {task.blockedBy && <div style={{ marginTop: '4px', color: '#ef4444' }}>🚫 {task.blockedBy}</div>}
        {task.notes && <div style={{ marginTop: '4px', fontStyle: 'italic' }}>{task.notes}</div>}
      </div>
    </div>
  )
}

export default async function Home() {
  const data = await getTasks()

  if (!data) {
    return (
      <main style={{ padding: '40px', maxWidth: '1200px', margin: '0 auto' }}>
        <h1>Failed to load tasks</h1>
      </main>
    )
  }

  const { tasks, meta } = data

  return (
    <main style={{ padding: '40px', maxWidth: '1400px', margin: '0 auto' }}>
      <div style={{ marginBottom: '40px' }}>
        <h1 style={{ fontSize: '32px', margin: '0 0 8px 0' }}>
          👓 Clarke's Task Board
        </h1>
        <p style={{ color: '#707070', margin: 0 }}>
          Last updated: {new Date(meta.lastUpdated).toLocaleString()}
        </p>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
        gap: '24px'
      }}>
        <div>
          <h2 style={{ fontSize: '20px', marginBottom: '16px', color: '#3b82f6' }}>
            🚀 In Progress ({tasks.in_progress?.length || 0})
          </h2>
          {tasks.in_progress?.map(task => (
            <TaskCard key={task.id} task={task} status="in_progress" />
          ))}
          {!tasks.in_progress?.length && (
            <p style={{ color: '#707070' }}>No tasks in progress</p>
          )}
        </div>

        <div>
          <h2 style={{ fontSize: '20px', marginBottom: '16px', color: '#8b5cf6' }}>
            📋 Planned ({tasks.planned?.length || 0})
          </h2>
          {tasks.planned?.map(task => (
            <TaskCard key={task.id} task={task} status="planned" />
          ))}
          {!tasks.planned?.length && (
            <p style={{ color: '#707070' }}>No planned tasks</p>
          )}
        </div>

        <div>
          <h2 style={{ fontSize: '20px', marginBottom: '16px', color: '#6b7280' }}>
            ⏸️ Back Burner ({tasks.backburner?.length || 0})
          </h2>
          {tasks.backburner?.map(task => (
            <TaskCard key={task.id} task={task} status="backburner" />
          ))}
          {!tasks.backburner?.length && (
            <p style={{ color: '#707070' }}>No backburner tasks</p>
          )}
        </div>
      </div>

      <div style={{ marginTop: '40px' }}>
        <h2 style={{ fontSize: '20px', marginBottom: '16px', color: '#10b981' }}>
          ✅ Recently Completed ({tasks.completed?.slice(0, 5).length || 0})
        </h2>
        <div style={{ display: 'grid', gap: '12px' }}>
          {tasks.completed?.slice(0, 5).map(task => (
            <TaskCard key={task.id} task={task} status="completed" />
          ))}
        </div>
      </div>
    </main>
  )
}
