import { useState } from 'react';
import { Download, Filter, Search, FileText, Calendar, User } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/ui/Card';
import Button from '../components/ui/Button';
import { formatDate } from '../lib/utils';

interface Report {
  id: string;
  title: string;
  type: 'security-audit' | 'vulnerability-scan' | 'compliance' | 'incident' | 'performance';
  status: 'completed' | 'pending' | 'failed';
  createdAt: Date;
  createdBy: string;
  summary: string;
}

const Reports = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [typeFilter, setTypeFilter] = useState<string>('all');
  
  // Mock reports data
  const [reports] = useState<Report[]>([
    {
      id: '1',
      title: 'Q1 2024 Security Audit Report',
      type: 'security-audit',
      status: 'completed',
      createdAt: new Date(2024, 0, 15),
      createdBy: 'Admin User',
      summary: 'Comprehensive security audit covering network infrastructure, access controls, and compliance requirements.',
    },
    {
      id: '2',
      title: 'Monthly Vulnerability Scan - March 2024',
      type: 'vulnerability-scan',
      status: 'completed',
      createdAt: new Date(2024, 2, 1),
      createdBy: 'Security Team',
      summary: 'Automated vulnerability assessment of all network endpoints and web applications.',
    },
    {
      id: '3',
      title: 'ISO 27001 Compliance Report',
      type: 'compliance',
      status: 'pending',
      createdAt: new Date(2024, 2, 10),
      createdBy: 'Compliance Officer',
      summary: 'Assessment of organizational compliance with ISO 27001 security standards.',
    },
    {
      id: '4',
      title: 'Security Incident Analysis - March 15',
      type: 'incident',
      status: 'completed',
      createdAt: new Date(2024, 2, 15),
      createdBy: 'Incident Response Team',
      summary: 'Detailed analysis of attempted unauthorized access incident.',
    },
    {
      id: '5',
      title: 'Security Tools Performance Review',
      type: 'performance',
      status: 'failed',
      createdAt: new Date(2024, 2, 20),
      createdBy: 'System Administrator',
      summary: 'Evaluation of security tool performance and resource utilization.',
    },
  ]);

  const filteredReports = reports
    .filter(report => typeFilter === 'all' || report.type === typeFilter)
    .filter(report => 
      report.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
      report.summary.toLowerCase().includes(searchQuery.toLowerCase())
    );

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'text-success';
      case 'pending':
        return 'text-warning';
      case 'failed':
        return 'text-error';
      default:
        return 'text-foreground';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'security-audit':
        return <FileText className="h-5 w-5 text-primary" />;
      case 'vulnerability-scan':
        return <FileText className="h-5 w-5 text-secondary" />;
      case 'compliance':
        return <FileText className="h-5 w-5 text-accent" />;
      case 'incident':
        return <FileText className="h-5 w-5 text-error" />;
      case 'performance':
        return <FileText className="h-5 w-5 text-warning" />;
      default:
        return <FileText className="h-5 w-5" />;
    }
  };

  return (
    <div className="space-y-6 animate-in">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold">Security Reports</h1>
          <p className="text-muted-foreground dark:text-muted-foreground-dark">
            View and download security assessment reports
          </p>
        </div>
        <Button>
          <Download className="mr-2 h-4 w-4" /> Generate Report
        </Button>
      </div>

      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground dark:text-muted-foreground-dark" />
          <input
            type="text"
            placeholder="Search reports..."
            className="w-full rounded-md border border-input dark:border-input-dark bg-background dark:bg-background-dark pl-9 pr-4 py-2 text-sm"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        
        <div className="flex items-center gap-2">
          <Filter className="h-4 w-4 text-muted-foreground dark:text-muted-foreground-dark" />
          <select
            className="rounded-md border border-input dark:border-input-dark bg-background dark:bg-background-dark px-3 py-2 text-sm"
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value)}
          >
            <option value="all">All reports</option>
            <option value="security-audit">Security Audits</option>
            <option value="vulnerability-scan">Vulnerability Scans</option>
            <option value="compliance">Compliance Reports</option>
            <option value="incident">Incident Reports</option>
            <option value="performance">Performance Reports</option>
          </select>
        </div>
      </div>

      <div className="space-y-4">
        {filteredReports.length === 0 ? (
          <div className="bg-card dark:bg-card-dark rounded-lg p-8 text-center">
            <p className="text-muted-foreground dark:text-muted-foreground-dark">
              No reports found. Try adjusting your filters or generate a new report.
            </p>
          </div>
        ) : (
          filteredReports.map((report) => (
            <Card key={report.id} className="overflow-hidden">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    {getTypeIcon(report.type)}
                    <CardTitle className="text-lg">{report.title}</CardTitle>
                  </div>
                  <span className={`text-sm font-medium ${getStatusColor(report.status)} capitalize`}>
                    {report.status}
                  </span>
                </div>
                <CardDescription>{report.summary}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground dark:text-muted-foreground-dark">
                  <div className="flex items-center gap-1">
                    <Calendar className="h-4 w-4" />
                    <span>Created: {formatDate(report.createdAt)}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <User className="h-4 w-4" />
                    <span>By: {report.createdBy}</span>
                  </div>
                </div>
                <div className="mt-4 flex justify-end gap-2">
                  <Button variant="outline" size="sm">
                    Preview
                  </Button>
                  <Button size="sm">
                    <Download className="mr-2 h-3 w-3" /> Download
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Report Generation</CardTitle>
          <CardDescription>
            Create custom security reports based on specific criteria
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form className="space-y-4">
            <div>
              <label htmlFor="report-type" className="block text-sm font-medium mb-1">
                Report Type
              </label>
              <select
                id="report-type"
                className="w-full rounded-md border border-input dark:border-input-dark bg-background dark:bg-background-dark px-3 py-2 text-sm"
              >
                <option value="security-audit">Security Audit</option>
                <option value="vulnerability-scan">Vulnerability Scan</option>
                <option value="compliance">Compliance Report</option>
                <option value="incident">Incident Report</option>
                <option value="performance">Performance Report</option>
              </select>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="start-date" className="block text-sm font-medium mb-1">
                  Start Date
                </label>
                <input
                  id="start-date"
                  type="date"
                  className="w-full rounded-md border border-input dark:border-input-dark bg-background dark:bg-background-dark px-3 py-2 text-sm"
                />
              </div>
              
              <div>
                <label htmlFor="end-date" className="block text-sm font-medium mb-1">
                  End Date
                </label>
                <input
                  id="end-date"
                  type="date"
                  className="w-full rounded-md border border-input dark:border-input-dark bg-background dark:bg-background-dark px-3 py-2 text-sm"
                />
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium mb-1">
                Include Sections
              </label>
              <div className="space-y-2">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    className="rounded border-input dark:border-input-dark text-primary mr-2"
                    defaultChecked
                  />
                  <span className="text-sm">Executive Summary</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    className="rounded border-input dark:border-input-dark text-primary mr-2"
                    defaultChecked
                  />
                  <span className="text-sm">Detailed Findings</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    className="rounded border-input dark:border-input-dark text-primary mr-2"
                    defaultChecked
                  />
                  <span className="text-sm">Recommendations</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    className="rounded border-input dark:border-input-dark text-primary mr-2"
                  />
                  <span className="text-sm">Technical Details</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    className="rounded border-input dark:border-input-dark text-primary mr-2"
                  />
                  <span className="text-sm">Compliance Status</span>
                </label>
              </div>
            </div>
            
            <div className="flex justify-end gap-2">
              <Button variant="outline">
                Cancel
              </Button>
              <Button>
                Generate Report
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default Reports;