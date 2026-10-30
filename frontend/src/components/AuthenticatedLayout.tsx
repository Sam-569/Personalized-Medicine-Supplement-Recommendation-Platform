import React, { useState, useEffect } from 'react';
import { NavLink, useNavigate, useLocation } from 'react-router-dom';
import {
  ShieldCheck,
  LayoutDashboard,
  Sliders,
  BookOpen,
  Clock,
  User as UserIcon,
  LogOut,
  Menu,
  X,
  Shield,
} from 'lucide-react';
import { setToken, http } from '../api';

interface AuthenticatedLayoutProps {
  children: React.ReactNode;
}

export const AuthenticatedLayout: React.FC<AuthenticatedLayoutProps> = ({ children }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [userEmail, setUserEmail] = useState<string>('');
  const navigate = useNavigate();
  const location = useLocation();

  // Close mobile drawer on route change
  useEffect(() => {
    setMobileMenuOpen(false);
  }, [location.pathname]);

  // Load current authenticated user info for account section
  useEffect(() => {
    http.get('/auth/me')
      .then((res) => {
        if (res.data?.email) {
          setUserEmail(res.data.email);
        }
      })
      .catch(() => {
        // Silently fallback if session is expired
      });
  }, []);

  const handleLogout = () => {
    setToken(null);
    navigate('/');
  };

  const navItems = [
    { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/profile', label: 'Health Profile', icon: Sliders },
    { to: '/catalogue', label: 'Catalogue', icon: BookOpen },
    { to: '/history', label: 'Evaluation History', icon: Clock },
    { to: '/settings', label: 'Account & Settings', icon: UserIcon },
  ];

  const getNavLinkClass = ({ isActive }: { isActive: boolean }) =>
    `group flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-medium transition-colors ${
      isActive
        ? 'bg-[#EEF3EE] text-[#244B38] font-semibold border-l-2 border-[#244B38]'
        : 'text-[#5A6056] hover:text-[#252923] hover:bg-[#F7F7F2]'
    }`;

  return (
    <div className="min-h-screen flex flex-col lg:flex-row bg-[#F7F7F2] text-[#252923]">
      {/* Mobile Header Bar */}
      <header className="lg:hidden sticky top-0 z-40 flex h-14 items-center justify-between border-b border-[#E5E5DD] bg-white px-4">
        <NavLink to="/dashboard" className="flex items-center gap-2 text-[#252923]">
          <div className="flex h-7 w-7 items-center justify-center rounded-md bg-[#244B38] text-white">
            <ShieldCheck className="h-4 w-4" aria-hidden="true" />
          </div>
          <span className="text-sm font-bold tracking-tight">Supplement Guidance</span>
        </NavLink>

        <button
          type="button"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="flex h-9 w-9 items-center justify-center rounded-lg border border-[#E5E5DD] text-[#5A6056] hover:bg-[#F7F7F2] hover:text-[#252923] transition-colors cursor-pointer"
          aria-label={mobileMenuOpen ? 'Close navigation menu' : 'Open navigation menu'}
          aria-expanded={mobileMenuOpen}
        >
          {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </header>

      {/* Mobile Drawer Backdrop */}
      {mobileMenuOpen && (
        <div
          className="lg:hidden fixed inset-0 z-40 bg-black/20 backdrop-blur-xs transition-opacity"
          onClick={() => setMobileMenuOpen(false)}
          aria-hidden="true"
        />
      )}

      {/* Mobile Navigation Drawer */}
      <div
        className={`lg:hidden fixed inset-y-0 left-0 z-50 w-64 bg-white border-r border-[#E5E5DD] flex flex-col transform transition-transform duration-200 ease-in-out ${
          mobileMenuOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
        role="dialog"
        aria-label="Navigation drawer"
      >
        <div className="flex h-14 items-center justify-between border-b border-[#E5E5DD] px-4">
          <div className="flex items-center gap-2">
            <div className="flex h-7 w-7 items-center justify-center rounded-md bg-[#244B38] text-white">
              <ShieldCheck className="h-4 w-4" aria-hidden="true" />
            </div>
            <div>
              <span className="text-xs font-bold text-[#252923] block leading-tight">Supplement Guidance</span>
              <span className="text-[10px] text-[#73796F] block tracking-wide">Platform v1.0</span>
            </div>
          </div>
          <button
            type="button"
            onClick={() => setMobileMenuOpen(false)}
            className="p-1.5 rounded-md text-[#73796F] hover:bg-[#F7F7F2] hover:text-[#252923] cursor-pointer"
            aria-label="Close menu"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-1">
          <div className="px-3 pb-2 text-[10px] font-bold uppercase tracking-wider text-[#73796F]">
            Navigation
          </div>
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                className={getNavLinkClass}
                onClick={() => setMobileMenuOpen(false)}
              >
                <Icon className="h-4 w-4 shrink-0" aria-hidden="true" />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </nav>

        <div className="border-t border-[#E5E5DD] p-3 space-y-2 bg-[#F7F7F2]/50">
          <div className="px-2 py-1 text-xs">
            <span className="text-[10px] text-[#73796F] block uppercase tracking-wider font-semibold">User Session</span>
            <span className="text-xs font-medium text-[#252923] truncate block" title={userEmail}>
              {userEmail || 'Active User'}
            </span>
          </div>
          <button
            type="button"
            onClick={handleLogout}
            className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-medium text-[#9E2A2B] hover:bg-[#FDF2F2] transition-colors cursor-pointer"
          >
            <LogOut className="h-4 w-4" aria-hidden="true" />
            <span>Sign Out</span>
          </button>
        </div>
      </div>

      {/* Desktop Sidebar */}
      <aside className="hidden lg:flex lg:flex-col lg:w-60 lg:shrink-0 lg:sticky lg:top-0 lg:h-screen border-r border-[#E5E5DD] bg-white">
        {/* Sidebar Brand Header */}
        <div className="flex h-16 items-center border-b border-[#E5E5DD] px-5 gap-2.5">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-[#244B38] text-white shadow-2xs">
            <ShieldCheck className="h-4.5 w-4.5" aria-hidden="true" />
          </div>
          <div>
            <span className="text-xs font-bold text-[#252923] block leading-tight tracking-tight">
              Supplement Guidance
            </span>
            <span className="text-[10px] font-medium text-[#73796F] block tracking-wide uppercase">
              Deterministic Platform
            </span>
          </div>
        </div>

        {/* Sidebar Navigation */}
        <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-1">
          <div className="px-3 pb-2 text-[10px] font-bold uppercase tracking-wider text-[#73796F]">
            Main Menu
          </div>
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink key={item.to} to={item.to} className={getNavLinkClass}>
                <Icon className="h-4 w-4 shrink-0" aria-hidden="true" />
                <span>{item.label}</span>
              </NavLink>
            );
          })}

          <div className="pt-6 px-3">
            <div className="rounded-lg border border-[#E5E5DD] bg-[#F7F7F2] p-2.5 space-y-1">
              <div className="flex items-center gap-1.5 text-[11px] font-semibold text-[#244B38]">
                <Shield className="h-3.5 w-3.5 text-[#244B38]" aria-hidden="true" />
                <span>Safety Incompleteness</span>
              </div>
              <p className="text-[10px] text-[#73796F] leading-tight">
                Rule R000 enforced. Unverified candidates route to review.
              </p>
            </div>
          </div>
        </nav>

        {/* Sidebar Account & Logout */}
        <div className="border-t border-[#E5E5DD] p-3 space-y-2 bg-[#F7F7F2]/40">
          <div className="flex items-center justify-between px-2 py-1">
            <div className="min-w-0 flex-1">
              <span className="text-[10px] font-semibold uppercase tracking-wider text-[#73796F] block">
                Account
              </span>
              <span className="text-xs font-medium text-[#252923] truncate block" title={userEmail}>
                {userEmail || 'Active Session'}
              </span>
            </div>
            <button
              type="button"
              onClick={handleLogout}
              className="p-1.5 rounded-md text-[#73796F] hover:text-[#9E2A2B] hover:bg-[#FDF2F2] transition-colors cursor-pointer"
              title="Sign Out"
              aria-label="Sign Out"
            >
              <LogOut className="h-4 w-4" aria-hidden="true" />
            </button>
          </div>
          <div className="px-2 pt-1 border-t border-[#E5E5DD]/70 text-[10px] text-[#9A9F96]">
            Group 101 · Capstone SRS v1.0
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 min-w-0 overflow-y-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto w-full">
          {children}
        </div>
      </main>
    </div>
  );
};
