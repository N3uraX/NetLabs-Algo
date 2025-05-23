import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import Input from '../../components/ui/Input';
import Button from '../../components/ui/Button';
import { useAuth } from '../../contexts/AuthContext';

interface LoginFormValues {
  email: string;
  password: string;
  rememberMe: boolean;
}

const Login = () => {
  const { login } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormValues>({
    defaultValues: {
      email: '',
      password: '',
      rememberMe: false,
    },
  });
  
  const onSubmit = async (data: LoginFormValues) => {
    try {
      setIsLoading(true);
      setErrorMessage(null);
      await login(data.email, data.password);
    } catch (error) {
      console.error('Login failed:', error);
      setErrorMessage('Invalid email or password. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-foreground dark:text-foreground-dark">
          Email address
        </label>
        <div className="mt-1">
          <Input
            id="email"
            type="email"
            autoComplete="email"
            error={errors.email?.message}
            {...register('email', {
              required: 'Email is required',
              pattern: {
                value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                message: 'Invalid email address',
              },
            })}
          />
        </div>
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium text-foreground dark:text-foreground-dark">
          Password
        </label>
        <div className="mt-1">
          <Input
            id="password"
            type="password"
            autoComplete="current-password"
            error={errors.password?.message}
            {...register('password', {
              required: 'Password is required',
            })}
          />
        </div>
      </div>

      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <input
            id="remember-me"
            type="checkbox"
            className="h-4 w-4 rounded border-input dark:border-input-dark text-primary focus:ring-primary"
            {...register('rememberMe')}
          />
          <label htmlFor="remember-me" className="ml-2 block text-sm text-foreground dark:text-foreground-dark">
            Remember me
          </label>
        </div>

        <div className="text-sm">
          <a href="#" className="font-medium text-primary hover:text-primary-600">
            Forgot your password?
          </a>
        </div>
      </div>

      {errorMessage && (
        <div className="rounded-md bg-error/10 p-3">
          <p className="text-sm text-error">{errorMessage}</p>
        </div>
      )}

      <div>
        <Button type="submit" className="w-full" isLoading={isLoading}>
          Sign in
        </Button>
      </div>

      <div className="text-center text-sm">
        <p className="text-muted-foreground dark:text-muted-foreground-dark">
          Don't have an account?{' '}
          <Link to="/register" className="font-medium text-primary hover:text-primary-600">
            Sign up
          </Link>
        </p>
        
        {/* Demo credentials notice */}
        <div className="mt-4 p-2 rounded-md bg-muted dark:bg-muted-dark text-xs">
          <p className="font-medium">Demo Credentials</p>
          <p>Email: admin@netlabs.com</p>
          <p>Password: password</p>
        </div>
      </div>
    </form>
  );
};

export default Login;