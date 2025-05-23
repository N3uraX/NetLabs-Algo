import { useState } from 'react';
import { Bell, Settings, Sun, Moon, Menu, Search } from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';
import { useTheme } from '../../contexts/ThemeContext';
import Button from '../ui/Button';

interface HeaderProps {
  onMenuClick: () => void;
}

const Header = ({ onMenuClick }: HeaderProps) => {
  const { user, logout } = useAuth();
  const { darkMode, toggleTheme } = useTheme();
  const [notificationCount] = useState(3);
  
  return (
    <header className="sticky top-0 z-10 flex h-16 items-center border-b border-border dark:border-border-dark bg-card dark:bg-card-dark px-4 md:px-6">
      <button
        onClick={onMenuClick}
        className="mr-4 rounded-md p-2 text-muted-foreground dark:text-muted-foreground-dark hover:bg-muted dark:hover:bg-muted-dark md:hidden"
        aria-label="Open menu"
      >
        <Menu className="h-5 w-5" />
      </button>
      
      <div className="hidden md:flex md:items-center md:gap-2">
        <Search className="h-5 w-5 text-muted-foreground dark:text-muted-foreground-dark" />
        <input 
          type="search" 
          placeholder="Search..." 
          className="w-64 bg-transparent border-none text-sm focus:outline-none text-foreground dark:text-foreground-dark placeholder:text-muted-foreground dark:placeholder:text-muted-foreground-dark"
        />
      </div>
      
      <div className="ml-auto flex items-center gap-4">
        <button
          onClick={toggleTheme}
          className="rounded-md p-2 text-muted-foreground dark:text-muted-foreground-dark hover:bg-muted dark:hover:bg-muted-dark"
          aria-label={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
        >
          {darkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
        </button>
        
        <div className="relative">
          <button
            className="rounded-md p-2 text-muted-foreground dark:text-muted-foreground-dark hover:bg-muted dark:hover:bg-muted-dark"
            aria-label="View notifications"
          >
            <Bell className="h-5 w-5" />
            {notificationCount > 0 && (
              <span className="absolute top-1 right-1 flex h-4 w-4 items-center justify-center rounded-full bg-error text-[10px] font-medium text-white">
                {notificationCount}
              </span>
            )}
          </button>
        </div>
        
        <a href="/settings" className="rounded-md p-2 text-muted-foreground dark:text-muted-foreground-dark hover:bg-muted dark:hover:bg-muted-dark">
          <Settings className="h-5 w-5" />
        </a>
        
        <div className="flex items-center gap-2">
          <div className="rounded-full bg-primary h-8 w-8 flex items-center justify-center text-white font-medium">
            {user?.name.charAt(0).toUpperCase()}
          </div>
          <div className="hidden md:block">
            <p className="text-sm font-medium">{user?.name}</p>
            <p className="text-xs text-muted-foreground dark:text-muted-foreground-dark">{user?.role}</p>
          </div>
          <Button variant="ghost" size="sm" onClick={logout} className="ml-2 hidden md:block">
            Log out
          </Button>
        </div>
      </div>
    </header>
  );
};

export default Header;