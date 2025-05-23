import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import Input from '../../components/ui/Input';
import Button from '../../components/ui/Button';
import { useAuth } from '../../contexts/AuthContext';

interface RegisterFormValues {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
  termsAndConditions: boolean;
}

const Register = () => {
  const { register: registerUser } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<RegisterFormValues>({
    defaultValues: {
      name: '',
      email: '',
      password: '',
      confirmPassword: '',
      termsAndConditions: false,
    },
  });
  
  const password = watch('password');
  
  const onSubmit = async (data: RegisterFormValues) => {
    try {
      setIsLoading(true);
      setErrorMessage(null);
      await registerUser(data.name, data.email, data.password);
    } catch (error) {
      console.error('Registration failed:', error);
      setErrorMessage('Registration failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label htmlFor="name" className="block text-sm font-medium text-foreground dark:text-foreground-dark">
          Full name
        </label>
        <div className="mt-1">
          <Input
            id="name"
            type="text"
            autoComplete="name"
            error={errors.name?.message}
            {...register('name', {
              required: 'Name is required',
            })}
          />
        </div>
      </div>

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
            autoComplete="new-password"
            error={errors.password?.message}
            {...register('password', {
              required: 'Password is required',
              minLength: {
                value: 8,
                message: 'Password must be at least 8 characters',
              },
            })}
          />
        </div>
      </div>

      <div>
        <label htmlFor="confirmPassword" className="block text-sm font-medium text-foreground dark:text-foreground-dark">
          Confirm password
        </label>
        <div className="mt-1">
          <Input
            id="confirmPassword"
            type="password"
            autoComplete="new-password"
            error={errors.confirmPassword?.message}
            {...register('confirmPassword', {
              required: 'Please confirm your password',
              validate: (value) => value === password || 'Passwords do not match',
            })}
          />
        </div>
      </div>

      <div className="flex items-center">
        <input
          id="terms"
          type="checkbox"
          className="h-4 w-4 rounded border-input dark:border-input-dark text-primary focus:ring-primary"
          {...register('termsAndConditions', {
            required: 'You must agree to the terms and conditions',
          })}
        />
        <label htmlFor="terms" className="ml-2 block text-sm text-foreground dark:text-foreground-dark">
          I agree to the{' '}
          <a href="#" className="font-medium text-primary hover:text-primary-600">
            terms and conditions
          </a>
        </label>
      </div>
      {errors.termsAndConditions && (
        <p className="text-sm text-error">{errors.termsAndConditions.message}</p>
      )}

      {errorMessage && (
        <div className="rounded-md bg-error/10 p-3">
          <p className="text-sm text-error">{errorMessage}</p>
        </div>
      )}

      <div>
        <Button type="submit" className="w-full" isLoading={isLoading}>
          Sign up
        </Button>
      </div>

      <div className="text-center text-sm">
        <p className="text-muted-foreground dark:text-muted-foreground-dark">
          Already have an account?{' '}
          <Link to="/login" className="font-medium text-primary hover:text-primary-600">
            Sign in
          </Link>
        </p>
      </div>
    </form>
  );
};

export default Register;