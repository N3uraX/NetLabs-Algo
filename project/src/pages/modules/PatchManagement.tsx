import React, { useState } from 'react';
import { HardDrive, Download, Check, AlertTriangle, Filter, Search, ChevronDown, RefreshCw } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '../../components/ui/Card';
import Button from '../../components/ui/Button';

interface System {
  id: string;
  name: string;
  type: 'server' | 'workstation' | 'mobile';
  os: string;
  ipAddress: string;
  lastUpdated: string;
  updates: {
    critical: number;
    important: number;
    moderate: number;
    low: number;
  };
  status: 'up-to-date' | 'needs-attention' | 'critical' | 'offline';
}

const PatchManagement = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [showPatchWindow, setShowPatchWindow] = useState(false);
  
  // Mock systems data
  const [systems, setSystems] = useState<System[]>([
    {
      id: '1',
      name: 'DC-PROD-01',
      type: 'server',
      os: 'Windows Server 2019',
      ipAddress: '10.0.1.5',
      lastUpdated: '3 days ago',
      updates: {
        critical: 0,
        important: 1,
        moderate: 3,
        low: 0,
      },
      status: 'needs-attention',
    },
    {
      id: '2',
      name: 'WEB-PROD-01',
      type: 'server',
      os: 'Ubuntu 22.04 LTS',
      ipAddress: '10.0.1.10',
      lastUpdated: '1 day ago',
      updates: {
        critical: 0,
        important: 0,
        moderate: 0,
        low: 2,
      },
      status: 'up-to-date',
    },
    {
      id: '3',
      name: 'FINANCE-PC',
      type: 'workstation',
      os: 'Windows 11 Pro',
      ipAddress: '10.0.2.15',
      lastUpdated: '7 days ago',
      updates: {
        critical: 2,
        important: 3,
        moderate: 5,
        low: 1,
      },
      status: 'critical',
    },
    {
      id: '4',
      name: 'DEV-LAPTOP-03',
      type: 'workstation',
      os: 'macOS Ventura',
      ipAddress: '10.0.2.23',
      lastUpdated: '2 days ago',
      updates: {
        critical: 0,
        important: 0,
        moderate: 1,
        low: 3,
      },
      status: 'up-to-date',
    },
    {
      id: '5',
      name: 'RECEPTION-KIOSK',
      type: 'workstation',
      os: 'Windows 10 Enterprise',
      ipAddress: '10.0.3.5',
      lastUpdated: 'Unknown',
      updates: {
        critical: 0,
        important: 0,
        moderate: 0,
        low: 0,
      },
      status: 'offline',
    },
  ]);

  const filteredSystems = systems
    .filter(system => statusFilter === 'all' || system.status === statusFilter)
    .filter(system => 
      system.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
      system.os.toLowerCase().includes(searchQuery.toLowerCase()) ||
      system.ipAddress.includes(searchQuery)
    );

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'up-to-date':
        return 'text-success';
      case 'needs-attention':
        return 'text-warning';
      case 'critical':
        return 'text-error';
      case 'offline':
        return 'text-muted-foreground dark:text-muted-foreground-dark';
      default:
        return 'text-foreground';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'up-to-date':
        return <Check className="h-4 w-4 text-success" />;
      case 'needs-attention':
        return <AlertTriangle className="h-4 w-4 text-warning" />;
      case 'critical':
        return <AlertTriangle className="h-4 w-4 text-error" />;
      default:
        return <AlertTriangle className="h-4 w-4 text-muted-foreground dark:text-muted-foreground-dark" />;
    }
  };

  const getTotalUpdates = (system: System) => {
    return system.updates.critical + system.updates.important + system.updates.moderate + system.updates.low;
  };

  const getSystemTypeIcon = (type: string) => {
    switch (type) {
      case 'server':
        return <HardDrive className="h-4 w-4" />;
      case 'workstation':
        return <HardDrive className="h-4 w-4" />;
      case 'mobile':
        return <HardDrive className="h-4 w-4" />;
      default:
        return <HardDrive className="h-4 w-4" />;
    }
  };

  return (
    <div className="space-y-6 animate-in">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold">Patch Management</h1>
          <p className="text-muted-foreground dark:text-muted-foreground-dark">
            Monitor and update systems across your network
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            onClick={() => {
              // In a real app, this would trigger a scan for updates
              alert('Scanning for updates...');
            }}
          >
            <RefreshCw className="mr-2 h-4 w-4" /> Scan for Updates
          </Button>
          <Button onClick={() => setShowPatchWindow(!showPatchWindow)}>
            <Download className="mr-2 h-4 w-4" /> Create Patch Window
          </Button>
        </div>
      </div>

      {showPatchWindow && (
        <Card>
          <CardHeader>
            <CardTitle>Schedule Patch Window</CardTitle>
            <CardDescription>
              Create a maintenance window for applying updates
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form className="space-y-4">
              <div>
                <label htmlFor="window-name" className="block text-sm font-medium mb-1">
                  Window Name
                </label>
                <input
                  id="window-name"
                  type="text"
                  placeholder="e.g., July Security Patches"
                  className="w-full rounded-md border border-input dark:border-input-dark bg-background dark:bg-background-dark px-3 py-2 text-sm"
                />
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="start-date" className="block text-sm font-medium mb-1">
                    Start Date & Time
                  </label>
                  <input
                    id="start-date"
                    type="datetime-local"
                    className="w-full rounded-md border border-input dark:border-input-dark bg-background dark:bg-background-dark px-3 py-2 text-sm"
                  />
                </div>
                
                <div>
                  <label htmlFor="end-date" className="block text-sm font-medium mb-1">
                    End Date & Time
                  </label>
                  <input
                    id="end-date"
                    type="datetime-local"
                    className="w-full rounded-md border border-input dark:border-input-dark bg-background dark:bg-background-dark px-3 py-2 text-sm"
                  />
                </div>
              </div>
              
              <div>
                <label htmlFor="systems" className="block text-sm font-medium mb-1">
                  Select Systems
                </label>
                <select
                  id="systems"
                  multiple
                  className="w-full rounded-md border border-input dark:border-input-dark bg-background dark:bg-background-dark px-3 py-2 text-sm h-32"
                >
                  {systems.map((system) => (
                    <option key={system.id} value={system.id}>
                      {system.name} - {system.os} ({system.ipAddress})
                    </option>
                  ))}
                </select>
                <p className="text-xs text-muted-foreground dark:text-muted-foreground-dark mt-1">
                  Hold Ctrl/Cmd to select multiple systems
                </p>
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">
                  Update Types
                </label>
                <div className="flex flex-wrap gap-3">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      className="rounded border-input dark:border-input-dark text-primary mr-2"
                      defaultChecked
                    />
                    <span>Critical</span>
                  </label>
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      className="rounded border-input dark:border-input-dark text-primary mr-2"
                      defaultChecked
                    />
                    <span>Important</span>
                  </label>
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      className="rounded border-input dark:border-input-dark text-primary mr-2"
                    />
                    <span>Moderate</span>
                  </label>
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      className="rounded border-input dark:border-input-dark text-primary mr-2"
                    />
                    <span>Low</span>
                  </label>
                </div>
              </div>
              
              <div>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    className="rounded border-input dark:border-input-dark text-primary mr-2"
                  />
                  <span className="text-sm">Automatic reboot if required</span>
                </label>
              </div>
            </form>
          </CardContent>
          <CardFooter className="justify-between">
            <Button variant="outline" onClick={() => setShowPatchWindow(false)}>
              Cancel
            </Button>
            <Button>
              Schedule Patch Window
            </Button>
          </CardFooter>
        </Card>
      )}

      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground dark:text-muted-foreground-dark" />
          <input
            type="text"
            placeholder="Search systems..."
            className="w-full rounded-md border border-input dark:border-input-dark bg-background dark:bg-background-dark pl-9 pr-4 py-2 text-sm"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        
        <div className="flex items-center gap-2">
          <Filter className="h-4 w-4 text-muted-foreground dark:text-muted-foreground-dark" />
          <select
            className="rounded-md border border-input dark:border-input-dark bg-background dark:bg-background-dark px-3 py-2 text-sm"
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <option value="all">All systems</option>
            <option value="up-to-date">Up to date</option>
            <option value="needs-attention">Needs attention</option>
            <option value="critical">Critical updates</option>
            <option value="offline">Offline</option>
          </select>
        </div>
      </div>

      <div className="space-y-4">
        {filteredSystems.length === 0 ? (
          <div className="bg-card dark:bg-card-dark rounded-lg p-8 text-center">
            <p className="text-muted-foreground dark:text-muted-foreground-dark">
              No systems found. Try adjusting your filters.
            </p>
          </div>
        ) : (
          filteredSystems.map((system) => (
            <Card key={system.id} className="overflow-hidden">
              <div className="p-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    {getSystemTypeIcon(system.type)}
                    <h3 className="font-medium">{system.name}</h3>
                    <div
                      className={`ml-2 flex items-center gap-1 text-xs font-medium ${getStatusColor(
                        system.status
                      )}`}
                    >
                      <span className="relative flex h-2 w-2">
                        <span
                          className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${
                            system.status === 'up-to-date' ? 'bg-success' : 
                            system.status === 'needs-attention' ? 'bg-warning' : 
                            system.status === 'critical' ? 'bg-error' : 'bg-muted-foreground'
                          }`}
                        ></span>
                        <span
                          className={`relative inline-flex rounded-full h-2 w-2 ${
                            system.status === 'up-to-date' ? 'bg-success' : 
                            system.status === 'needs-attention' ? 'bg-warning' : 
                            system.status === 'critical' ? 'bg-error' : 'bg-muted-foreground'
                          }`}
                        ></span>
                      </span>
                      {system.status === 'up-to-date' ? 'Up to date' : 
                       system.status === 'needs-attention' ? 'Needs attention' : 
                       system.status === 'critical' ? 'Critical updates' : 'Offline'}
                    </div>
                  </div>
                  
                  <div className="text-sm text-muted-foreground dark:text-muted-foreground-dark">
                    Last updated: {system.lastUpdated}
                  </div>
                </div>
                
                <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="col-span-1">
                    <div className="text-xs font-medium text-muted-foreground dark:text-muted-foreground-dark mb-1">System Information</div>
                    <div className="space-y-1 text-sm">
                      <div className="flex justify-between">
                        <span className="text-muted-foreground dark:text-muted-foreground-dark">OS:</span>
                        <span>{system.os}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground dark:text-muted-foreground-dark">IP:</span>
                        <span>{system.ipAddress}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground dark:text-muted-foreground-dark">Type:</span>
                        <span className="capitalize">{system.type}</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="col-span-1 md:col-span-2">
                    <div className="text-xs font-medium text-muted-foreground dark:text-muted-foreground-dark mb-1">Pending Updates</div>
                    <div className="grid grid-cols-4 gap-2">
                      <div className="flex flex-col items-center justify-center p-2 rounded bg-muted dark:bg-muted-dark">
                        <span className={`text-lg font-bold ${system.updates.critical > 0 ? 'text-error' : ''}`}>
                          {system.updates.critical}
                        </span>
                        <span className="text-xs text-muted-foreground dark:text-muted-foreground-dark">Critical</span>
                      </div>
                      <div className="flex flex-col items-center justify-center p-2 rounded bg-muted dark:bg-muted-dark">
                        <span className={`text-lg font-bold ${system.updates.important > 0 ? 'text-warning' : ''}`}>
                          {system.updates.important}
                        </span>
                        <span className="text-xs text-muted-foreground dark:text-muted-foreground-dark">Important</span>
                      </div>
                      <div className="flex flex-col items-center justify-center p-2 rounded bg-muted dark:bg-muted-dark">
                        <span className="text-lg font-bold">
                          {system.updates.moderate}
                        </span>
                        <span className="text-xs text-muted-foreground dark:text-muted-foreground-dark">Moderate</span>
                      </div>
                      <div className="flex flex-col items-center justify-center p-2 rounded bg-muted dark:bg-muted-dark">
                        <span className="text-lg font-bold">
                          {system.updates.low}
                        </span>
                        <span className="text-xs text-muted-foreground dark:text-muted-foreground-dark">Low</span>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="mt-4 flex flex-wrap justify-end gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    disabled={system.status === 'offline'}
                  >
                    View Details
                  </Button>
                  <Button
                    size="sm"
                    disabled={system.status === 'offline' || system.status === 'up-to-date' || getTotalUpdates(system) === 0}
                  >
                    <Download className="mr-1 h-3 w-3" /> Update Now
                  </Button>
                </div>
              </div>
            </Card>
          ))
        )}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Patch Compliance</CardTitle>
          <CardDescription>Overall system patch status</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h3 className="text-lg font-medium">Systems Up To Date</h3>
                <p className="text-muted-foreground dark:text-muted-foreground-dark">
                  {systems.filter(s => s.status === 'up-to-date').length} of {systems.length} systems (
                  {Math.round((systems.filter(s => s.status === 'up-to-date').length / systems.length) * 100)}%)
                </p>
              </div>
              <div className="w-full sm:w-64 h-4 bg-muted dark:bg-muted-dark rounded-full overflow-hidden">
                <div
                  className="h-full bg-success"
                  style={{
                    width: `${Math.round(
                      (systems.filter(s => s.status === 'up-to-date').length / systems.length) * 100
                    )}%`,
                  }}
                ></div>
              </div>
            </div>
            
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h3 className="text-lg font-medium">Critical Updates Pending</h3>
                <p className="text-muted-foreground dark:text-muted-foreground-dark">
                  {systems.filter(s => s.updates.critical > 0).length} of {systems.length} systems (
                  {Math.round((systems.filter(s => s.updates.critical > 0).length / systems.length) * 100)}%)
                </p>
              </div>
              <div className="w-full sm:w-64 h-4 bg-muted dark:bg-muted-dark rounded-full overflow-hidden">
                <div
                  className="h-full bg-error"
                  style={{
                    width: `${Math.round(
                      (systems.filter(s => s.updates.critical > 0).length / systems.length) * 100
                    )}%`,
                  }}
                ></div>
              </div>
            </div>
            
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h3 className="text-lg font-medium">Systems Offline</h3>
                <p className="text-muted-foreground dark:text-muted-foreground-dark">
                  {systems.filter(s => s.status === 'offline').length} of {systems.length} systems (
                  {Math.round((systems.filter(s => s.status === 'offline').length / systems.length) * 100)}%)
                </p>
              </div>
              <div className="w-full sm:w-64 h-4 bg-muted dark:bg-muted-dark rounded-full overflow-hidden">
                <div
                  className="h-full bg-muted-foreground dark:bg-muted-foreground-dark"
                  style={{
                    width: `${Math.round(
                      (systems.filter(s => s.status === 'offline').length / systems.length) * 100
                    )}%`,
                  }}
                ></div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default PatchManagement;