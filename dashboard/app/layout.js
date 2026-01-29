export const metadata = {
  title: "Clarke's Task Board",
  description: 'Task management for Clarke AI',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body style={{
        margin: 0,
        padding: 0,
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        backgroundColor: '#0a0a0a',
        color: '#e0e0e0'
      }}>
        {children}
      </body>
    </html>
  )
}
