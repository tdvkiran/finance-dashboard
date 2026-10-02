import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';

export default function UploadHistory() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Recent Uploads</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-secondary text-sm text-center py-4">No recent uploads</div>
      </CardContent>
    </Card>
  );
}
