import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { AlertTriangle, Shield, Activity, Server } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card';
import { formatDate } from '../lib/utils';

// Mock data
const securityEvents = [
  { name: 'Mon', value: 12 },
  { name: 'Tue', value: 19 },
  { name: 'Wed', value: 7 },
  { name: 'Thu', value: 15 },
  { name: 'Fri', value: 23 },
  { name: 'Sat', value: 8 },
  { name: 'Sun', value: 5 },
];

const vulnerabilityData = [
  { name: 'Critical', value: 4, color: '#ef4444' },
  { name: 'High', value: 8, color: '#f97316' },
  { name: 'Medium', value: 15, color: '#eab308' },
  { name: 'Low', value: 27, color: '#22c55e' },
];

const recentAlerts = [
  {
    id: '1',
    title: 'Brute Force Attempt Detected',
    description: 'Multiple failed login attempts from IP 192.168.1.105',
    severity: 'Critical',
    timestamp: new Date(Date.now() - 1000 * 60 * 30), // 30 minutes ago
  },
  {
    id: '2',
    title: 'Suspicious File Detected',
    description: 'Potential malware detected in uploads folder',
    severity: 'High',
    timestamp: new Date(Date.now() - 1000 * 60 * 120), // 2 hours ago
  },
  {
    id: '3',
    title: 'Unusual Network Traffic',
    description: 'Unexpected outbound connections to unknown IPs',
    severity: 'Medium',
    timestamp: new Date(Date.now() - 1000 * 60 * 240), // 4 hours ago
  },
  {
    id: '4',
    title: 'System Update Available',
    description: 'Security patches available for 3 systems',
    severity: 'Low',
    timestamp: new Date(Date.now() - 1000 * 60 * 360), // 6 hours ago
  },
];

// Severity badge component
const SeverityBadge = ({ severity }: { severity: string }) => {
  const getColor = () => {
    switch (severity) {
      case 'Critical':
        return 'bg-error/20 text-error';
      case 'High':
        return 'bg-orange-500/20 text-orange-500';
      case 'Medium':
        return 'bg-warning/20 text-warning';
      case 'Low':
        return 'bg-success/20 text-success';
      default:
        return 'bg-muted text-muted-foreground';
    }
  };

  return (
    <span className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${getColor()}`}>
      {severity}
    </span>
  );
};

const Dashboard = () => {
  return (
    <div className="space-y-6 animate-in">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold">Security Dashboard</h1>
          <p className="text-muted-foreground dark:text-muted-foreground-dark">
            Overview of your security posture and recent activity
          </p>
        </div>
        <div className="flex gap-2">
          <select className="h-9 rounded-md border border-input bg-transparent px-3 text-sm">
            <option value="today">Today</option>
            <option value="yesterday">Yesterday</option>
            <option value="last7days" selected>Last 7 days</option>
            <option value="last30days">Last 30 days</option>
          </select>
        </div>
      </div>

      {/* Security metrics cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Security Score</CardTitle>
            <Shield className="h-4 w-4 text-muted-foreground dark:text-muted-foreground-dark" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">78/100</div>
            <p className="text-xs text-muted-foreground dark:text-muted-foreground-dark">
              +2 from last week
            </p>
            <div className="mt-4 h-2 w-full rounded-full bg-muted dark:bg-muted-dark overflow-hidden">
              <div className="h-full bg-primary" style={{ width: '78%' }}></div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Active Threats</CardTitle>
            <AlertTriangle className="h-4 w-4 text-muted-foreground dark:text-muted-foreground-dark" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">12</div>
            <p className="text-xs text-muted-foreground dark:text-muted-foreground-dark">
              +3 from yesterday
            </p>
            <div className="mt-4 h-2 w-full rounded-full bg-muted dark:bg-muted-dark overflow-hidden">
              <div className="h-full bg-error" style={{ width: '60%' }}></div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Systems Monitored</CardTitle>
            <Server className="h-4 w-4 text-muted-foreground dark:text-muted-foreground-dark" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">26</div>
            <p className="text-xs text-muted-foreground dark:text-muted-foreground-dark">
              2 systems offline
            </p>
            <div className="mt-4 h-2 w-full rounded-full bg-muted dark:bg-muted-dark overflow-hidden">
              <div className="h-full bg-secondary" style={{ width: '92%' }}></div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Events</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground dark:text-muted-foreground-dark" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">89</div>
            <p className="text-xs text-muted-foreground dark:text-muted-foreground-dark">
              +12 in last 24 hours
            </p>
            <div className="mt-4 h-2 w-full rounded-full bg-muted dark:bg-muted-dark overflow-hidden">
              <div className="h-full bg-success" style={{ width: '42%' }}></div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Charts and alerts section */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card className="col-span-1">
          <CardHeader>
            <CardTitle>Security Events</CardTitle>
          </CardHeader>
          <CardContent className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={securityEvents} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="name" tickLine={false} axisLine={false} />
                <YAxis tickLine={false} axisLine={false} />
                <Tooltip />
                <Bar dataKey="value" fill="#3B82F6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
        
        <Card className="col-span-1">
          <CardHeader>
            <CardTitle>Vulnerability Distribution</CardTitle>
          </CardHeader>
          <CardContent className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={vulnerabilityData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={2}
                  dataKey="value"
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  labelLine={false}
                >
                  {vulnerabilityData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Recent alerts */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Alerts</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {recentAlerts.map((alert) => (
              <div key={alert.id} className="flex items-start gap-4 p-3 rounded-lg border border-border dark:border-border-dark hover:bg-muted/50 dark:hover:bg-muted-dark/50 transition-colors">
                <div className="mt-1">
                  <AlertTriangle className={`h-5 w-5 ${alert.severity === 'Critical' ? 'text-error' : alert.severity === 'High' ? 'text-orange-500' : alert.severity === 'Medium' ? 'text-warning' : 'text-success'}`} />
                </div>
                <div className="flex-1">
                  <div className="flex justify-between items-start">
                    <h3 className="font-medium">{alert.title}</h3>
                    <SeverityBadge severity={alert.severity} />
                  </div>
                  <p className="text-sm text-muted-foreground dark:text-muted-foreground-dark mt-1">{alert.description}</p>
                  <p className="text-xs text-muted-foreground dark:text-muted-foreground-dark mt-2">{formatDate(alert.timestamp)}</p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Dashboard;