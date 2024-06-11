import { IFarmDetail } from '@/interface/farm';
import { SvgIcon } from '@mui/material';
import Typography from '@mui/material/Typography';
import React from 'react';
import LinearProgressWithLabel from './LinearProgressWithLabel';

export default function CycleCard({
  cycleDetails,
}: {
  cycleDetails: IFarmDetail;
}) {
  const handleDelete = () => {
    console.log('delete');
  };
  return (
    <div
      className={`relative mt-5 ${
        cycleDetails.isActive
          ? 'bg-green-300'
          : cycleDetails.isCompleted
          ? 'bg-gray-300'
          : 'bg-gray-100'
      } rounded-lg p-3`}
    >
      <Typography variant="body2" color="text.secondary">
        Time: {cycleDetails.start_time} - {cycleDetails.end_time}
      </Typography>
      <Typography variant="body2" color="text.secondary">
        Cycle: {cycleDetails.cycle}
      </Typography>
      {cycleDetails.isActive && <LinearProgressWithLabel />}

      <div className="absolute top-2 right-2">
        <button
          className="bg-gray-300 rounded-full p-1 hover:bg-blue-400 hover:text-black"
          onClick={handleDelete}
        >
          <SvgIcon>
            {/* credit: plus icon from https://heroicons.com/ */}
            <svg
              xmlns="http://www.w3.org/2000/svg"
              height="24px"
              viewBox="0 0 24 24"
              width="24px"
              fill="#5f6368"
            >
              <path d="M0 0h24v24H0V0z" fill="none" />
              <path d="M14.12 10.47L12 12.59l-2.13-2.12-1.41 1.41L10.59 14l-2.12 2.12 1.41 1.41L12 15.41l2.12 2.12 1.41-1.41L13.41 14l2.12-2.12zM15.5 4l-1-1h-5l-1 1H5v2h14V4zM6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM8 9h8v10H8V9z" />
            </svg>
          </SvgIcon>
        </button>
      </div>
    </div>
  );
}
