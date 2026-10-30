import React from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { ShieldCheck, LogOut, User as UserIcon, BookOpen, Clock, LayoutDashboard, Sliders } from 'lucide-react';
import { getToken, setToken } from '../api';

export const Navbar: React.FC = () => {
  const token = getToken();
  const navigate = useNavigate();

  const handleLogout = () => {
    setToken(null);
    navigate('/');
  };

  const navLinkClass = ({ isActive }: { isActive: boolean }) =>
    `flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
      isActive
        ? 'bg-[#EEF3EE] text-[#244B38] font-semibold'
        : 'text-[#5A6056] hover:text-[#252923] hover:bg-[#F7F7F2]'
    }`;

  return (
    <header className="sticky top-0 z-40 border-b border-[#E5E5DD] bg-white">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3 sm:px-6">
        <Link to="/" className="flex items-center gap-2.5 text-[#252923] hover:opacity-95 transition-opacity">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-[#244B38] text-white shadow-2xs">
            <ShieldCheck className="h-4 w-4" aria-hidden="true" />
          </div>
          <div>
            <span className="text-sm font-bold tracking-tight text-[#252923] block leading-tight">
              Supplement Guidance
            </span>
            <span className="text-[10px] font-medium text-[#73796F] block tracking-wider uppercase">
              Open Source Platform
            </span>
          </div>
        </Link>

        <nav className="flex items-center gap-1 sm:gap-2">
          {token ? (
            <>
              <NavLink to="/dashboard" className={navLinkClass}>
                <LayoutDashboard className="h-3.5 w-3.5" aria-hidden="true" />
                <span className="hidden sm:inline">Dashboard</span>
              </NavLink>
              <NavLink to="/profile" className={navLinkClass}>
                <Sliders className="h-3.5 w-3.5" aria-hidden="true" />
                <span className="hidden sm:inline">Profile</span>
              </NavLink>
              <NavLink to="/catalogue" className={navLinkClass}>
                <BookOpen className="h-3.5 w-3.5" aria-hidden="true" />
                <span>Catalogue</span>
              </NavLink>
              <NavLink to="/history" className={navLinkClass}>
                <Clock className="h-3.5 w-3.5" aria-hidden="true" />
                <span className="hidden sm:inline">History</span>
              </NavLink>
              <NavLink to="/settings" className={navLinkClass} title="Account and Settings">
                <UserIcon className="h-3.5 w-3.5" aria-hidden="true" />
                <span className="hidden md:inline">Account</span>
              </NavLink>
              <button
                type="button"
                onClick={handleLogout}
                className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-medium text-[#9E2A2B] hover:bg-[#FDF2F2] transition-colors cursor-pointer"
                title="Log out"
              >
                <LogOut className="h-3.5 w-3.5" aria-hidden="true" />
                <span className="hidden sm:inline">Logout</span>
              </button>
            </>
          ) : (
            <>
              <NavLink to="/catalogue" className={navLinkClass}>
                <BookOpen className="h-3.5 w-3.5" aria-hidden="true" />
                <span>Catalogue</span>
              </NavLink>
              <Link
                to="/login"
                className="ml-2 inline-flex items-center justify-center rounded-lg bg-[#244B38] px-3.5 py-1.5 text-xs font-semibold text-white shadow-2xs hover:bg-[#1B382A] active:bg-[#14291F] transition-colors cursor-pointer"
              >
                Sign In / Register
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
};
