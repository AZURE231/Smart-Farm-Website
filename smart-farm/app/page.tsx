import FarmCard from '@/components/FarmCard';
import Image from 'next/image';

const farms = [
  {
    id: '1',
    name: 'Farm 1',
    description: 'Farm 1 description',
    image: 'carot.jpg',
    details: {
      id: '1',
      mixer_1: 'mixer 1',
      mixer_2: 'mixer 2',
      mixer_3: 'mixer 3',
      start_time: '12:00',
      end_time: '18:00',
      date: '2021-10-10',
      isActivated: true,
      cycle: 1,
    },
  },
  {
    id: '2',
    name: 'Farm 2',
    description: 'Farm 2 description',
    image: 'letttuce.jpg',
    details: {
      id: '2',
      mixer_1: 'mixer 1',
      mixer_2: 'mixer 2',
      mixer_3: 'mixer 3',
      start_time: '12:00',
      end_time: '18:00',
      date: '2021-10-10',
      isActivated: true,
      cycle: 1,
    },
  },
  {
    id: '3',
    name: 'Farm 3',
    description: 'Farm 3 description',
    image: 'tomatoes.jpg',
    details: {
      id: '3',
      mixer_1: 'mixer 1',
      mixer_2: 'mixer 2',
      mixer_3: 'mixer 3',
      start_time: '12:00',
      end_time: '18:00',
      date: '2021-10-10',
      isActivated: true,
      cycle: 1,
    },
  },
];

export default function Home() {
  return (
    <main className="container max-w-4xl mx-auto flex items-center justify-center h-screen">
      <div className="flex flex-col md:flex-row gap-3">
        {farms.map((farm) => (
          <FarmCard key={farm.id} farm={farm} />
        ))}
      </div>
    </main>
  );
}
