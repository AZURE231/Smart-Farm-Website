'use client';
import Clock from '@/components/Clock';
import FarmCard from '@/components/FarmCard';
import { IFarm } from '@/interface/farm';
import axios from 'axios';
import mqtt, { IClientOptions, MqttClient } from 'mqtt';
import { useEffect, useState } from 'react';

const options: IClientOptions = {
  host: 'mqttserver.tk',
  port: 9001,
  username: 'innovation',
  password: 'Innovation_RgPQAZoA5N',
};

const initialFarms: IFarm[] = [
  {
    area: '1',
    name: 'Carrot Farm',
    description:
      'BKU Carrot Farm thrives on fertile, well-drained loamy soil and a temperate climate, ideal for carrot cultivation.',
    image: 'carot.jpg',
    process: [],
  },
  {
    area: '2',
    name: 'Letttuce Farm',
    description:
      'BKU Lettuce Farm flourishes with nutrient-rich, well-drained soil and a cool, temperate climate perfect for lettuce growth.',
    image: 'lettuce.jpg',
    process: [],
  },
  {
    area: '3',
    name: 'Tomato Farm',
    description:
      'Tomato Farm thrives on rich, well-drained soil and a warm, sunny climate ideal for tomato cultivation.',
    image: 'tomatoes.jpg',
    process: [],
  },
];

export default function Home() {
  const [farms, setFarms] = useState<IFarm[]>(initialFarms);
  const [connected, setConnected] = useState(false);
  const [messages, setMessages] = useState<string[]>([]);
  const [client, setClient] = useState<MqttClient | null>(null);

  useEffect(() => {
    const mqttClient = mqtt.connect(options);

    mqttClient.on('connect', () => {
      console.log('Connected to MQTT broker');
      setClient(mqttClient);
      setConnected(true);
      mqttClient.subscribe(
        '/innovation/pumpcontroller/smartfarm/update',
        (err) => {
          if (err) {
            console.error('Subscription error:', err);
          } else {
            console.log('Subscribed to topic');
          }
        }
      );
    });

    mqttClient.on('message', (topic, message) => {
      console.log('Received on topic:', topic);
      console.log('Received message:', message.toString());

      const data = JSON.parse(message.toString());
      updateFarmsProcess(data);
      console.log('Farms!!!!!!!!!!!!!!!!!!!');
      setMessages((prevMessages) => [...prevMessages, message.toString()]);
    });

    mqttClient.on('error', (err) => {
      console.error('Connection error: ', err);
      mqttClient.end();
    });

    return () => {
      if (mqttClient) {
        mqttClient.end();
      }
    };
  }, []);

  const updateFarmsProcess = (data: { area: number; process: any[] }[]) => {
    setFarms((prevFarms) =>
      prevFarms.map((farm) => {
        const updatedFarm = data.find(
          (item) => item.area === parseInt(farm.area)
        );
        if (updatedFarm) {
          return {
            ...farm,
            process: updatedFarm.process,
          };
        }
        return farm;
      })
    );
  };

  return (
    <main className="container max-w-4xl mx-auto flex flex-col items-center justify-center mt-20 md:mt-0 md:h-screen">
      <div>
        <Clock />
        <div className="flex flex-col md:flex-row gap-3">
          {farms &&
            farms.map((farm) => (
              <FarmCard key={farm.area} farm={farm} client={client} />
            ))}
        </div>
      </div>
    </main>
  );
}
