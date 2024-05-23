'use client';
import React, { useState } from 'react';

const Clock = () => {
  // For digital clock
  let time = new Date().toLocaleTimeString();
  let [ctime, setCTime] = useState<string>();
  const updateTime = () => {
    time = new Date().toLocaleTimeString();
    setCTime(time);
  };
  setInterval(updateTime, 1000);
  return (
    <div className="w-full text-right">
      <h2 className="font-bold text-3xl mb-5"> {ctime}.</h2>
    </div>
  );
};
export default Clock;
