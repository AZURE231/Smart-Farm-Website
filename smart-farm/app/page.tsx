import FarmCard from '@/components/FarmCard';
import Image from 'next/image';

export default function Home() {
  return (
    <main className="container max-w-3xl mx-auto flex items-center justify-center h-screen">
      <div className="flex flex-col md:flex-row gap-3">
        <FarmCard />
        <FarmCard />
        <FarmCard />
      </div>
    </main>
  );
}
