import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { UploadCloud, CheckCircle, AlertCircle } from 'lucide-react';
import { Button } from '../ui/button';
import { Select } from '../ui/select';
import { Input } from '../ui/input';
import { uploadFile, getUsers } from '../../api/client';
import { useQueryClient } from '@tanstack/react-query';
import { useStore } from '../../store/useStore';

export default function DropZone() {
  const queryClient = useQueryClient();
  const { selectedUser, setAvailableUsers } = useStore();

  const [file, setFile] = useState<File | null>(null);
  const [bank, setBank] = useState('auto');
  const [password, setPassword] = useState('');
  const [uploadUsername, setUploadUsername] = useState(selectedUser !== 'all' ? selectedUser : '');
  const [status, setStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
  const [message, setMessage] = useState('');

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
      setStatus('idle');
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
      'application/pdf': ['.pdf'],
      'application/vnd.ms-excel': ['.xls'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx']
    }
  });

  const handleUpload = async () => {
    if (!file) return;
    setStatus('uploading');
    try {
      const usernameToSend = uploadUsername.trim() || 'default';
      const result = await uploadFile(file, password, bank !== 'auto' ? bank : undefined, usernameToSend);
      setStatus('success');
      const skippedMsg = result.duplicates_skipped ? ` (${result.duplicates_skipped} duplicates skipped)` : '';
      setMessage(`Successfully imported ${result.transactions_inserted || result.transactions_parsed} transactions from ${result.bank || 'statement'} for "${usernameToSend}"${skippedMsg}.`);

      // Refresh all queries and re-fetch user list
      queryClient.invalidateQueries();
      getUsers().then(users => setAvailableUsers(users)).catch(() => {});
    } catch (err: any) {
      setStatus('error');
      setMessage(err?.response?.data?.detail || err.message || 'Failed to upload file. Please try again.');
    }
  };

  return (
    <div className="space-y-6">
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-colors
          ${isDragActive ? 'border-accent bg-accent/5' : 'border-border hover:border-secondary'}`}
      >
        <input {...getInputProps()} />
        <UploadCloud className="w-12 h-12 mx-auto text-secondary mb-4" />
        {file ? (
          <p className="text-primary font-medium">{file.name}</p>
        ) : (
          <p className="text-secondary">Drag &amp; drop a bank statement here, or click to select</p>
        )}
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <label className="text-sm text-secondary">Bank / App Source</label>
          <Select value={bank} onChange={(e) => setBank(e.target.value)}>
            <option value="auto">Auto-detect from filename</option>
            <option value="hdfc">HDFC Bank</option>
            <option value="sbi">SBI Bank</option>
            <option value="idfc">IDFC First Bank</option>
            <option value="central_bank">Central Bank of India</option>
            <option value="phonepe">PhonePe</option>
            <option value="google_pay">Google Pay</option>
            <option value="cred">CRED UPI</option>
          </Select>
        </div>

        <div className="space-y-2">
          <label className="text-sm text-secondary">Statement Password (if PDF is protected)</label>
          <Input
            type="password"
            placeholder="Leave blank if not protected"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <div className="space-y-2 col-span-2">
          <label className="text-sm text-secondary">
            Assign to User <span className="text-secondary/60">(e.g. "Kiran", "Spouse")</span>
          </label>
          <Input
            placeholder="default"
            value={uploadUsername}
            onChange={(e) => setUploadUsername(e.target.value)}
          />
        </div>
      </div>

      <Button
        className="w-full"
        onClick={handleUpload}
        disabled={!file || status === 'uploading'}
      >
        {status === 'uploading' ? 'Uploading...' : 'Upload Statement'}
      </Button>

      {status === 'success' && (
        <div className="p-4 bg-success/20 text-success rounded-md flex items-center gap-2">
          <CheckCircle className="w-5 h-5" /> {message}
        </div>
      )}
      {status === 'error' && (
        <div className="p-4 bg-danger/20 text-danger rounded-md flex items-center gap-2">
          <AlertCircle className="w-5 h-5" /> {message}
        </div>
      )}
    </div>
  );
}