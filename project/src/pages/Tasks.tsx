import { useState } from 'react';
import { Plus, Check, X, Clock, Filter, Search, ChevronDown } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import Button from '../components/ui/Button';
import { formatDate } from '../lib/utils';

interface Task {
  id: string;
  title: string;
  description: string;
  status: 'pending' | 'in progress' | 'completed' | 'failed';
  priority: 'low' | 'medium' | 'high' | 'critical';
  category: string;
  createdAt: Date;
  dueDate?: Date;
  assignedTo?: string;
}

const Tasks = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [showAddTask, setShowAddTask] = useState(false);
  
  // Mock tasks data
  const [tasks, setTasks] = useState<Task[]>([
    {
      id: '1',
      title: 'Investigate suspicious login attempts',
      description: 'Multiple failed login attempts from IP 203.0.113.42',
      status: 'in progress',
      priority: 'high',
      category: 'Security Investigation',
      createdAt: new Date(Date.now() - 86400000 * 2), // 2 days ago
      dueDate: new Date(Date.now() + 86400000), // tomorrow
      assignedTo: 'Admin User',
    },
    {
      id: '2',
      title: 'Update firewall rules',
      description: 'Implement new egress filtering policy',
      status: 'pending',
      priority: 'medium',
      category: 'Network Security',
      createdAt: new Date(Date.now() - 86400000 * 3), // 3 days ago
      dueDate: new Date(Date.now() + 86400000 * 2), // 2 days from now
    },
    {
      id: '3',
      title: 'Deploy EDR agents to marketing department',
      description: 'Install and configure EDR solution on 15 workstations',
      status: 'completed',
      priority: 'medium',
      category: 'Endpoint Security',
      createdAt: new Date(Date.now() - 86400000 * 5), // 5 days ago
      dueDate: new Date(Date.now() - 86400000), // yesterday
      assignedTo: 'Admin User',
    },
    {
      id: '4',
      title: 'Respond to ransomware alert',
      description: 'Critical alert - potential ransomware detected on finance1-pc',
      status: 'failed',
      priority: 'critical',
      category: 'Incident Response',
      createdAt: new Date(Date.now() - 86400000), // 1 day ago
      assignedTo: 'Security Team',
    },
    {
      id: '5',
      title: 'Conduct phishing awareness training',
      description: 'Schedule and conduct quarterly security awareness training',
      status: 'pending',
      priority: 'low',
      category: 'Training',
      createdAt: new Date(Date.now() - 86400000 * 7), // 7 days ago
      dueDate: new Date(Date.now() + 86400000 * 14), // 14 days from now
    },
  ]);

  const filteredTasks = tasks
    .filter(task => statusFilter === 'all' || task.status === statusFilter)
    .filter(task => 
      task.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
      task.description.toLowerCase().includes(searchQuery.toLowerCase())
    );

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <Check className="h-4 w-4 text-success" />;
      case 'failed':
        return <X className="h-4 w-4 text-error" />;
      case 'in progress':
        return <Clock className="h-4 w-4 text-primary animate-pulse-slow" />;
      default:
        return <Clock className="h-4 w-4 text-muted-foreground dark:text-muted-foreground-dark" />;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical':
        return 'bg-error/20 text-error';
      case 'high':
        return 'bg-orange-500/20 text-orange-500';
      case 'medium':
        return 'bg-warning/20 text-warning';
      case 'low':
        return 'bg-success/20 text-success';
      default:
        return 'bg-muted text-muted-foreground';
    }
  };

  const updateTaskStatus = (id: string, status: Task['status']) => {
    setTasks(tasks.map(task => 
      task.id === id ? { ...task, status } : task
    ));
  };

  return (
    <div className="space-y-6 animate-in">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold">Security Tasks</h1>
          <p className="text-muted-foreground dark:text-muted-foreground-dark">
            Manage and track security operations
          </p>
        </div>
        <Button onClick={() => setShowAddTask(!showAddTask)}>
          <Plus className="mr-2 h-4 w-4" /> New Task
        </Button>
      </div>

      {showAddTask && (
        <Card>
          <CardHeader>
            <CardTitle>Add New Task</CardTitle>
          </CardHeader>
          <CardContent>
            <form className="space-y-4">
              <div>
                <label htmlFor="title" className="block text-sm font-medium mb-1">
                  Title
                </label>
                <input
                  id="title"
                  type="text"
                  placeholder="Task title"
                  className="w-full rounded-md border border-input dark:border-input-dark bg-background dark:bg-background-dark px-3 py-2 text-sm"
                />
              </div>
              
              <div>
                <label htmlFor="description" className="block text-sm font-medium mb-1">
                  Description
                </label>
                <textarea
                  id="description"
                  placeholder="Task description"
                  rows={3}
                  className="w-full rounded-md border border-input dark:border-input-dark bg-background dark:bg-background-dark px-3 py-2 text-sm"
                ></textarea>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="priority" className="block text-sm font-medium mb-1">
                    Priority
                  </label>
                  <select
                    id="priority"
                    className="w-full rounded-md border border-input dark:border-input-dark bg-background dark:bg-background-dark px-3 py-2 text-sm"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                    <option value="critical">Critical</option>
                  </select>
                </div>
                
                <div>
                  <label htmlFor="category" className="block text-sm font-medium mb-1">
                    Category
                  </label>
                  <select
                    id="category"
                    className="w-full rounded-md border border-input dark:border-input-dark bg-background dark:bg-background-dark px-3 py-2 text-sm"
                  >
                    <option value="security-investigation">Security Investigation</option>
                    <option value="network-security">Network Security</option>
                    <option value="endpoint-security">Endpoint Security</option>
                    <option value="incident-response">Incident Response</option>
                    <option value="training">Training</option>
                  </select>
                </div>
                
                <div>
                  <label htmlFor="assigned" className="block text-sm font-medium mb-1">
                    Assigned To
                  </label>
                  <input
                    id="assigned"
                    type="text"
                    placeholder="User or team name"
                    className="w-full rounded-md border border-input dark:border-input-dark bg-background dark:bg-background-dark px-3 py-2 text-sm"
                  />
                </div>
                
                <div>
                  <label htmlFor="due-date" className="block text-sm font-medium mb-1">
                    Due Date
                  </label>
                  <input
                    id="due-date"
                    type="date"
                    className="w-full rounded-md border border-input dark:border-input-dark bg-background dark:bg-background-dark px-3 py-2 text-sm"
                  />
                </div>
              </div>
              
              <div className="flex justify-end gap-2">
                <Button variant="outline" onClick={() => setShowAddTask(false)}>
                  Cancel
                </Button>
                <Button>
                  Create Task
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground dark:text-muted-foreground-dark" />
          <input
            type="text"
            placeholder="Search tasks..."
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
            <option value="all">All tasks</option>
            <option value="pending">Pending</option>
            <option value="in progress">In Progress</option>
            <option value="completed">Completed</option>
            <option value="failed">Failed</option>
          </select>
        </div>
      </div>

      <div className="space-y-4">
        {filteredTasks.length === 0 ? (
          <div className="bg-card dark:bg-card-dark rounded-lg p-8 text-center">
            <p className="text-muted-foreground dark:text-muted-foreground-dark">
              No tasks found. Try adjusting your filters or create a new task.
            </p>
          </div>
        ) : (
          filteredTasks.map((task) => (
            <div
              key={task.id}
              className="bg-card dark:bg-card-dark rounded-lg border border-border dark:border-border-dark p-4 transition-all hover:shadow-md"
            >
              <div className="flex flex-col sm:flex-row justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    {getStatusIcon(task.status)}
                    <h3 className="font-medium">{task.title}</h3>
                    <span className={`ml-2 rounded-full px-2 py-0.5 text-xs font-medium ${getPriorityColor(task.priority)}`}>
                      {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
                    </span>
                  </div>
                  <p className="mt-1 text-sm text-muted-foreground dark:text-muted-foreground-dark">
                    {task.description}
                  </p>
                  <div className="mt-2 flex flex-wrap items-center text-xs text-muted-foreground dark:text-muted-foreground-dark gap-x-4 gap-y-1">
                    <span>Category: {task.category}</span>
                    <span>Created: {formatDate(task.createdAt)}</span>
                    {task.dueDate && <span>Due: {formatDate(task.dueDate)}</span>}
                    {task.assignedTo && <span>Assigned to: {task.assignedTo}</span>}
                  </div>
                </div>
                
                <div className="mt-4 sm:mt-0 flex items-center gap-2 self-end sm:self-start">
                  <div className="relative">
                    <button className="flex items-center rounded-md border border-input dark:border-input-dark bg-background dark:bg-background-dark px-3 py-1.5 text-sm">
                      Update Status <ChevronDown className="ml-2 h-3 w-3" />
                    </button>
                    <div className="absolute right-0 z-10 mt-1 hidden w-48 origin-top-right rounded-md bg-card dark:bg-card-dark border border-border dark:border-border-dark shadow-lg">
                      <div className="py-1">
                        <button 
                          className="block px-4 py-2 text-sm hover:bg-muted dark:hover:bg-muted-dark w-full text-left"
                          onClick={() => updateTaskStatus(task.id, 'pending')}
                        >
                          Pending
                        </button>
                        <button 
                          className="block px-4 py-2 text-sm hover:bg-muted dark:hover:bg-muted-dark w-full text-left"
                          onClick={() => updateTaskStatus(task.id, 'in progress')}
                        >
                          In Progress
                        </button>
                        <button 
                          className="block px-4 py-2 text-sm hover:bg-muted dark:hover:bg-muted-dark w-full text-left"
                          onClick={() => updateTaskStatus(task.id, 'completed')}
                        >
                          Completed
                        </button>
                        <button 
                          className="block px-4 py-2 text-sm hover:bg-muted dark:hover:bg-muted-dark w-full text-left"
                          onClick={() => updateTaskStatus(task.id, 'failed')}
                        >
                          Failed
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Tasks;