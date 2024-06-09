'use client';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { IFarm } from '@/interface/farm';
import FarmDetailModal from './FarmDetailModal';
import { useState } from 'react';
import Divider from '@mui/material/Divider';
import CycleCard from './CycleCard';
import { Fab, SvgIcon } from '@mui/material';

export default function FarmCard({ farm }: { farm: IFarm }) {
  const [open, setOpen] = useState(false);
  const handleInit = () => setOpen(true);
  return (
    <Card sx={{ maxWidth: 500 }}>
      <CardMedia
        component="img"
        alt={farm.name}
        className="h-60 w-full object-cover"
        image={farm.image}
      />
      <CardContent>
        <Typography gutterBottom variant="h5" component="div">
          {farm.name}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {farm.description}
        </Typography>
        <Divider className="mt-5" />
        {farm.details &&
          farm.details.map((detail) => (
            <CycleCard key={detail.id} cycleDetails={detail} />
          ))}
      </CardContent>
      <CardActions>
        <Button size="small" onClick={handleInit}>
          <Fab color="success" aria-label="add" size="medium">
            <SvgIcon>
              {/* credit: plus icon from https://heroicons.com/ */}
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="24px"
                viewBox="0 0 24 24"
                width="24px"
                fill="#ffffff"
              >
                <path d="M0 0h24v24H0V0z" fill="none" />
                <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" />
              </svg>
            </SvgIcon>
          </Fab>
        </Button>
        {/* {farm.details?.isActivated && <Progress />} */}
        <FarmDetailModal open={open} setOpen={setOpen} />
      </CardActions>
    </Card>
  );
}
