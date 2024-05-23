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
import Progress from './Progress';

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
        <div className="mt-5 bg-gray-100 rounded-lg p-3">
          <Typography variant="body2" color="text.secondary">
            Date: {farm.details?.date}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Time: {farm.details?.start_time} - {farm.details?.end_time}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Cycle: {farm.details?.cycle}
          </Typography>
        </div>
      </CardContent>
      <CardActions>
        <Button size="small" onClick={handleInit}>
          Init
        </Button>
        {farm.details?.isActivated && <Progress />}
        <FarmDetailModal open={open} setOpen={setOpen} />
      </CardActions>
    </Card>
  );
}
