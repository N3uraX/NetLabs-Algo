import { Outlet, Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Shield } from 'lucide-react';

const AuthLayout = () => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div className="flex items-center justify-center h-screen">Loading...</div>;
  }

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  return (
    <div className="min-h-screen flex flex-col justify-center py-12 sm:px-6 lg:px-8 bg-gradient-to-br from-background dark:from-background-dark to-background dark:to-background-dark">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-center">
          <Shield className="h-12 w-12 text-primary" />
        </div>
        <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-foreground dark:text-foreground-dark">
          NetLabs Algo
        </h2>
        <p className="mt-2 text-center text-sm text-muted-foreground dark:text-muted-foreground-dark">
          Advanced Cybersecurity Toolkit
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-card dark:bg-card-dark py-8 px-4 shadow sm:rounded-lg sm:px-10 border border-border dark:border-border-dark">
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default AuthLayout;