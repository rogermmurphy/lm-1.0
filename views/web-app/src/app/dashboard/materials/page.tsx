'use client';

import { useState, useEffect } from 'react';
import { chat } from '@/lib/api';

interface Material {
  id: number;
  title: string;
  subject?: string;
  content_preview: string;
  created_at: string;
}

export default function MaterialsPage() {
  const [materials, setMaterials] = useState<Material[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isUploading, setIsUploading] = useState(false);
  const [showUploadForm, setShowUploadForm] = useState(false);
  const [title, setTitle] = useState('');
  const [subject, setSubject] = useState('');
  const [content, setContent] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    loadMaterials();
  }, []);

  const loadMaterials = async () => {
    try {
      const response = await chat.getConversations();
      // API returns conversations, but we'll adapt for materials
      // In production, there should be a dedicated materials endpoint
      setMaterials([]);
    } catch (err: any) {
      console.error('Error loading materials:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      
      // Validate file type
      const validTypes = [
        'text/plain',
        'text/markdown',
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
      ];
      
      if (!validTypes.includes(selectedFile.type)) {
        setError('Please upload a text file (TXT, MD, PDF, or DOCX)');
        return;
      }
      
      // Validate file size (max 10MB)
      if (selectedFile.size > 10 * 1024 * 1024) {
        setError('File size must be less than 10MB');
        return;
      }
      
      setFile(selectedFile);
      setTitle(selectedFile.name);
      
      // Read file content for text files
      if (selectedFile.type.startsWith('text/')) {
        const text = await selectedFile.text();
        setContent(text);
      }
      
      setError('');
    }
  };

  const handleUpload = async () => {
    if (!title.trim() || !content.trim()) {
      setError('Title and content are required');
      return;
    }

    setIsUploading(true);
    setError('');

    try {
      await chat.uploadMaterial(title, content, subject || undefined);
      
      // Reset form
      setTitle('');
      setSubject('');
      setContent('');
      setFile(null);
      setShowUploadForm(false);
      
      // Reload materials
      await loadMaterials();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to upload material');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-6 border-2 border-lmPink/30">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-2xl font-bold text-lmGray mb-2">
              Study Materials
            </h1>
            <p className="text-lmGray/70">
              Upload and manage your learning resources for RAG-powered tutoring
            </p>
          </div>
          <button
            onClick={() => setShowUploadForm(!showUploadForm)}
            className="px-4 py-2 bg-lmPink text-white rounded-md hover:bg-lmPink/90 font-medium"
          >
            {showUploadForm ? '✕ Cancel' : '📤 Upload Material'}
          </button>
        </div>

        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        {/* Upload Form */}
        {showUploadForm && (
          <div className="mb-6 bg-lmCream border-2 border-lmPink/30 rounded-lg p-6 space-y-4">
            <h3 className="font-semibold text-lmGray">Upload New Material</h3>
            
            {/* File Upload */}
            <div>
              <label className="block text-sm font-medium text-lmGray mb-2">
                Upload File (Optional)
              </label>
              <input
                type="file"
                accept=".txt,.md,.pdf,.docx"
                onChange={handleFileChange}
                className="block w-full text-sm text-lmGray
                  file:mr-4 file:py-2 file:px-4
                  file:rounded-md file:border-0
                  file:text-sm file:font-semibold
                  file:bg-lmPink/20 file:text-lmGray
                  hover:file:bg-lmPink/30"
              />
            </div>

            {/* Title */}
            <div>
              <label className="block text-sm font-medium text-lmGray mb-2">
                Title *
              </label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g., Chapter 3: Photosynthesis"
                className="block w-full px-3 py-2 border border-lmPink/30 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-lmPurple"
              />
            </div>

            {/* Subject */}
            <div>
              <label className="block text-sm font-medium text-lmGray mb-2">
                Subject (Optional)
              </label>
              <input
                type="text"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                placeholder="e.g., Biology"
                className="block w-full px-3 py-2 border border-lmPink/30 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-lmPurple"
              />
            </div>

            {/* Content */}
            <div>
              <label className="block text-sm font-medium text-lmGray mb-2">
                Content *
              </label>
              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Paste or type your study material content here..."
                rows={10}
                className="block w-full px-3 py-2 border border-lmPink/30 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-lmPurple font-mono text-sm"
              />
              <p className="mt-2 text-sm text-lmGray/60">
                {content.length} characters
              </p>
            </div>

            {/* Upload Button */}
            <button
              onClick={handleUpload}
              disabled={!title.trim() || !content.trim() || isUploading}
              className="w-full py-3 px-4 bg-lmPink text-white rounded-md hover:bg-lmPink/90 focus:outline-none focus:ring-2 focus:ring-lmPurple disabled:opacity-50 disabled:cursor-not-allowed font-medium"
            >
              {isUploading ? 'Uploading...' : 'Upload Material'}
            </button>
          </div>
        )}

        {/* Materials List */}
        {isLoading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-lmPurple mx-auto"></div>
            <p className="mt-4 text-lmGray/70">Loading materials...</p>
          </div>
        ) : materials.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">📚</div>
            <h3 className="text-lg font-semibold text-lmGray mb-2">
              No Materials Yet
            </h3>
            <p className="text-lmGray/70 mb-4">
              Upload study materials to enable RAG-powered tutoring
            </p>
            <button
              onClick={() => setShowUploadForm(true)}
              className="px-6 py-3 bg-lmPink text-white rounded-md hover:bg-lmPink/90 font-medium"
            >
              📤 Upload Your First Material
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {materials.map((material) => (
              <div
                key={material.id}
                className="bg-white border-2 border-lmPink/30 rounded-lg p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-semibold text-lmGray">{material.title}</h3>
                  {material.subject && (
                    <span className="px-2 py-1 bg-lmPurple/20 text-lmPurple text-xs rounded-full">
                      {material.subject}
                    </span>
                  )}
                </div>
                <p className="text-sm text-lmGray/70 mb-3 line-clamp-3">
                  {material.content_preview}
                </p>
                <div className="flex items-center justify-between text-xs text-lmGray/60">
                  <span>{new Date(material.created_at).toLocaleDateString()}</span>
                  <button className="text-red-600 hover:text-red-800">
                    🗑️ Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Info */}
        <div className="mt-6 bg-gradient-to-r from-lmCream to-lmPink/20 border-2 border-lmPink/30 rounded-lg p-4">
          <h3 className="font-semibold text-lmGray mb-2">💡 How It Works</h3>
          <ul className="text-sm text-lmGray/80 space-y-1">
            <li>• Upload lecture notes, textbooks, or study guides</li>
            <li>• Materials are indexed using vector embeddings</li>
            <li>• AI tutor can reference your materials when answering questions</li>
            <li>• Supported formats: TXT, MD, PDF, DOCX</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
