'use client';
import Clock from '@/components/Clock';
import FarmCard from '@/components/FarmCard';
import { IFarm } from '@/interface/farm';
import axios from 'axios';
import mqtt, { IClientOptions, MqttClient } from 'mqtt';
import { useEffect, useState } from 'react';
import { set } from 'react-hook-form';

export const options: IClientOptions = {
  host: 'mqttserver.tk',
  port: 9001,
  username: 'innovation',
  password: 'Innovation_RgPQAZoA5N',
};

const farms: IFarm[] = [
  {
    area: '1',
    name: 'Carot Farm',
    description:
      'BKU Carrot Farm thrives on fertile, well-drained loamy soil and a temperate climate, ideal for carrot cultivation. We utilize organic farming methods, including compost fertilization and drip irrigation, ensuring high-quality produce. Our sustainable practices, such as crop rotation and eco-friendly packaging, promote environmental stewardship while delivering fresh, delicious carrots to our customers.',
    image: 'carot.jpg',
    process: [
      {
        cycle: 2,
        end_time: '09/06/2024 14:55:00',
        id: '5',
        init_mixer: [0, 200, 100],
        isActive: false,
        isCompleted: true,
        mixer: [0.0, 0, 0.0],
        start_time: '09/06/2024 14:41:00',
      },
      {
        cycle: 1,
        end_time: '09/06/2024 09:40:00',
        id: '3',
        init_mixer: [100, 200, 300],
        isActive: false,
        isCompleted: true,
        mixer: [0.0, 0.0, 0],
        start_time: '09/06/2024 09:30:00',
      },
    ],
  },
  {
    area: '2',
    name: 'Carot Farm',
    description:
      'BKU Carrot Farm thrives on fertile, well-drained loamy soil and a temperate climate, ideal for carrot cultivation. We utilize organic farming methods, including compost fertilization and drip irrigation, ensuring high-quality produce. Our sustainable practices, such as crop rotation and eco-friendly packaging, promote environmental stewardship while delivering fresh, delicious carrots to our customers.',
    image: 'carot.jpg',
    process: [
      {
        cycle: 1,
        end_time: '09/06/2024 15:40:00',
        id: '4',
        init_mixer: [200, 0, 200],
        isActive: false,
        isCompleted: true,
        mixer: [0, 0.0, 0.0],
        start_time: '09/06/2024 14:30:00',
      },
    ],
  },
  {
    area: '3',
    name: 'Carot Farm',
    description:
      'BKU Carrot Farm thrives on fertile, well-drained loamy soil and a temperate climate, ideal for carrot cultivation. We utilize organic farming methods, including compost fertilization and drip irrigation, ensuring high-quality produce. Our sustainable practices, such as crop rotation and eco-friendly packaging, promote environmental stewardship while delivering fresh, delicious carrots to our customers.',
    image: 'carot.jpg',
    process: [
      {
        cycle: 3,
        end_time: '10/06/2024 10:15:00',
        id: '6',
        init_mixer: [0, 200, 300],
        isActive: false,
        isCompleted: true,
        mixer: [0.0, 0.0, 0],
        start_time: '10/06/2024 10:00:00',
      },
      {
        cycle: 2,
        end_time: '09/06/2024 12:55:00',
        id: '1',
        init_mixer: [0, 100, 100],
        isActive: false,
        isCompleted: true,
        mixer: [0.0, 0, 0.0],
        start_time: '09/06/2024 12:40:00',
      },
    ],
  },
];

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
  const [messages, setMessages] = useState<string[]>([]);
  const [client, setClient] = useState<MqttClient | null>(null);

  useEffect(() => {
    const client = mqtt.connect(options);

    client.on('message', (message) => {
      setMessages(messages.concat(message.toString()));
    });

    client.on('connect', () => {
      console.log('Connected to MQTT broker');
      setClient(client);
    });

    client.on('error', (err: Error) => {
      console.error('Connection error: ', err);
      client?.end();
    });

    client.subscribe('/innovation/pumpcontroller/WSNs');

    return () => {
      if (client) {
        client.unsubscribe('test');
        client.end();
      }
    };
  }, []);

  // useEffect(() => {
  //   const fetchData = async () => {
  //     try {
  //       const response = await axios.get('http://127.0.0.1:8000/all_process');
  //       const mergedData = response.data.map((farm: IFarm) => {
  //         const description = farms_description.find(
  //           (desc) => desc.area == farm.area
  //         );
  //         return description ? { ...farm, ...description } : farm;
  //       });
  //       console.log('Data:', mergedData);
  //       setData(mergedData);
  //     } catch (error) {
  //       console.error('Error fetching data:', error);
  //     }
  //   };

  //   // Fetch data immediately and then at intervals
  //   fetchData();
  //   const intervalId = setInterval(fetchData, 5000); // Pull every 5 seconds

  //   setConnected(true);

  //   // Cleanup interval on component unmount
  //   return () => {
  //     clearInterval(intervalId);
  //     setConnected(false);
  //   };
  // }, []);

  return (
    <main className="container max-w-4xl mx-auto flex flex-col items-center justify-center mt-20 md:mt-0 md:h-screen">
      {
        <div>
          <Clock />
          <div className="flex flex-col md:flex-row gap-3">
            {farms &&
              farms.map((farm) => (
                <FarmCard key={farm.area} farm={farm} client={client} />
              ))}
          </div>
        </div>
      }
    </main>
  );
}
