import React, { useState } from 'react';
import { Search, AlertTriangle, Eye, Info, ExternalLink, Map } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '../../components/ui/Card';
import Button from '../../components/ui/Button';

interface IntelligenceResult {
  ip?: string;
  domain?: string;
  malicious: boolean;
  risk: 'Low' | 'Medium' | 'High' | 'Critical';
  lastSeen: string;
  tags: string[];
  details: {
    countryCode?: string;
    asn?: string;
    category?: string;
    malwareType?: string;
    firstSeen?: string;
    associatedUrls?: string[];
  };
}

const ThreatIntelligence = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState<IntelligenceResult | null>(null);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!searchQuery) return;
    
    setIsLoading(true);
    
    // Simulate API call with mock data
    setTimeout(() => {
      // Mock results based on input
      let mockResult: IntelligenceResult;
      
      if (searchQuery.includes('malware') || searchQuery.includes('evil')) {
        mockResult = {
          domain: searchQuery.includes('@') ? undefined : searchQuery,
          ip: searchQuery.match(/\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/) ? searchQuery : undefined,
          malicious: true,
          risk: 'High',
          lastSeen: '2 days ago',
          tags: ['Malware', 'C2', 'Phishing'],
          details: {
            countryCode: 'RU',
            asn: 'AS12345',
            category: 'Malware Distribution',
            malwareType: 'Trojan',
            firstSeen: '2023-01-15',
            associatedUrls: [
              'hxxp://evil-malware.example/payload.exe',
              'hxxp://another-bad-site.example/config.bin'
            ]
          }
        };
      } else {
        mockResult = {
          domain: searchQuery.includes('@') ? undefined : searchQuery,
          ip: searchQuery.match(/\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/) ? searchQuery : undefined,
          malicious: false,
          risk: 'Low',
          lastSeen: 'N/A',
          tags: ['Benign'],
          details: {
            countryCode: 'US',
            asn: 'AS15169',
            category: 'Legitimate Business',
          }
        };
      }
      
      setResults(mockResult);
      setIsLoading(false);
    }, 1500);
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'Critical':
        return 'text-error';
      case 'High':
        return 'text-orange-500';
      case 'Medium':
        return 'text-warning';
      case 'Low':
        return 'text-success';
      default:
        return 'text-foreground';
    }
  };

  return (
    <div className="space-y-6 animate-in">
      <div>
        <h1 className="text-2xl font-bold">Threat Intelligence</h1>
        <p className="text-muted-foreground dark:text-muted-foreground-dark">
          Search and analyze indicators of compromise (IOCs)
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>IOC Lookup</CardTitle>
          <CardDescription>
            Search for IPs, domains, URLs, file hashes, or email addresses
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSearch} className="flex gap-2">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground dark:text-muted-foreground-dark" />
              <input
                type="text"
                placeholder="example.com, 192.168.1.1, hash, or email@example.com"
                className="w-full rounded-md border border-input dark:border-input-dark bg-background dark:bg-background-dark pl-9 pr-4 py-2 text-sm"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
            <Button type="submit" isLoading={isLoading}>
              Search
            </Button>
          </form>
          
          <div className="mt-4">
            <div className="text-sm font-medium">Example queries:</div>
            <div className="flex flex-wrap gap-2 mt-2">
              {['example.com', '1.1.1.1', 'malware.exe', 'evil-domain.com'].map((example) => (
                <button
                  key={example}
                  className="px-3 py-1 rounded-full bg-muted dark:bg-muted-dark text-xs hover:bg-muted-foreground/10 dark:hover:bg-muted-foreground-dark/10"
                  onClick={() => setSearchQuery(example)}
                >
                  {example}
                </button>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {results && (
        <Card>
          <CardHeader className="flex flex-row items-start justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                {results.malicious ? (
                  <AlertTriangle className="h-5 w-5 text-error" />
                ) : (
                  <Info className="h-5 w-5 text-success" />
                )}
                {results.domain || results.ip}
              </CardTitle>
              <CardDescription>
                Risk Level: <span className={getRiskColor(results.risk)}>{results.risk}</span>
              </CardDescription>
            </div>
            <div className="flex gap-2">
              <Button variant="outline" size="sm">
                <Eye className="h-4 w-4 mr-2" /> 
                Visualize
              </Button>
              <Button variant="outline" size="sm">
                <ExternalLink className="h-4 w-4 mr-2" /> 
                Open in VT
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="space-y-3">
                <h3 className="text-sm font-medium">Threat Details</h3>
                
                <dl className="grid grid-cols-3 gap-1 text-sm">
                  <dt className="col-span-1 font-medium text-muted-foreground dark:text-muted-foreground-dark">Status</dt>
                  <dd className="col-span-2">
                    <span className={`font-medium ${results.malicious ? 'text-error' : 'text-success'}`}>
                      {results.malicious ? 'Malicious' : 'Clean'}
                    </span>
                  </dd>
                  
                  <dt className="col-span-1 font-medium text-muted-foreground dark:text-muted-foreground-dark">Last Seen</dt>
                  <dd className="col-span-2">{results.lastSeen}</dd>
                  
                  <dt className="col-span-1 font-medium text-muted-foreground dark:text-muted-foreground-dark">First Seen</dt>
                  <dd className="col-span-2">{results.details.firstSeen || 'N/A'}</dd>
                  
                  <dt className="col-span-1 font-medium text-muted-foreground dark:text-muted-foreground-dark">Category</dt>
                  <dd className="col-span-2">{results.details.category}</dd>
                  
                  {results.details.malwareType && (
                    <>
                      <dt className="col-span-1 font-medium text-muted-foreground dark:text-muted-foreground-dark">Malware Type</dt>
                      <dd className="col-span-2">{results.details.malwareType}</dd>
                    </>
                  )}
                  
                  <dt className="col-span-1 font-medium text-muted-foreground dark:text-muted-foreground-dark">Tags</dt>
                  <dd className="col-span-2">
                    <div className="flex flex-wrap gap-1">
                      {results.tags.map((tag) => (
                        <span
                          key={tag}
                          className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                            tag === 'Malware' || tag === 'Phishing' || tag === 'C2'
                              ? 'bg-error/10 text-error'
                              : tag === 'Benign'
                              ? 'bg-success/10 text-success'
                              : 'bg-muted dark:bg-muted-dark'
                          }`}
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </dd>
                </dl>
              </div>
              
              <div className="space-y-3">
                <h3 className="text-sm font-medium">Location Information</h3>
                
                <div className="aspect-video rounded-md bg-muted dark:bg-muted-dark flex items-center justify-center">
                  <Map className="h-8 w-8 text-muted-foreground dark:text-muted-foreground-dark" />
                  <span className="ml-2 text-sm">Map data would appear here</span>
                </div>
                
                <dl className="grid grid-cols-3 gap-1 text-sm">
                  <dt className="col-span-1 font-medium text-muted-foreground dark:text-muted-foreground-dark">Country</dt>
                  <dd className="col-span-2">{results.details.countryCode || 'Unknown'}</dd>
                  
                  <dt className="col-span-1 font-medium text-muted-foreground dark:text-muted-foreground-dark">ASN</dt>
                  <dd className="col-span-2">{results.details.asn || 'Unknown'}</dd>
                </dl>
                
                {results.details.associatedUrls && results.details.associatedUrls.length > 0 && (
                  <div className="mt-4">
                    <h3 className="text-sm font-medium mb-2">Associated URLs</h3>
                    <ul className="space-y-1">
                      {results.details.associatedUrls.map((url) => (
                        <li key={url} className="text-xs font-mono bg-muted dark:bg-muted-dark p-1 rounded">
                          {url}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          </CardContent>
          <CardFooter className="justify-between border-t border-border dark:border-border-dark pt-4">
            <Button variant="outline" size="sm">
              Export Report
            </Button>
            <Button size="sm">
              Add to Blocklist
            </Button>
          </CardFooter>
        </Card>
      )}
      
      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Threat Feeds</CardTitle>
            <CardDescription>
              Manage and configure threat intelligence feeds
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-success"></div>
                  <span className="font-medium">AlienVault OTX</span>
                </div>
                <span className="text-xs text-muted-foreground dark:text-muted-foreground-dark">Updated 2h ago</span>
              </div>
              
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-success"></div>
                  <span className="font-medium">Abuse.ch</span>
                </div>
                <span className="text-xs text-muted-foreground dark:text-muted-foreground-dark">Updated 4h ago</span>
              </div>
              
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-warning"></div>
                  <span className="font-medium">Cisco Talos</span>
                </div>
                <span className="text-xs text-muted-foreground dark:text-muted-foreground-dark">Update failed</span>
              </div>
              
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-success"></div>
                  <span className="font-medium">VirusTotal</span>
                </div>
                <span className="text-xs text-muted-foreground dark:text-muted-foreground-dark">Updated 1h ago</span>
              </div>
            </div>
          </CardContent>
          <CardFooter>
            <Button variant="outline" className="w-full">Manage Feeds</Button>
          </CardFooter>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Recent Threats</CardTitle>
            <CardDescription>
              Latest threats detected across all sources
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="border-l-2 border-error pl-3">
                <div className="font-medium">Ransomware Campaign</div>
                <div className="text-sm text-muted-foreground dark:text-muted-foreground-dark">New strain targeting healthcare</div>
                <div className="text-xs text-muted-foreground dark:text-muted-foreground-dark">10 minutes ago</div>
              </div>
              
              <div className="border-l-2 border-warning pl-3">
                <div className="font-medium">Phishing Attack</div>
                <div className="text-sm text-muted-foreground dark:text-muted-foreground-dark">Targeting financial institutions</div>
                <div className="text-xs text-muted-foreground dark:text-muted-foreground-dark">2 hours ago</div>
              </div>
              
              <div className="border-l-2 border-primary pl-3">
                <div className="font-medium">Zero-day Vulnerability</div>
                <div className="text-sm text-muted-foreground dark:text-muted-foreground-dark">Critical browser vulnerability</div>
                <div className="text-xs text-muted-foreground dark:text-muted-foreground-dark">1 day ago</div>
              </div>
            </div>
          </CardContent>
          <CardFooter>
            <Button variant="outline" className="w-full">View All Threats</Button>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
};

export default ThreatIntelligence;