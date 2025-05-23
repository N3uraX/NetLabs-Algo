import { Link, useLocation } from 'react-router-dom';
import { 
  Shield, 
  Home, 
  Zap, 
  AlertTriangle, 
  Database, 
  HardDrive, 
  User, 
  BarChart2, 
  RefreshCw, 
  Activity, 
  Smartphone, 
  Clipboard, 
  FileText, 
  Settings as SettingsIcon,
  X 
} from 'lucide-react';
import { cn } from '../../lib/utils';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const Sidebar = ({ isOpen, onClose }: SidebarProps) => {
  const { pathname } = useLocation();
  
  const mainNavItems = [
    { icon: Home, label: 'Dashboard', href: '/' },
    { icon: Clipboard, label: 'Tasks', href: '/tasks' },
    { icon: FileText, label: 'Reports', href: '/reports' },
  ];
  
  const moduleNavItems = [
    { icon: Zap, label: 'Penetration Testing', href: '/modules/penetration-testing' },
    { icon: AlertTriangle, label: 'Threat Intelligence', href: '/modules/threat-intelligence' },
    { icon: Database, label: 'SIEM Integration', href: '/modules/siem-integration' },
    { icon: HardDrive, label: 'Patch Management', href: '/modules/patch-management' },
    { icon: User, label: 'UEBA Analytics', href: '/modules/ueba-analytics' },
    { icon: RefreshCw, label: 'Automated Response', href: '/modules/automated-response' },
    { icon: Activity, label: 'Deep Detection', href: '/modules/deep-detection' },
    { icon: Smartphone, label: 'Mobile Integration', href: '/modules/mobile-integration' },
  ];
  
  return (
    <>
      {/* Mobile sidebar backdrop */}
      {isOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black/50 md:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside 
        className={cn(
          "fixed inset-y-0 left-0 z-50 w-64 transform overflow-y-auto bg-card dark:bg-card-dark border-r border-border dark:border-border-dark p-4 transition-transform duration-200 ease-in-out md:translate-x-0 md:static md:z-0",
          isOpen ? "translate-x-0" : "-translate-x-full"
        )}
      >
        <div className="flex items-center justify-between mb-8">
          <Link to="/" className="flex items-center gap-2">
            <Shield className="h-8 w-8 text-primary" />
            <div>
              <h1 className="font-bold text-lg text-foreground dark:text-foreground-dark">NetLabs Algo</h1>
              <p className="text-xs text-muted-foreground dark:text-muted-foreground-dark">Cybersecurity Toolkit</p>
            </div>
          </Link>
          <button 
            onClick={onClose}
            className="rounded-md p-1 text-muted-foreground dark:text-muted-foreground-dark hover:bg-muted dark:hover:bg-muted-dark md:hidden"
          >
            <X className="h-5 w-5" />
          </button>
        </div>
        
        <nav className="space-y-6">
          <div>
            <h2 className="mb-2 px-2 text-xs font-semibold tracking-wide text-muted-foreground dark:text-muted-foreground-dark uppercase">
              Main
            </h2>
            <ul className="space-y-1">
              {mainNavItems.map((item) => (
                <li key={item.href}>
                  <Link
                    to={item.href}
                    className={cn(
                      "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                      pathname === item.href
                        ? "bg-primary/10 text-primary"
                        : "text-foreground dark:text-foreground-dark hover:bg-muted dark:hover:bg-muted-dark"
                    )}
                  >
                    <item.icon className="h-5 w-5" />
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
          
          <div>
            <h2 className="mb-2 px-2 text-xs font-semibold tracking-wide text-muted-foreground dark:text-muted-foreground-dark uppercase">
              Security Modules
            </h2>
            <ul className="space-y-1">
              {moduleNavItems.map((item) => (
                <li key={item.href}>
                  <Link
                    to={item.href}
                    className={cn(
                      "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                      pathname === item.href
                        ? "bg-primary/10 text-primary"
                        : "text-foreground dark:text-foreground-dark hover:bg-muted dark:hover:bg-muted-dark"
                    )}
                  >
                    <item.icon className="h-5 w-5" />
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
          
          <div>
            <h2 className="mb-2 px-2 text-xs font-semibold tracking-wide text-muted-foreground dark:text-muted-foreground-dark uppercase">
              Settings
            </h2>
            <ul className="space-y-1">
              <li>
                <Link
                  to="/settings"
                  className={cn(
                    "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                    pathname === "/settings"
                      ? "bg-primary/10 text-primary"
                      : "text-foreground dark:text-foreground-dark hover:bg-muted dark:hover:bg-muted-dark"
                  )}
                >
                  <SettingsIcon className="h-5 w-5" />
                  Settings
                </Link>
              </li>
            </ul>
          </div>
        </nav>
        
        <div className="mt-6 rounded-lg bg-muted dark:bg-muted-dark p-4">
          <h3 className="font-medium text-sm">Need Help?</h3>
          <p className="mt-1 text-xs text-muted-foreground dark:text-muted-foreground-dark">
            Check our documentation for guides and API references.
          </p>
          <a
            href="#"
            className="mt-3 inline-block text-xs font-medium text-primary hover:underline"
          >
            View Documentation →
          </a>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;