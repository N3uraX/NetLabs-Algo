import { useState } from 'react';
import { Zap, Wifi, Server, Database, Globe, Shield, ArrowRight } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '../../components/ui/Card';
import Button from '../../components/ui/Button';

interface TestModule {
  id: string;
  name: string;
  description: string;
  icon: React.ElementType;
  status: 'idle' | 'running' | 'completed' | 'failed';
  result?: string;
}

const PenetrationTesting = () => {
  const [modules, setModules] = useState<TestModule[]>([
    {
      id: 'port-scan',
      name: 'Port Scanner',
      description: 'Scan network for open ports and running services',
      icon: Server,
      status: 'idle',
    },
    {
      id: 'web-enum',
      name: 'Web Enumeration',
      description: 'Identify web technologies and vulnerabilities',
      icon: Globe,
      status: 'idle',
    },
    {
      id: 'ssh-brute',
      name: 'SSH Brute Force',
      description: 'Test SSH services for weak credentials',
      icon: Shield,
      status: 'idle',
    },
    {
      id: 'wifi-audit',
      name: 'Wi-Fi Security Audit',
      description: 'Analyze wireless networks for vulnerabilities',
      icon: Wifi,
      status: 'idle',
    },
    {
      id: 'sql-injection',
      name: 'SQL Injection',
      description: 'Test web applications for SQL injection vulnerabilities',
      icon: Database,
      status: 'idle',
    },
    {
      id: 'xss-scanner',
      name: 'XSS Scanner',
      description: 'Detect cross-site scripting vulnerabilities',
      icon: Zap,
      status: 'idle',
    },
  ]);

  const runTest = (id: string) => {
    setModules(modules.map(module => 
      module.id === id 
        ? { ...module, status: 'running' } 
        : module
    ));

    // Simulate test completion after a delay
    setTimeout(() => {
      setModules(modules.map(module => 
        module.id === id 
          ? { 
              ...module, 
              status: 'completed',
              result: 'Test completed successfully. No critical vulnerabilities found.'
            } 
          : module
      ));
    }, 3000);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running':
        return 'text-primary';
      case 'completed':
        return 'text-success';
      case 'failed':
        return 'text-error';
      default:
        return 'text-muted-foreground dark:text-muted-foreground-dark';
    }
  };

  return (
    <div className="space-y-6 animate-in">
      <div>
        <h1 className="text-2xl font-bold">Penetration Testing</h1>
        <p className="text-muted-foreground dark:text-muted-foreground-dark">
          Test systems and applications for security vulnerabilities
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {modules.map((module) => (
          <Card key={module.id} className="overflow-hidden">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg">{module.name}</CardTitle>
                <module.icon className="h-5 w-5 text-primary" />
              </div>
              <CardDescription>{module.description}</CardDescription>
            </CardHeader>
            <CardContent>
              {module.status !== 'idle' && (
                <div className="mb-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium">Status</span>
                    <span className={`text-sm ${getStatusColor(module.status)} capitalize`}>
                      {module.status}
                    </span>
                  </div>
                  {module.status === 'running' && (
                    <div className="h-2 w-full rounded-full bg-muted dark:bg-muted-dark overflow-hidden">
                      <div className="h-full bg-primary animate-pulse" style={{ width: '60%' }}></div>
                    </div>
                  )}
                  {module.result && (
                    <div className="mt-4 p-3 bg-muted dark:bg-muted-dark rounded text-sm">
                      {module.result}
                    </div>
                  )}
                </div>
              )}
            </CardContent>
            <CardFooter className="bg-muted/50 dark:bg-muted-dark/50 px-6 py-3">
              <Button
                onClick={() => runTest(module.id)}
                className="w-full"
                disabled={module.status === 'running'}
                isLoading={module.status === 'running'}
              >
                {module.status === 'idle' ? (
                  <>
                    Run Test <ArrowRight className="ml-2 h-4 w-4" />
                  </>
                ) : module.status === 'running' ? (
                  'Running...'
                ) : (
                  'Run Again'
                )}
              </Button>
            </CardFooter>
          </Card>
        ))}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Custom Penetration Test</CardTitle>
          <CardDescription>
            Configure and run a custom penetration test with advanced options
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <label htmlFor="target" className="block text-sm font-medium mb-1">
                Target IP/Domain
              </label>
              <input
                id="target"
                type="text"
                placeholder="e.g. 192.168.1.1 or example.com"
                className="w-full rounded-md border border-input dark:border-input-dark bg-background dark:bg-background-dark px-3 py-2 text-sm"
              />
            </div>
            
            <div>
              <label htmlFor="scan-type" className="block text-sm font-medium mb-1">
                Scan Type
              </label>
              <select
                id="scan-type"
                className="w-full rounded-md border border-input dark:border-input-dark bg-background dark:bg-background-dark px-3 py-2 text-sm"
              >
                <option value="quick">Quick Scan</option>
                <option value="full">Full Scan</option>
                <option value="vuln">Vulnerability Scan</option>
                <option value="custom">Custom</option>
              </select>
            </div>
            
            <div className="flex items-center">
              <input
                id="aggressive"
                type="checkbox"
                className="h-4 w-4 rounded border-input dark:border-input-dark text-primary focus:ring-primary"
              />
              <label htmlFor="aggressive" className="ml-2 block text-sm">
                Aggressive Mode (may trigger IDS/IPS)
              </label>
            </div>
          </div>
        </CardContent>
        <CardFooter className="justify-end space-x-2">
          <Button variant="outline">Reset</Button>
          <Button>Start Custom Scan</Button>
        </CardFooter>
      </Card>
    </div>
  );
};

export default PenetrationTesting;