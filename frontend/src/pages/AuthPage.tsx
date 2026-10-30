import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { ShieldCheck, Lock, Mail, AlertCircle, ArrowRight } from 'lucide-react';
import { http, setToken, errMsg } from '../api';

const authSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters long').max(72, 'Password cannot exceed 72 characters'),
});

type AuthFormData = z.infer<typeof authSchema>;

export const AuthPage: React.FC = () => {
  const [isRegister, setIsRegister] = useState(false);
  const [serverError, setServerError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<AuthFormData>({
    resolver: zodResolver(authSchema),
  });

  const onSubmit = async (data: AuthFormData) => {
    setServerError('');
    setIsLoading(true);
    try {
      const endpoint = isRegister ? '/auth/register' : '/auth/login';
      const res = await http.post(endpoint, data);
      if (res.data?.token) {
        setToken(res.data.token);
        navigate('/dashboard');
      } else {
        setServerError('Authentication failed: No session token received.');
      }
    } catch (err: any) {
      setServerError(errMsg(err));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-md py-8">
      <div className="rounded-2xl border border-[#E5E5DD] bg-white p-8 shadow-2xs">
        <div className="text-center mb-6">
          <div className="mx-auto flex h-11 w-11 items-center justify-center rounded-xl bg-[#EEF3EE] text-[#244B38] mb-3 shadow-2xs">
            <ShieldCheck className="h-5 w-5" aria-hidden="true" />
          </div>
          <h2 className="text-xl font-bold text-[#252923]">
            {isRegister ? 'Create Your Account' : 'Welcome Back'}
          </h2>
          <p className="mt-1 text-xs text-[#73796F]">
            {isRegister
              ? 'Register to complete your profile and explore personalized guidance.'
              : 'Sign in to access your dashboard, saved profile, and recommendation history.'}
          </p>
        </div>

        {/* Tab Switcher */}
        <div className="grid grid-cols-2 rounded-xl bg-slate-100 p-1 mb-6 text-sm font-medium">
          <button
            type="button"
            onClick={() => {
              setIsRegister(false);
              setServerError('');
            }}
            className={`py-2 rounded-lg transition cursor-pointer ${
              !isRegister
                ? 'bg-white text-slate-900 font-semibold shadow-2xs'
                : 'text-slate-500 hover:text-slate-800'
            }`}
          >
            Sign In
          </button>
          <button
            type="button"
            onClick={() => {
              setIsRegister(true);
              setServerError('');
            }}
            className={`py-2 rounded-lg transition cursor-pointer ${
              isRegister
                ? 'bg-white text-slate-900 font-semibold shadow-2xs'
                : 'text-slate-500 hover:text-slate-800'
            }`}
          >
            Register
          </button>
        </div>

        {serverError && (
          <div className="mb-5 flex items-start gap-2.5 rounded-xl border border-rose-200 bg-rose-50 p-3 text-xs text-rose-800">
            <AlertCircle className="h-4 w-4 shrink-0 text-rose-600 mt-0.5" />
            <span>{serverError}</span>
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1" htmlFor="email">
              Email Address
            </label>
            <div className="relative">
              <Mail className="absolute left-3 top-3 h-4 w-4 text-slate-400" />
              <input
                id="email"
                type="email"
                autoComplete="email"
                placeholder="user@example.com"
                {...register('email')}
                className="w-full rounded-xl border border-slate-300 py-2.5 pl-10 pr-3 text-sm text-slate-900 placeholder:text-slate-400 focus:border-teal-600 focus:outline-none focus:ring-2 focus:ring-teal-100"
              />
            </div>
            {errors.email && (
              <p className="mt-1 text-xs text-rose-600">{errors.email.message}</p>
            )}
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1" htmlFor="password">
              Password
            </label>
            <div className="relative">
              <Lock className="absolute left-3 top-3 h-4 w-4 text-slate-400" />
              <input
                id="password"
                type="password"
                autoComplete={isRegister ? 'new-password' : 'current-password'}
                placeholder="At least 8 characters"
                {...register('password')}
                className="w-full rounded-xl border border-slate-300 py-2.5 pl-10 pr-3 text-sm text-slate-900 placeholder:text-slate-400 focus:border-teal-600 focus:outline-none focus:ring-2 focus:ring-teal-100"
              />
            </div>
            {errors.password && (
              <p className="mt-1 text-xs text-rose-600">{errors.password.message}</p>
            )}
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full mt-2 flex items-center justify-center gap-2 rounded-lg bg-[#244B38] py-2.5 text-sm font-semibold text-white shadow-2xs hover:bg-[#1B382A] active:bg-[#14291F] transition-colors disabled:opacity-50 cursor-pointer"
          >
            {isLoading ? (
              <span>Authenticating...</span>
            ) : (
              <>
                <span>{isRegister ? 'Create Account' : 'Sign In'}</span>
                <ArrowRight className="h-4 w-4" />
              </>
            )}
          </button>
        </form>

        <div className="mt-6 border-t border-[#E5E5DD] pt-4 text-center">
          <p className="text-xs text-[#73796F]">
            {isRegister ? 'Already have an account?' : "Don't have an account yet?"}{' '}
            <button
              type="button"
              onClick={() => {
                setIsRegister(!isRegister);
                setServerError('');
              }}
              className="font-semibold text-teal-700 hover:underline cursor-pointer"
            >
              {isRegister ? 'Sign In here' : 'Register now'}
            </button>
          </p>
        </div>

        <div className="mt-6 rounded-xl bg-slate-50 p-3 text-[11px] text-slate-500 border border-slate-200/80">
          <strong>Security note:</strong> Passwords are cryptographically hashed using salted bcrypt on the backend. Sessions use signed HS256 JWT tokens with automatic expiry.
        </div>
      </div>
    </div>
  );
};

