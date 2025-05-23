import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(date: Date): string {
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date);
}

export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return `${text.slice(0, maxLength)}...`;
}

export function generateId(): string {
  return Math.random().toString(36).substring(2, 9);
}

export function getStatusColor(status: string): string {
  switch (status.toLowerCase()) {
    case 'critical':
      return 'text-error';
    case 'high':
      return 'text-orange-500';
    case 'medium':
      return 'text-warning';
    case 'low':
      return 'text-secondary';
    case 'info':
      return 'text-primary';
    case 'completed':
    case 'secure':
      return 'text-success';
    case 'in progress':
      return 'text-primary';
    case 'pending':
      return 'text-muted-foreground';
    case 'failed':
      return 'text-error';
    default:
      return 'text-foreground';
  }
}