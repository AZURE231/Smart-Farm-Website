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
      </CardContent>
      <CardActions>
        <Button size="small" onClick={handleInit}>
          Init
        </Button>
        <FarmDetailModal open={open} setOpen={setOpen} />
      </CardActions>
    </Card>
  );
}
