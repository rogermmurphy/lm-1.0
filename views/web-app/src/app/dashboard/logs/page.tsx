'use client';

import { useState, useEffect } from 'react';
import { logger } from '@/lib/logger';

export default function LogsPage() {
  const [logs, setLogs] = useState<any[]>([]);
  const [summary, setSummary] = useState<any>(null);
  const [filter, setFilter] = useState<string>('ALL');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadLogs();
    // Refresh logs every 2 seconds
    const interval = setInterval(loadLogs, 2000);
    return () => clearInterval(interval);
  }, []);

  const loadLogs() => {
    const allLogs = logger.getLogs();
    setLogs(allLogs);
    setSummary(logger.getSummary());
  };

  const handleClearLogs = () => {
    if (confirm('Are you sure you want to clear all logs?')) {
      logger.clearLogs();
      loadLogs();
    }
  };

  const handleDownloadLogs = () => {
    logger.downloadLogs();
  };

  const filteredLogs = logs
    .filter(log => filter === 'ALL' || log.level === filter)
    .filter(log => 
      searchTerm === '' || 
      log.message.toLowerCase().includes(searchTerm.toLowerCase()) ||
      log.category.toLowerCase().includes(searchTerm.toLowerCase())
    )
    .reverse(); // Show newest first

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'ERROR': return 'text-red-700 bg-red-50';
      case 'WARN': return 'text-yellow-700 bg-yellow-50';
      case 'INFO': return 'text-green-700 bg-green-50';
      case 'DEBUG': return 'text-blue-700 bg-blue-50';
      default: return 'text-gray-700 bg-gray-50';
    }
  };

  return (
    <div className="max-w-7xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="mb-6">
          <div className="flex justify-between items-center mb-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 mb-2">
                🔍 Application Logs
              </h1>
              <p className="text-gray-600">
                Verbose logging of all UI operations - automatically refreshes
              </p>
            </div>
            <div className="flex space-x-2">
              <button
                onClick={handleDownloadLogs}
                className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 font-medium"
              >
                📥 Download Logs
              </button>
              <button
                onClick={handleClearLogs}
                className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 font-medium"
              >
                🗑️ Clear Logs
              </button>
            </div>
          </div>

          {/* Summary Stats */}
          {summary && (
            <div className="grid grid-cols-5 gap-4 mb-4">
              <div className="bg-gray-50 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-gray-900">{summary.total}</div>
                <div className="text-sm text-gray-600">Total</div>
              </div>
              <div className="bg-red-50 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-red-700">{summary.errors}</div>
                <div className="text-sm text-red-600">Errors</div>
              </div>
              <div className="bg-yellow-50 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-yellow-700">{summary.warns}</div>
                <div className="text-sm text-yellow-600">Warnings</div>
              </div>
              <div className="bg-green-50 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-green-700">{summary.info}</div>
                <div className="text-sm text-green-600">Info</div>
              </div>
              <div className="bg-blue-50 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-blue-700">{summary.debug}</div>
                <div className="text-sm text-blue-600">Debug</div>
              </div>
            </div>
          )}

          {/* Filters */}
          <div className="flex space-x-4 mb-4">
            <div className="flex-1">
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search logs..."
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <select
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="ALL">All Levels</option>
              <option value="ERROR">Errors Only</option>
              <option value="WARN">Warnings Only</option>
              <option value="INFO">Info Only</option>
              <option value="DEBUG">Debug Only</option>
            </select>
          </div>
        </div>

        {/* Logs Display */}
        <div className="bg-gray-900 rounded-lg p-4 max-h-[600px] overflow-y-auto font-mono text-xs">
          {filteredLogs.length === 0 ? (
            <div className="text-center text-gray-500 py-8">
              No logs found
            </div>
          ) : (
            filteredLogs.map((log, index) => (
              <div
                key={index}
                className="mb-3 pb-3 border-b border-gray-700 last:border-b-0"
              >
                <div className="flex items-start space-x-3">
                  <span className="text-gray-500 flex-shrink-0">
                    {new Date(log.timestamp).toLocaleTimeString()}
                  </span>
                  <span className={`px-2 py-1 rounded text-xs font-semibold flex-shrink-0 ${
                    log.level === 'ERROR' ? 'bg-red-900 text-red-200' :
                    log.level === 'WARN' ? 'bg-yellow-900 text-yellow-200' :
                    log.level === 'INFO' ? 'bg-green-900 text-green-200' :
                    'bg-blue-900 text-blue-200'
                  }`}>
                    {log.level}
                  </span>
                  <span className="text-purple-400 flex-shrink-0">
                    [{log.category}]
                  </span>
                  <span className="text-gray-300 flex-1">
                    {log.message}
                  </span>
                </div>
                {log.data && (
                  <div className="mt-2 ml-12 text-gray-400">
                    <details>
                      <summary className="cursor-pointer hover:text-gray-300">
                        View Details
                      </summary>
                      <pre className="mt-2 p-2 bg-gray-800 rounded overflow-x-auto">
                        {JSON.stringify(log.data, null, 2)}
                      </pre>
                    </details>
                  </div>
                )}
              </div>
            ))
          )}
        </div>

        {/* Info */}
        <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h3 className="font-semibold text-blue-900 mb-2">💡 About Logs</h3>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• Logs are stored in browser localStorage (max 1000 entries)</li>
            <li>• All API requests/responses are logged with full details</li>
            <li>• Page automatically refreshes logs every 2 seconds</li>
            <li>• Download logs button exports to text file for sharing</li>
            <li>• Open browser DevTools Console for real-time logs</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
