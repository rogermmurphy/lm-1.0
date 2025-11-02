/**
 * Frontend Logger Utility
 * Logs to console AND saves to localStorage for debugging
 * Provides verbose logging for all UI operations
 */

type LogLevel = 'DEBUG' | 'INFO' | 'WARN' | 'ERROR';

interface LogEntry {
  timestamp: string;
  level: LogLevel;
  category: string;
  message: string;
  data?: any;
}

class Logger {
  private maxLogs = 1000; // Keep last 1000 log entries
  private logKey = 'lm_ui_logs';
  
  private log(level: LogLevel, category: string, message: string, data?: any) {
    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      category,
      message,
      data
    };

    // Console output with color
    const colors = {
      DEBUG: '\x1b[36m', // Cyan
      INFO: '\x1b[32m',  // Green
      WARN: '\x1b[33m',  // Yellow
      ERROR: '\x1b[31m'  // Red
    };
    const reset = '\x1b[0m';
    
    console.log(
      `${colors[level]}[${level}]${reset} [${category}] ${message}`,
      data ? data : ''
    );

    // Save to localStorage
    if (typeof window !== 'undefined') {
      try {
        const logs = this.getLogs();
        logs.push(entry);
        
        // Keep only last N logs
        if (logs.length > this.maxLogs) {
          logs.shift();
        }
        
        localStorage.setItem(this.logKey, JSON.stringify(logs));
      } catch (error) {
        console.error('Failed to save log:', error);
      }
    }
  }

  debug(category: string, message: string, data?: any) {
    this.log('DEBUG', category, message, data);
  }

  info(category: string, message: string, data?: any) {
    this.log('INFO', category, message, data);
  }

  warn(category: string, message: string, data?: any) {
    this.log('WARN', category, message, data);
  }

  error(category: string, message: string, data?: any) {
    this.log('ERROR', category, message, data);
  }

  // Get all logs from localStorage
  getLogs(): LogEntry[] {
    if (typeof window === 'undefined') return [];
    
    try {
      const logsJson = localStorage.getItem(this.logKey);
      return logsJson ? JSON.parse(logsJson) : [];
    } catch (error) {
      console.error('Failed to get logs:', error);
      return [];
    }
  }

  // Clear all logs
  clearLogs() {
    if (typeof window !== 'undefined') {
      localStorage.removeItem(this.logKey);
    }
  }

  // Download logs as file
  downloadLogs() {
    const logs = this.getLogs();
    const logText = logs.map(entry => 
      `[${entry.timestamp}] [${entry.level}] [${entry.category}] ${entry.message}${
        entry.data ? '\n  Data: ' + JSON.stringify(entry.data, null, 2) : ''
      }`
    ).join('\n\n');

    const blob = new Blob([logText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `lm-ui-logs-${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  // Get logs summary
  getSummary() {
    const logs = this.getLogs();
    return {
      total: logs.length,
      errors: logs.filter(l => l.level === 'ERROR').length,
      warns: logs.filter(l => l.level === 'WARN').length,
      info: logs.filter(l => l.level === 'INFO').length,
      debug: logs.filter(l => l.level === 'DEBUG').length,
      latest: logs.slice(-10).reverse() // Last 10 logs
    };
  }
}

// Export singleton instance
export const logger = new Logger();

// Log initialization
logger.info('Logger', 'UI Logger initialized', {
  url: typeof window !== 'undefined' ? window.location.href : 'SSR',
  userAgent: typeof window !== 'undefined' ? navigator.userAgent : 'SSR'
});
