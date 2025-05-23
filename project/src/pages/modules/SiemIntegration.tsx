import React from 'react';
import { Database, Server, Link, RefreshCw, Plus, Trash, Shield } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '../../components/ui/Card';
import Button from '../../components/ui/Button';

interface IntegrationConfig {
  id: string;
  name: string;
  type: 'siem' | 'edr' | 'mdm';
  status: 'connected' | 'disconnected' | 'error';
  lastSync: string;
  details: {
    endpoint: string;
    apiKey?: string;
    description: string;
  };
}

const SiemIntegration = () => {
  const [integrations, setIntegrations] = React.useState<IntegrationConfig[]>([
    {
      id: '1',
      name: 'Splunk Enterprise',
      type: 'siem',
      status: 'connected',
      lastSync: '10 minutes ago',
      details: {
        endpoint: 'https://splunk.example.com:8089',
        apiKey: '••••••••••••••••',
        description: 'Main SIEM for SOC operations',
      },
    },
    {
      id: '2',
      name: 'Elastic Security',
      type: 'siem',
      status: 'connected',
      lastSync: '25 minutes ago',
      details: {
        endpoint: 'https://elastic.example.com:9200',
        apiKey: '••••••••••••••••',
        description: 'Secondary SIEM for log aggregation',
      },
    },
    {
      id: '3',
      name: 'CrowdStrike Falcon',
      type: 'edr',
      status: 'error',
      lastSync: '3 hours ago',
      details: {
        endpoint: 'https://api.crowdstrike.com',
        apiKey: '••••••••••••••••',
        description: 'EDR solution for endpoint monitoring',
      },
    },
    {
      id: '4',
      name: 'Microsoft Intune',
      type: 'mdm',
      status: 'disconnected',
      lastSync: 'Never',
      details: {
        endpoint: 'https://graph.microsoft.com/beta/deviceManagement',
        description: 'Mobile device management solution',
      },
    },
  ]);

  const [showNewIntegration, setShowNewIntegration] = React.useState(false);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'connected':
        return 'text-success';
      case 'disconnected':
        return 'text-muted-foreground dark:text-muted-foreground-dark';
      case 'error':
        return 'text-error';
      default:
        return 'text-foreground';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'siem':
        return <Database className="h-5 w-5 text-primary" />;
      case 'edr':
        return <Shield className="h-5 w-5 text-secondary" />;
      case 'mdm':
        return <Server className="h-5 w-5 text-accent" />;
      default:
        return <Database className="h-5 w-5" />;
    }
  };

  const handleSync = (id: string) => {
    // In a real app, this would trigger a synchronization
    // For now, just update the lastSync time
    setIntegrations(
      integrations.map((integration) =>
        integration.id === id
          ? { ...integration, lastSync: 'Just now' }
          : integration
      )
    );
  };

  return (
    <div className="space-y-6 animate-in">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold">SIEM & EDR Integration</h1>
          <p className="text-muted-foreground dark:text-muted-foreground-dark">
            Connect and manage security information and event management systems
          </p>
        </div>
        <Button onClick={() => setShowNewIntegration(!showNewIntegration)}>
          <Plus className="mr-2 h-4 w-4" /> New Integration
        </Button>
      </div>

      {showNewIntegration && (
        <Card>
          <CardHeader>
            <CardTitle>Add New Integration</CardTitle>
            <CardDescription>
              Connect NetLabs Algo to your security systems
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form className="space-y-4">
              <div>
                <label htmlFor="integration-name" className="block text-sm font-medium mb-1">
                  Integration Name
                </label>
                <input
                  id="integration-name"
                  type="text"
                  placeholder="e.g., Splunk SIEM"
                  className="w-full rounded-md border border-input dark:border-input-dark bg-background dark:bg-background-dark px-3 py-2 text-sm"
                />
              </div>
              
              <div>
                <label htmlFor="integration-type" className="block text-sm font-medium mb-1">
                  Integration Type
                </label>
                <select
                  id="integration-type"
                  className="w-full rounded-md border border-input dark:border-input-dark bg-background dark:bg-background-dark px-3 py-2 text-sm"
                >
                  <option value="siem">SIEM System</option>
                  <option value="edr">EDR Solution</option>
                  <option value="mdm">MDM Platform</option>
                </select>
              </div>
              
              <div>
                <label htmlFor="endpoint-url" className="block text-sm font-medium mb-1">
                  API Endpoint URL
                </label>
                <input
                  id="endpoint-url"
                  type="text"
                  placeholder="https://api.example.com"
                  className="w-full rounded-md border border-input dark:border-input-dark bg-background dark:bg-background-dark px-3 py-2 text-sm"
                />
              </div>
              
              <div>
                <label htmlFor="api-key" className="block text-sm font-medium mb-1">
                  API Key / Token
                </label>
                <input
                  id="api-key"
                  type="password"
                  placeholder="Enter API key or token"
                  className="w-full rounded-md border border-input dark:border-input-dark bg-background dark:bg-background-dark px-3 py-2 text-sm"
                />
              </div>
              
              <div>
                <label htmlFor="description" className="block text-sm font-medium mb-1">
                  Description
                </label>
                <textarea
                  id="description"
                  placeholder="Brief description of this integration"
                  rows={2}
                  className="w-full rounded-md border border-input dark:border-input-dark bg-background dark:bg-background-dark px-3 py-2 text-sm"
                ></textarea>
              </div>
            </form>
          </CardContent>
          <CardFooter className="justify-between">
            <Button variant="outline" onClick={() => setShowNewIntegration(false)}>
              Cancel
            </Button>
            <Button>
              Test & Save
            </Button>
          </CardFooter>
        </Card>
      )}

      <div className="grid gap-6 md:grid-cols-2">
        {integrations.map((integration) => (
          <Card key={integration.id} className="overflow-hidden">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  {getTypeIcon(integration.type)}
                  <CardTitle className="text-lg">{integration.name}</CardTitle>
                </div>
                <div
                  className={`flex items-center gap-1 text-xs font-medium ${getStatusColor(
                    integration.status
                  )}`}
                >
                  <span className="relative flex h-2 w-2">
                    <span
                      className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${
                        integration.status === 'connected' ? 'bg-success' : 
                        integration.status === 'error' ? 'bg-error' : 'bg-muted-foreground'
                      }`}
                    ></span>
                    <span
                      className={`relative inline-flex rounded-full h-2 w-2 ${
                        integration.status === 'connected' ? 'bg-success' : 
                        integration.status === 'error' ? 'bg-error' : 'bg-muted-foreground'
                      }`}
                    ></span>
                  </span>
                  {integration.status.charAt(0).toUpperCase() + integration.status.slice(1)}
                </div>
              </div>
              <CardDescription>
                {integration.type === 'siem'
                  ? 'Security Information & Event Management'
                  : integration.type === 'edr'
                  ? 'Endpoint Detection & Response'
                  : 'Mobile Device Management'}
              </CardDescription>
            </CardHeader>
            <CardContent className="pb-2">
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-muted-foreground dark:text-muted-foreground-dark">Endpoint:</span>
                  <span className="truncate max-w-[200px]">{integration.details.endpoint}</span>
                </div>
                
                <div className="flex justify-between">
                  <span className="text-muted-foreground dark:text-muted-foreground-dark">Last sync:</span>
                  <span>{integration.lastSync}</span>
                </div>
                
                <div className="flex justify-between">
                  <span className="text-muted-foreground dark:text-muted-foreground-dark">Description:</span>
                  <span className="truncate max-w-[200px]">{integration.details.description}</span>
                </div>
              </div>
            </CardContent>
            <CardFooter className="flex justify-between pt-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleSync(integration.id)}
              >
                <RefreshCw className="mr-1 h-3 w-3" /> Sync
              </Button>
              
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                >
                  <Link className="mr-1 h-3 w-3" /> Configure
                </Button>
                
                <Button
                  variant="outline"
                  size="sm"
                  className="border-error/30 hover:bg-error/10 text-error hover:text-error"
                >
                  <Trash className="h-3 w-3" />
                </Button>
              </div>
            </CardFooter>
          </Card>
        ))}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Integration Activity</CardTitle>
          <CardDescription>Recent events from connected systems</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="relative pl-5 pb-5 border-l border-border dark:border-border-dark">
              <div className="absolute w-3 h-3 bg-primary rounded-full -left-[6.5px] top-1"></div>
              <div className="text-sm">
                <div className="font-medium">Splunk Enterprise connected</div>
                <p className="text-muted-foreground dark:text-muted-foreground-dark">
                  Successfully established connection with Splunk SIEM
                </p>
                <span className="text-xs text-muted-foreground dark:text-muted-foreground-dark">10 minutes ago</span>
              </div>
            </div>
            
            <div className="relative pl-5 pb-5 border-l border-border dark:border-border-dark">
              <div className="absolute w-3 h-3 bg-error rounded-full -left-[6.5px] top-1"></div>
              <div className="text-sm">
                <div className="font-medium">CrowdStrike Falcon API error</div>
                <p className="text-muted-foreground dark:text-muted-foreground-dark">
                  Authentication failed: Invalid API credentials
                </p>
                <span className="text-xs text-muted-foreground dark:text-muted-foreground-dark">3 hours ago</span>
              </div>
            </div>
            
            <div className="relative pl-5 pb-5 border-l border-border dark:border-border-dark">
              <div className="absolute w-3 h-3 bg-success rounded-full -left-[6.5px] top-1"></div>
              <div className="text-sm">
                <div className="font-medium">Event data synchronized</div>
                <p className="text-muted-foreground dark:text-muted-foreground-dark">
                  Successfully synced 256 events from Elastic Security
                </p>
                <span className="text-xs text-muted-foreground dark:text-muted-foreground-dark">1 day ago</span>
              </div>
            </div>
            
            <div className="relative pl-5">
              <div className="absolute w-3 h-3 bg-warning rounded-full -left-[6.5px] top-1"></div>
              <div className="text-sm">
                <div className="font-medium">Microsoft Intune integration added</div>
                <p className="text-muted-foreground dark:text-muted-foreground-dark">
                  New MDM integration configured but not connected
                </p>
                <span className="text-xs text-muted-foreground dark:text-muted-foreground-dark">2 days ago</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default SiemIntegration;