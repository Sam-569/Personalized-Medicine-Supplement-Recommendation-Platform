import React from 'react';
import { Navbar } from './Navbar';
import { Footer } from './Footer';

interface PublicLayoutProps {
  children: React.ReactNode;
}

export const PublicLayout: React.FC<PublicLayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen flex flex-col bg-[#F7F7F2] text-[#252923]">
      <Navbar />
      <main className="flex-1 mx-auto w-full max-w-6xl px-4 py-8 sm:px-6">
        {children}
      </main>
      <Footer />
    </div>
  );
};
