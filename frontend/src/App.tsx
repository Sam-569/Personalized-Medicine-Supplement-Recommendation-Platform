import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { PublicLayout } from './components/PublicLayout';
import { AuthenticatedLayout } from './components/AuthenticatedLayout';
import { LandingPage } from './pages/LandingPage';
import { AuthPage } from './pages/AuthPage';
import { DashboardPage } from './pages/DashboardPage';
import { ProfilePage } from './pages/ProfilePage';
import { CataloguePage } from './pages/CataloguePage';
import { ResultsPage } from './pages/ResultsPage';
import { HistoryPage } from './pages/HistoryPage';
import { SettingsPage } from './pages/SettingsPage';
import { getToken } from './api';

function ProtectedRoute({ children }: { children: JSX.Element }) {
  const token = getToken();
  return token ? children : <Navigate to="/login" replace />;
}

export default function App() {
  const token = getToken();

  return (
    <Routes>
      {/* Public Pages */}
      <Route
        path="/"
        element={
          token ? (
            <Navigate to="/dashboard" replace />
          ) : (
            <PublicLayout>
              <LandingPage />
            </PublicLayout>
          )
        }
      />
      <Route
        path="/login"
        element={
          token ? (
            <Navigate to="/dashboard" replace />
          ) : (
            <PublicLayout>
              <AuthPage />
            </PublicLayout>
          )
        }
      />

      {/* Catalogue: adapts layout whether user is authenticated or public */}
      <Route
        path="/catalogue"
        element={
          token ? (
            <AuthenticatedLayout>
              <CataloguePage />
            </AuthenticatedLayout>
          ) : (
            <PublicLayout>
              <CataloguePage />
            </PublicLayout>
          )
        }
      />

      {/* Authenticated Pages */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <AuthenticatedLayout>
              <DashboardPage />
            </AuthenticatedLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/profile"
        element={
          <ProtectedRoute>
            <AuthenticatedLayout>
              <ProfilePage />
            </AuthenticatedLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/runs/:id"
        element={
          <ProtectedRoute>
            <AuthenticatedLayout>
              <ResultsPage />
            </AuthenticatedLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/history"
        element={
          <ProtectedRoute>
            <AuthenticatedLayout>
              <HistoryPage />
            </AuthenticatedLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/settings"
        element={
          <ProtectedRoute>
            <AuthenticatedLayout>
              <SettingsPage />
            </AuthenticatedLayout>
          </ProtectedRoute>
        }
      />

      {/* Fallback */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
