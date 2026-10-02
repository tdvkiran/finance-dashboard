import React from 'react';
import DropZone from './DropZone';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';

export default function UploadPage() {
  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold text-primary">Upload Statement</h1>
      <Card>
        <CardHeader>
          <CardTitle>Import Bank Statement</CardTitle>
        </CardHeader>
        <CardContent>
          <DropZone />
        </CardContent>
      </Card>
    </div>
  );
}