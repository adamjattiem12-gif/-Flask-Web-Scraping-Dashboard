export const exportToCSV = (data, filename = 'market-data') => {
  // Check if there's data to export
  if (!data || data.length === 0) {
    alert('No data to export!')
    return
  }

  // Get headers from the first item's keys
  const headers = Object.keys(data[0])
  const rows = []
  
  // Add header row
  rows.push(headers.join(','))

  // Add data rows
  for (const item of data) {
    const values = headers.map(header => {
      let value = item[header] || ''
      
      // If value is an object (like 'extra'), convert to JSON string
      if (typeof value === 'object') {
        value = JSON.stringify(value)
      }
      
      // Wrap in quotes and escape any existing quotes
      return `"${String(value).replace(/"/g, '""')}"`
    })
    rows.push(values.join(','))
  }

  // Create and download the file
  const csvString = rows.join('\n')
  const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  link.href = url
  link.download = `${filename}_${formatDate()}.csv`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

/**
 * exportToJSON
 * @param {Array} data - Array of objects to export
 * @param {string} filename - Filename without extension (default: 'market-data')
 */

export const exportToJSON = (data, filename = 'market-data') => {
  // Check if there's data to export
  if (!data || data.length === 0) {
    alert('No data to export!')
    return
  }

  // Convert to JSON with nice formatting (2 spaces indent)
  const jsonString = JSON.stringify(data, null, 2)
  const blob = new Blob([jsonString], { type: 'application/json' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  link.href = url
  link.download = `${filename}_${formatDate()}.json`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

/**
 * formatDate - Helper function to format date for filename
 * @returns {string} Formatted date string (YYYYMMDD_HHMM)
 * 
 * Used by: Both export functions for consistent filenames
 */
const formatDate = () => {
  const now = new Date()
  return now.getFullYear() +
    String(now.getMonth() + 1).padStart(2, '0') +
    String(now.getDate()).padStart(2, '0') +
    '_' +
    String(now.getHours()).padStart(2, '0') +
    String(now.getMinutes()).padStart(2, '0')
}