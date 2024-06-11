'use client';
import Clock from '@/components/Clock';
import FarmCard from '@/components/FarmCard';
import { IFarm } from '@/interface/farm';
import axios from 'axios';
import { useEffect, useState } from 'react';

const farms_description = [
  {
    area: '1',
    name: 'Carrot Farm',
    description:
      'BKU Carrot Farm thrives on fertile, well-drained loamy soil and a temperate climate, ideal for carrot cultivation.',
    image: 'carot.jpg',
  },
  {
    area: '2',
    name: 'Lettuce Farm',
    description:
      'BKU Lettuce Farm flourishes with nutrient-rich, well-drained soil and a cool, temperate climate perfect for lettuce growth.',
    image: 'lettuce.jpg',
  },
  {
    area: '3',
    name: 'Tomato Farm',
    description:
      'Tomato Farm thrives on rich, well-drained soil and a warm, sunny climate ideal for tomato cultivation.',
    image: 'tomatoes.jpg',
  },
];

export default function Home() {
  const [data, setData] = useState<IFarm[]>();
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/all_process');
        const mergedData = response.data.map((farm: IFarm) => {
          const description = farms_description.find(
            (desc) => desc.area == farm.area
          );
          return description ? { ...farm, ...description } : farm;
        });
        console.log('Data:', mergedData);
        setData(mergedData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    // Fetch data immediately and then at intervals
    fetchData();
    const intervalId = setInterval(fetchData, 5000); // Pull every 5 seconds

    setConnected(true);

    // Cleanup interval on component unmount
    return () => {
      clearInterval(intervalId);
      setConnected(false);
    };
  }, []);

  return (
    <main className="container max-w-4xl mx-auto flex flex-col items-center justify-center mt-20 md:mt-0 md:h-screen">
      {connected && (
        <div>
          <Clock />
          <div className="flex flex-col md:flex-row gap-3">
            {data &&
              data.map((farm) => <FarmCard key={farm.area} farm={farm} />)}
          </div>
        </div>
      )}
    </main>
  );
}
